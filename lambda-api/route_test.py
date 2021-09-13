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

    def test_add(self):
        def hoge():
            pass

        def fuga():
            pass

        self.route.add(path="hoge", func=hoge)
        self.route.add(path="hoge/fuga", func=fuga)

        want = [hoge, fuga]
        got = []
        got.append(self.route.handlers["hoge"])
        got.append(self.route.handlers["hoge/fuga"])
        self.assertEqual(want, got)

    def test_run(self):
        spy_function_calling = SpyFunctionCalling()

        def hoge():
            spy_function_calling("hoge")

        self.route.add(path="hoge", func=hoge)
        self.route.run("hoge")

        want = ["hoge"]
        got = spy_function_calling.called_function_names
        self.assertEqual(want, got)


if __name__ == "__main__":
    unittest.main()
