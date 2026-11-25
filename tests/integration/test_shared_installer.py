from tests.support.shared_installer_fixture import (
    importlib, json, os, Path, shutil, subprocess, sys, tempfile, unittest, patch, attach, ROOT, spec, engine, packaging, SharedInstallerTestsFixture, LocalDevelopmentTestsFixture
)

class SharedInstallerTests(SharedInstallerTestsFixture, unittest.TestCase):
    def test_whitespace_description_rejected_before_snapshot_replacement(self):
        self.make_install(check=True)
        before = {str(p):p.read_bytes() for p in (self.market/'dist').rglob('*') if p.is_file()}
        self.manifest['description']='   ';self.write_manifest()
        result=self.make_install()
        self.assertNotEqual(result.returncode,0)
        self.assertIn('description is required',result.stderr)
        self.assertEqual(before,{str(p):p.read_bytes() for p in (self.market/'dist').rglob('*') if p.is_file()})

    def test_parallel_host_layout_preserves_existing_snapshots(self):
        self.make_install(check=True)
        before = {str(p):p.read_bytes() for p in (self.market/'dist').rglob('*') if p.is_file()}
        self.assertTrue(before)
        for obsolete in ('.claude/skills','.agents/skills'):
            path = self.root/obsolete; path.mkdir(parents=True)
            result = self.make_install()
            self.assertNotEqual(0,result.returncode)
            self.assertIn('Unsupported host-local',result.stderr)
            self.assertEqual(before, {str(p):p.read_bytes() for p in (self.market/'dist').rglob('*') if p.is_file()})
            path.rmdir()

    def test_snapshot_rejects_version_and_custom_skill_root(self):
        for change in ('version', 'skillRoot'):
            original = json.loads(json.dumps(self.manifest))
            if change == 'version':
                self.manifest['version'] = '1.0.0'
            else:
                shutil.copytree(self.root/'skills', self.root/'custom/skills')
                self.manifest['extensions']['io.zyris.distribution']['skillRoot'] = 'custom/skills'
            self.write_manifest()
            with patch.object(packaging, 'ROOT', self.root), self.assertRaises(ValueError):
                packaging.payload()
            self.manifest = original
            self.write_manifest()

    def test_removed_commands_fail_without_creating_outputs(self):
        for command in ('package', 'install', 'update', 'install-local'):
            result = subprocess.run(['make', '-s', command], cwd=self.root, capture_output=True)
            self.assertNotEqual(0, result.returncode, command)
        for command in ('build', 'install', 'update', 'install-local'):
            for prefix in ([sys.executable, 'scripts/plugin.py'],):
                result = subprocess.run(prefix + [command], cwd=self.root, capture_output=True)
                self.assertEqual(2, result.returncode, command)
        self.assertFalse((self.market/'dist').exists())
        self.assertFalse((self.root/'plugin.mk').exists())


    def test_make_metadata_check_detects_and_sync_repairs_drift(self):
        catalog = self.root/'.claude-plugin/plugin.json'
        catalog.write_text('{}')
        result = subprocess.run(['make', '-s', 'check'], cwd=self.root, capture_output=True)
        self.assertNotEqual(0, result.returncode)
        self.assertEqual('{}', catalog.read_text())
        self.invoke('make', '-s', 'sync')
        self.invoke('make', '-s', 'check')
        self.assertNotIn('version', json.loads(catalog.read_text()))


    def test_different_marketplace_name_is_rejected(self):
        self.manifest['extensions']['io.zyris.distribution']['marketplace'] = 'another-marketplace'
        self.write_manifest()
        with patch.object(engine, 'ROOT', self.root):
            with self.assertRaisesRegex(ValueError, 'Unsupported distribution'):
                engine.configuration()
            with self.assertRaisesRegex(ValueError, 'Unsupported distribution'):
                engine.repository_files(self.manifest)


    def test_extra_file_mapping_cannot_ship_local_outputs_or_bytecode(self):
        for relative in ('.local/marketplace.json', '.git/config', '.tmp/report.txt', 'dist/old.zip', '.idea/workspace.xml',
                         '__pycache__/module.pyc', 'module.pyo', 'module.pyd', '.DS_Store'):
            with self.subTest(relative=relative):
                source = self.root / relative
                source.parent.mkdir(parents=True, exist_ok=True)
                source.write_text('Fictional local output')
                self.manifest['extensions']['io.zyris.distribution']['files'] = {'assets/leak.txt': relative}
                self.write_manifest()
                with self.assertRaisesRegex(ValueError, 'Generated/local'):
                    engine.configuration(self.root)
        self.manifest['extensions']['io.zyris.distribution']['files'] = {'dist/leak.txt': 'plugin.json'}
        self.write_manifest()
        with self.assertRaisesRegex(ValueError, 'Generated/local'):
            engine.configuration(self.root)


    def test_manifest_paths_and_identity_are_validated(self):
        with patch.object(engine,'ROOT',self.root), patch.object(packaging,'ROOT',self.root):
            for cfg in ({'skillRoot':'../external'},{'skillRoot':'skills','files':{'../escape':'plugin.json'}},{'skillRoot':'skills','files':{'plugin.json':'plugin.json'}}):
                self.manifest['extensions']['io.zyris.distribution']=cfg;self.write_manifest()
                with self.assertRaises(ValueError):packaging.payload()
            self.manifest['name']='../bad';self.write_manifest()
            with self.assertRaises(ValueError):engine.configuration()


    def test_existing_skills_and_private_workspace_are_untouched(self):
        private=self.root/'private-training';private.mkdir();(private/'state.json').write_text('fictional-progress')
        legacy=self.root/'home/.agents/skills/fictional-skill';legacy.mkdir(parents=True);(legacy/'SKILL.md').write_text('preserve')
        env=dict(os.environ,HOME=str(self.root/'home'))
        for args in (('claude-chat',),('all',)):
            result=subprocess.run([sys.executable,'scripts/plugin.py',*args],cwd=self.root,env=env,capture_output=True)
            self.assertEqual(2,result.returncode)
        self.install('claude')
        self.assertEqual('preserve',(legacy/'SKILL.md').read_text())
        self.assertEqual('fictional-progress',(private/'state.json').read_text())



class LocalDevelopmentTests(LocalDevelopmentTestsFixture, unittest.TestCase):
    def test_local_snapshot_is_separate_and_includes_uncommitted_changes(self):
        with patch.object(subprocess, 'run') as run:
            first = self.install('codex')
            run.assert_not_called()
            self.assertEqual('fictional-market-dev', first['marketplace'])
            self.assertNotIn(self.manifest['repository'], str(first['commands']))
            self.assertFalse(first['published'])
            self.assertFalse(list((self.market/'dist/local-development').glob('*.zip')))
            skill=self.root/'skills/fictional-skill/SKILL.md'
            skill.write_text(skill.read_text()+'\nUncommitted fictional change.\n')
            second=self.install('codex')
            self.assertNotEqual(first['plugins']['fictional-product']['version'],second['plugins']['fictional-product']['version'])
            copied=Path(second['path'])/'plugins/fictional-product/skills/fictional-skill/SKILL.md'
            self.assertEqual(skill.read_bytes(),copied.read_bytes())


    def test_local_install_needs_no_remote_and_never_writes_host_cache_directly(self):
        # Local installation never fetches the configured GitHub source.
        with patch.object(subprocess,'run') as run:
            result=self.install('claude')
            run.assert_not_called()
            self.assertEqual(['claude','plugin','install'],result['commands'][1][:3])
            self.assertTrue(Path(result['path']).is_relative_to(self.market/'dist'))


    def test_local_install_preserves_foreign_output(self):
        output=self.market/'dist/local-development/codex-marketplace'
        output.mkdir(parents=True);(output/'keep.txt').write_text('Fictional unrelated file')
        with self.assertRaisesRegex(ValueError,'unowned'):
            self.install('codex')
        self.assertEqual('Fictional unrelated file',(output/'keep.txt').read_text())
