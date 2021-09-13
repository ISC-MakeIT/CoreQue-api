import unittest
import route


class TestRoute(unittest.TestCase):
    def setUp(self):
        self.route = route.Route()

    def test_add(self):
        def hoge():
            pass

        self.route.add(path="action", func=hoge)
        want = hoge
        got = self.route.handlers["action"]
        self.assertEqual(want, got)


if __name__ == "__main__":
    unittest.main()
