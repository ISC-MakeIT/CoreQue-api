import sys

sys.path.insert(0, "package/")
import boto3
from boto3.dynamodb.conditions import Key
from pprint import pprint
import json


# def get_meal(dynamodb=None):
#     if not dynamodb:
#         dynamodb = boto3.resource("dynamodb")
#     table = dynamodb.Table("Meal")

#     response = table.query(
#         IndexName="MealClassifyIndex",
#         KeyConditionExpression=Key("Classification").eq("riceball"),
#     )
#     return response["Items"]

from route import Route
from writer import Writer

placehold_dir_path = "./json/placehold/"
convenience_json_path = placehold_dir_path + "convenience.json"
file_not_found_error_json = {"statusCode": 404, "body": "File Not Found"}


def convenience() -> dict:
    try:
        with open(convenience_json_path, "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return file_not_found_error_json


writer = Writer()
route = Route(writer=writer)
route.add(path="convenience", func=convenience)


def lambda_handler(event, context):
    # meal = get_meal()
    # if meal:
    #     print("取得完了")
    #     pprint(meal, sort_dicts=False)
    # return {"statusCode": 200, "body": json.dumps(meal, indent=2)}

    route.run(path=event["pathParameters"]["proxy"])
    resp = route.get_result()
    return resp
