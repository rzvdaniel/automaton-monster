import importlib.util, os, unittest

spec = importlib.util.spec_from_file_location("run_app_tests", os.path.join(os.path.dirname(__file__), "run_app_tests.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
APPS = ["games/a", "games/ab", "wallpapers/h"]


class Select(unittest.TestCase):
    def test_only_changed_apps(self):
        self.assertEqual(mod.select(APPS, ["games/a/x.js", "README.md"]), ["games/a"])

    def test_prefix_is_a_folder_not_a_name_start(self):
        self.assertEqual(mod.select(APPS, ["games/ab/x.js"]), ["games/ab"])

    def test_docs_only_runs_nothing(self):
        self.assertEqual(mod.select(APPS, ["README.md"]), [])

    def test_shared_paths_run_everything(self):
        for path in ("tools/x.py", ".github/workflows/a.yml", "design/automaton-app-ui/app.css", "catalog-apps.json"):
            self.assertEqual(mod.select(APPS, [path]), APPS, path)

    def test_no_diff_means_all(self):
        self.assertEqual(mod.select(APPS, None), APPS)


if __name__ == "__main__":
    unittest.main()
