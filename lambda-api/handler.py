import sys

sys.path.insert(0, "package/")
import boto3
from boto3.dynamodb.conditions import Key
from pprint import pprint
import json


def get_meal(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("Meal")

    response = table.query(
        IndexName="MealClassifyIndex",
        KeyConditionExpression=Key("Classification").eq("riceball"),
    )
    return response["Items"]


def lambda_handler(event, context):
    meal = get_meal()
    if meal:
        print("取得完了")
        pprint(meal, sort_dicts=False)
    return {"statusCode": 200, "body": json.dumps(meal, indent=2)}
