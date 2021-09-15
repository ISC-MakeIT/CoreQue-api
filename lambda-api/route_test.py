import unittest
from route import Route
from writer import Writer


class SpyFunctionCalling:
    def __init__(self):
        self.called_function_names = []

    def __call__(self, function_name: str):
        self.called_function_names.append(function_name)


class TestRoute(unittest.TestCase):
    def setUp(self):
        self.route = Route()

    def test_has_path(self):
        """
        パスが存在するかどうかを確認する
        """
        handlers = {
            "hoge": lambda: None,
            "hoge/fuga": lambda: None,
        }
        new_route = Route(handlers)

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
        """
        ハンドラーが呼ばれることを確認する
        """
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

    def test_get_result(self):
        """
        ハンドラーが返す値を取得する
        """
        writer = Writer()
        route = Route(writer=writer)

        def hoge() -> str:
            return '{"message": "hogehogehogegenoge"}'

        route.add(path="hoge", func=hoge)
        route.run(path="hoge")

        want = {"statusCode": 200, "body": '{"message": "hogehogehogegenoge"}'}
        got = route.get_result()
        self.assertEqual(want, got)

        def fuga() -> dict:
            return {"message": "dict to str"}

        route.add(path="fuga", func=fuga)
        route.run(path="fuga")

        want = {"statusCode": 200, "body": '{"message": "dict to str"}'}
        got = route.get_result()
        self.assertEqual(want, got)


if __name__ == "__main__":
    unittest.main()
