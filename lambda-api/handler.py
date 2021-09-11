import sys

sys.path.insert(0, "package/")
import boto3
from pprint import pprint


def get_meal(dynamodb=None):
    if not dynamodb:
        client = boto3.client("dynamodb")
    try:
        response = client.query(
            TableName="Meal",
            IndexName="MealClassifyIndex",
            Limit=10,
            Select="ALL_ATTRIBUTES",
            KeyConditionExpression="MealClassify = :meal_classify",
            ExpressionAttributeValues={":meal_classify": {"S": "riceball"}},
        )
    except client.exceptions.InternalServerError:
        return None
    else:
        return response["Item"]


def lambda_handler(event, context):
    meal = get_meal()
    if meal:
        print("取得完了")
        pprint(meal, sort_dicts=False)
    return {"statusCode": 200, "body": "Hello from Lambda!"}
