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
<<<<<<< HEAD
import lxml
from bs4 import BeautifulSoup

def lambda_handler(event, context):
    

=======

table_name = "Meal"

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(table_name)


def put_meal(id):
    return table.put_item(
        Item={
            "Id": id,
            "Classification": "riceball",
            "Name": "tunamayo",
            "Calorie": 3,
            "Carbohydrate": 37,
            "Fat": 3,
            "Protein": 4,
            "Sodium": 113,
            "details": {
                "Name": "Rice Ball",
                "Classification": "riceball",
                "Name": "tunamayo",
                "Calorie": 3,
                "Carbohydrate": 37,
                "Fat": 3,
                "Protein": 4,
                "Sodium": 113,
                "Timestamp": str(datetime.datetime.now(timezone("Asia/Tokyo"))),
            },
        }
    )


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket
>>>>>>> ce6c6cd30c15c5625e48316f6deee2dcdc670e1e

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3 = boto3.client("s3")
    try:
        s3.put_object(
            Bucket="meal-image-bucket",
            Key=file_name+".png",
            Body=requests.get("http://placehold.jp/150x150.png").content,
        )
    except ClientError as e:
        logging.error(e)
        return False
    return True


def lambda_handler(event, context):
    meal_id = str(uuid.uuid4())
    resp = put_meal(meal_id)
    upload_file(meal_id, "meal-image-bucket")
    return {"statusCode": 200, "body": json.dumps(resp)}
