import unittest
import route


class TestRoute(unittest.TestCase):
    def setUp(self):
        self.route = route.Route()

    def test_append(self):
        def hoge():
            pass

        self.route.add("action", hoge)
        want = hoge
        got = self.route.handlers["action"]
        self.assertEqual(want, got)


if __name__ == "__main__":
    unittest.main()
