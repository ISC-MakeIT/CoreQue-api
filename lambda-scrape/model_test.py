import requests
import unittest
import re
from model import *
from bs4 import BeautifulSoup
import datetime
from pytz import timezone
from moto import mock_dynamodb2, mock_s3
import boto3
import uuid

# testこーど実行するときpipenv run testを実行するとテストできる


class TestModel(unittest.TestCase):
    def test_get_url_hand_over(self):
        """
        ベースURLに商品URLが一覧されてるので、全てのURLをリストで返す。
        """

        want = [
            [
                '/products/a/item/050958/',
                'https://img.7api-01.dp1.sej.co.jp/item-image/050958/288678CE8FB1C5AD4F6D6B845C9A62EC.jpg',
                278
            ],
            [
                '/products/a/item/050953/',
                'https://img.7api-01.dp1.sej.co.jp/item-image/050953/D6B90933BCA77FAB458CC4AB4C095AEB.jpg',
                250
            ],
            [
                '/products/a/item/050952/',
                'https://img.7api-01.dp1.sej.co.jp/item-image/050952/650EAD4D89F5B6DD73DDBF7455EB58BD.jpg',
                250
            ],
            [
                '/products/a/item/050968/',
                'https://img.7api-01.dp1.sej.co.jp/item-image/050968/579E16F050614E49A69BB8317A78A3E1.jpg',
                238
            ],
            [
                '/products/a/item/050964/',
                'https://img.7api-01.dp1.sej.co.jp/item-image/050964/49A3A6A9B2397199620D7016292A4722.jpg',
                238
            ],
            [
                '/products/a/item/050959/',
                'https://img.7api-01.dp1.sej.co.jp/item-image/050959/772553F65ECF8F506773BB5C2EA5227A.jpg',
                290
            ],
            [
                '/products/a/item/050955/',
                'https://img.7api-01.dp1.sej.co.jp/item-image/050955/D5C962BF8F5072E5B7058A90E93A0CAE.jpg',
                330
            ],
            [
                '/products/a/item/050960/',
                'https://img.7api-01.dp1.sej.co.jp/item-image/050960/87591F6D3D6B9BCEBE2FA45E6EF3C064.jpg',
                320
            ],
            [
                '/products/a/item/050954/',
                'https://img.7api-01.dp1.sej.co.jp/item-image/050954/BC582D2D749174F882B3E3AD8C7EFF60.jpg',
                220
            ],
            [
                '/products/a/item/050946/',
                'https://img.7api-01.dp1.sej.co.jp/item-image/050946/15E7A9BEA9B15B680CE7A819B66AAB9F.jpg',
                360
            ],
            [
                '/products/a/item/050945/',
                'https://img.7api-01.dp1.sej.co.jp/item-image/050945/580096044D07AD9B8745C386F4613FF5.jpg',
                298
            ],
            [
                '/products/a/item/050628/',
                'https://img.7api-01.dp1.sej.co.jp/item-image/050628/269618B8813CBA7610643AFE6EADBC43.jpg',
                340
            ],
            [
                '/products/a/item/050449/',
                'https://img.7api-01.dp1.sej.co.jp/item-image/050449/8B493B42272674F74E16B0E332879A6A.jpg',
                198
            ],
            [
                '/products/a/item/050951/',
                'https://img.7api-01.dp1.sej.co.jp/item-image/050951/B8A049519ED8ACD2E49246664FE9165D.jpg',
                230
            ],
            [
                '/products/a/item/050731/',
                'https://img.7api-01.dp1.sej.co.jp/item-image/050731/8CABC42381DF77455B95DF8222358C50.jpg',
                258
            ]
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
        classification = "sandwich"

        want = {
            "Id":
            "b8c89b974700464208be283257b0b6702085936811545fe2b5ab74a8644acfb2",
            "Classification": "sandwich",
            "Status": "exist",
            "Name": "照焼チキンとたまごのサンド",
            "Price": 258,
            "Calorie": 424,
            "Protein": 19,
            "Fat": 25,
            "Carbohydrate": 29,
            "Fibre": 1,
            "details": {
                "Id":
                "b8c89b974700464208be283257b0b6702085936811545fe2b5ab74a8644acfb2",
                "Classification": "sandwich",
                "Name": "照焼チキンとたまごのサンド",
                "Price": 258,
                "Calorie": 424,
                "Protein": 19,
                "Fat": 25,
                "Carbohydrate": 29,
                "Fibre": 1,
                "Timestamp": timestamp,
            },
        }

        with open("mock/teriyaki.txt", "r") as f:
            data = f.read()
        html = data
        price = 258
        got = get_nutrition(html, price, classification, timestamp)
        self.assertEqual(want, got)

        want = {}
        price = None
        got = get_nutrition("", price, classification, timestamp)
        self.assertEqual(want, got)

    @mock_dynamodb2
    def test_dynamodb_poi(self):
        dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-1")
        dynamodb.create_table(
            TableName="Movies",
            KeySchema=[
                {
                    "AttributeName": "year",
                    "KeyType": "HASH"
                },  # Partition key
                {
                    "AttributeName": "title",
                    "KeyType": "RANGE"
                },  # Sort key
            ],
            AttributeDefinitions=[
                {
                    "AttributeName": "year",
                    "AttributeType": "N"
                },
                {
                    "AttributeName": "title",
                    "AttributeType": "S"
                },
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 10,
                "WriteCapacityUnits": 10
            },
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
                "image_url":
                "http://ia.media-imdb.com/images/N/O9ERWAU7FS797AJ7LU8HN09AMUP908RLlo5JF90EWR7LJKQ7@@._V1_SX400_.jpg",
                "plot":
                "A rock band plays their music at high volumes, annoying the neighbors.",
                "rank": 11,
                "running_time_secs": 5215,
                "actors":
                ["David Matthewman", "Ann Thomas", "Jonathan G. Neff"],
            },
        }
        got = dynamodb_poi(
            item=item,
            table_name="Movies")["ResponseMetadata"]["HTTPStatusCode"]
        self.assertTrue(want, got)

    @mock_s3
    def test_s3_poi(self):
        bucket_name = "meal-image-bucket"
        s3 = boto3.resource("s3", region_name="us-east-1")
        s3.create_bucket(Bucket=bucket_name)

        want = 200
        file_name = str(uuid.uuid4())
        content = requests.get("http://placehold.jp/150x150.png").content
        got = s3_poi(file_name, content,
                     bucket_name)["ResponseMetadata"]["HTTPStatusCode"]
        self.assertEqual(want, got)


if __name__ == "__main__":
    unittest.main()
