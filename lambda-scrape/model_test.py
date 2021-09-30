import requests
import unittest
import re
from model import *
from bs4 import BeautifulSoup
import datetime
from pytz import timezone
from moto import mock_dynamodb2
import boto3

# testこーど実行するときpipenv run testを実行するとテストできる


class TestModel(unittest.TestCase):
    def test_get_url_hand_over(self):
        """
        ベースURLに商品URLが一覧されてるので、全てのURLをリストで返す。
        """

        want = [
            "/products/a/item/050958/",
            "/products/a/item/050953/",
            "/products/a/item/050952/",
            "/products/a/item/050968/",
            "/products/a/item/050964/",
            "/products/a/item/050959/",
            "/products/a/item/050955/",
            "/products/a/item/050960/",
            "/products/a/item/050954/",
            "/products/a/item/050946/",
            "/products/a/item/050945/",
            "/products/a/item/050628/",
            "/products/a/item/050449/",
            "/products/a/item/050951/",
            "/products/a/item/050731/",
        ]
        with open("mock/sandwich.txt", "r") as f:
            data = f.read()
        html = data
        got = get_url_hand_over(html)

        self.assertEqual(want, got)

    def test_get_nutrition(self):
        """
        URLを受け取って栄養素と名前をを含むdictを返す
        熱量：456kcal、たんぱく質：17.6g、脂質：27.7g、炭水化物：34.6g（糖質：33.3g、食物繊維：1.3g）、食塩相当量：2.5g
        """
        timestamp = str(datetime.datetime.now(timezone("Asia/Tokyo")))
        seven_url_prefix = "https://www.sej.co.jp{}"
        item_url_suffix = "/products/a/item/050922/"
        url = seven_url_prefix.format(item_url_suffix)

        want = {
            "Id": "hogefuga",
            # "Classification": "riceball",
            "Name": "玉子焼き＆海老カツサンド",
            "Calorie": 456,
            "Protein": 17,
            "Fat": 27,
            "Carbohydrate": 34,
            "Fibre": 1,
            "details": {
                "Id": "hogefuga",
                # "Classification": "riceball",
                "Name": "玉子焼き＆海老カツサンド",
                "Calorie": 456,
                "Protein": 17,
                "Fat": 27,
                "Carbohydrate": 34,
                "Fibre": 1,
                "Timestamp": timestamp,
            },
        }

        id = "hogefuga"

        got = get_nutrition(url, id, timestamp)
        self.assertEqual(want, got)

    @mock_dynamodb2
    def test_dynamodb_poi(self):
        dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-1")
        dynamodb.create_table(
            TableName="Movies",
            KeySchema=[
                {"AttributeName": "year", "KeyType": "HASH"},  # Partition key
                {"AttributeName": "title", "KeyType": "RANGE"},  # Sort key
            ],
            AttributeDefinitions=[
                {"AttributeName": "year", "AttributeType": "N"},
                {"AttributeName": "title", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
        )

        want = 200
        item = {
            "year": 2013,
            "title": "Turn It Down, Or Else!",
            "info": {
                "directors": ["Alice Smith", "Bob Jones"],
                "release_date": "2013-01-18T00:00:00Z",
                "rating": int(6.2),
                "genres": ["Comedy", "Drama"],
                "image_url": "http://ia.media-imdb.com/images/N/O9ERWAU7FS797AJ7LU8HN09AMUP908RLlo5JF90EWR7LJKQ7@@._V1_SX400_.jpg",
                "plot": "A rock band plays their music at high volumes, annoying the neighbors.",
                "rank": 11,
                "running_time_secs": 5215,
                "actors": ["David Matthewman", "Ann Thomas", "Jonathan G. Neff"],
            },
        }
        got = dynamodb_poi(item=item, table_name="Movies")["ResponseMetadata"][
            "HTTPStatusCode"
        ]
        self.assertTrue(want, got)


if __name__ == "__main__":
    unittest.main()
