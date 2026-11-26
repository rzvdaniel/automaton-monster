import importlib.util, os, unittest

spec = importlib.util.spec_from_file_location("check_manifests", os.path.join(os.path.dirname(__file__), "check_manifests.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
OK = {"name": "A", "summary": "s", "application": {"permissions": []}}


class Problems(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(mod.problems(OK), [])

    def test_missing_name_and_summary(self):
        self.assertEqual(len(mod.problems({"application": {"permissions": []}})), 2)

    def test_missing_permissions_is_not_an_error(self):
        self.assertEqual(mod.problems({"name": "A", "summary": "s", "application": {}}), [])

    def test_permissions_must_be_a_list(self):
        self.assertTrue(mod.problems(dict(OK, application={"permissions": "none"})))

    def test_not_an_object(self):
        self.assertEqual(mod.problems([]), ["not a JSON object"])


if __name__ == "__main__":
    unittest.main()
