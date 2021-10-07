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

baseURLs = [{
    "url": "https://www.sej.co.jp/products/a/sandwich/",
    "classification": "sandwich"
}, {
    "url": "https://www.sej.co.jp/products/a/onigiri/",
    "classification": "onigiri"
}, {
    "url": "https://www.sej.co.jp/products/a/bento/",
    "classification": "bento"
}, {
    "url": "https://www.sej.co.jp/products/a/bread/",
    "classification": "bread"
}, {
    "url": "https://www.sej.co.jp/products/a/men/",
    "classification": "men"
}, {
    "url": "https://www.sej.co.jp/products/a/pasta/",
    "classification": "pasta"
}, {
    "url": "https://www.sej.co.jp/products/a/gratin/ ",
    "classification": "gratin"
}, {
    "url": "https://www.sej.co.jp/products/a/dailydish/",
    "classification": "dailydish"
}, {
    "url": "https://www.sej.co.jp/products/a/salad/",
    "classification": "salad"
}, {
    "url": "https://www.sej.co.jp/products/a/sweets/",
    "classification": "sweets"
}, {
    "url": "https://www.sej.co.jp/products/a/ice_cream/",
    "classification": "ice_cream"
}, {
    "url": "https://www.sej.co.jp/products/a/hotsnack/",
    "classification": "hotsnack"
}, {
    "url": "https://www.sej.co.jp/products/a/oden/",
    "classification": "oden"
}, {
    "url": "https://www.sej.co.jp/products/a/chukaman/",
    "classification": "chukaman"
}]

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
            image_url = item_url[1]
            url = seven_url_prefix.format(seven_url_suffix)
            timestamp = str(datetime.datetime.now(timezone("Asia/Tokyo")))
            classification = baseURL["classification"]
            html = requests.get(url).content

            item = get_nutrition(html, classification, timestamp)
            if item != {}:
                resp = dynamodb_poi(item, table_name, dynamodb)
                if 200 != resp["ResponseMetadata"]["HTTPStatusCode"]:
                    return {
                        "statusCode": 500,
                        "body": "Internal server error 1"
                    }

                content = requests.get(image_url).content
                file_name = item["Id"]
                resp = s3_poi(file_name, content, bucket_name, s3)
                if 200 != resp["ResponseMetadata"]["HTTPStatusCode"]:
                    return {
                        "statusCode": 500,
                        "body": "Internal server error 2"
                    }

    return {"statusCode": 200, "body": json.dumps(resp)}
