import unittest
import route


class SpyFunctionCalling:
    def __init__(self):
        self.called_function_names = []

    def __call__(self, function_name: str):
        self.called_function_names.append(function_name)


class TestRoute(unittest.TestCase):
    def setUp(self):
        self.route = route.Route()

    def test_has_path(self):
        handlers = {
            "hoge": lambda: None,
            "hoge/fuga": lambda: None,
        }
        new_route = route.Route(handlers)

        self.assertTrue(new_route.has_path("hoge"))
        self.assertTrue(new_route.has_path("hoge/fuga"))

        self.assertFalse(new_route.has_path("hoge/fuga/"))

    def test_add(self):
        def hoge():
            pass

        def fuga():
            pass

        self.route.add(path="hoge", func=hoge)
        self.route.add(path="hoge/fuga", func=fuga)

        self.assertTrue(self.route.has_path("hoge"))
        self.assertTrue(self.route.has_path("hoge/fuga"))

        self.assertFalse(self.route.has_path("hoge/fuga/"))

    def test_run(self):
        spy_function_calling = SpyFunctionCalling()

        def hoge():
            spy_function_calling("hoge")

        def fuga():
            spy_function_calling("fuga")

        self.route.add(path="hoge", func=hoge)
        self.route.add(path="fuga", func=fuga)

        self.assertTrue(self.route.run("hoge"))
        self.assertTrue(self.route.run("fuga"))

        self.assertFalse(self.route.run("nothing"))

        want = ["hoge", "fuga"]
        got = spy_function_calling.called_function_names
        self.assertEqual(want, got)


if __name__ == "__main__":
    unittest.main()
