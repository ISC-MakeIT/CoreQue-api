import unittest
import route


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

        want = []
        got = []
        got.append(self.route.handlers["hoge"])
        got.append(self.route.handlers["hoge/fuga"])
        self.assertEqual(want, got)


if __name__ == "__main__":
    unittest.main()
