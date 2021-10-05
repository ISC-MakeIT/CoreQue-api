# Tell python to include the package directory
import sys

sys.path.insert(0, "package/")

import json
import boto3
from botocore.exceptions import ClientError
import logging
import uuid
import datetime
from pytz import timezone
import requests
import hashlib
from model import *


baseURLs = [
    {"url": "https://www.sej.co.jp/products/a/sandwich/", "classification": "sandwich"},
    {"url": "https://www.sej.co.jp/products/a/onigiri/", "classification": "onigiri"},
    {"url": "https://www.sej.co.jp/products/a/bento/", "classification": "bento"},
    {"url": "https://www.sej.co.jp/products/a/bread/", "classification": "bread"},
]

table_name = "Meal"
bucket_name = "meal-image-bucket"

dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-1")
s3 = boto3.client("s3", region_name="ap-northeast-1")

table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    resp = []
    for baseURL in baseURLs:
        print(baseURL)
        html = requests.get(baseURL["url"]).content
        item_urls = get_url_hand_over(html)

        seven_url_prefix = "https://www.sej.co.jp{}"

        for item_url in item_urls:
            seven_url_suffix = item_url[0]
            url = seven_url_prefix.format(seven_url_suffix)
            timestamp = str(datetime.datetime.now(timezone("Asia/Tokyo")))
            # TODO: あたらしくuuidを生成するとdynamodb内で重複する
            classification = baseURL["classification"]

            item = get_nutrition(url, id, classification, timestamp)
            resp = dynamodb_poi(item, table_name, dynamodb)
            if 200 != resp["ResponseMetadata"]["HTTPStatusCode"]:
                return {"statusCode": 500, "body": "Internal server error 1"}

            content = requests.get(item_url[1]).content
            resp = s3_poi(id, content, bucket_name, s3)
            if 200 != resp["ResponseMetadata"]["HTTPStatusCode"]:
                return {"statusCode": 500, "body": "Internal server error 2"}

    return {"statusCode": 200, "body": json.dumps(resp)}
