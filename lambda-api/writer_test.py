import unittest
from writer import Writer


class TestWriter(unittest.TestCase):
    def setUp(self):
        self.writer = Writer()

    def test_get_response(self):
        """
        基本的なレスポンスを返す
        """
        want = {"statusCode": 200, "body": {"message": "test"}}
        new_writer = Writer(want)
        got = new_writer.get_response()
        self.assertEqual(want, got)

    def test_body_write(self):
        """
        レスポンスのbodyに書き込む
        """
        want = {"statusCode": 200, "body": '{"message": "test"}'}
        body = '{"message": "test"}'
        self.writer.body_write(body=body)
        got = self.writer.get_response()
        self.assertEqual(want, got)


if __name__ == "__main__":
    unittest.main()
