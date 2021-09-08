# Tell python to include the package directory
import sys

sys.path.insert(0, "package/")

import json
import boto3
import uuid
import datetime
from pytz import timezone

table_name = "Meal"

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    resp = table.put_item(
        Item={
            "Id": str(uuid.uuid4()),
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
                "Photo": "https://example.com",
                "Timestamp": str(datetime.datetime.now(timezone("Asia/Tokyo"))),
            },
        }
    )
    return {"statusCode": 200, "body": json.dumps(resp)}
