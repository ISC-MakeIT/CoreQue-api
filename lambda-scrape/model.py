import requests
import unittest
import boto3
import re
from model import *
from bs4 import BeautifulSoup
import datetime
from pytz import timezone
import logging
from botocore.exceptions import ClientError


def get_url_hand_over(baseURL: str) -> list:
    result = []
    res = requests.get(baseURL)
    if res.status_code != 200:
        return False
    soup = BeautifulSoup(res.content, 'html.parser')
    tentative = soup.find_all('figure')
    number_of_times = len(tentative)
    for i in range(0, number_of_times):
        tentative = soup.find_all('figure')[i]
        link = tentative.find("a")
        url = link.get('href')
        result.append(url)
    return result


def get_nutrition(url: str, id: str, timestamp: str) -> dict:
    def str_to_int(value: str) -> int:
        return int(float(value))

    res = requests.get(url)
    if res.status_code != 200:
        return False
    soup = BeautifulSoup(res.content, 'html.parser')

    td = soup.find_all('td')
    nutrient_component = td[1].text

    nutrition = []
    column = re.sub(r"[g|kcal]",  ",",  nutrient_component)
    b = re.split(r'（|）|kcal |、',  column)
    d = ','.join(b)
    c = d.split(',' '')
    strandint = list(filter(None, c))
    for i in strandint:
        Coordinate = i.find("：")+1
        onlyNum = i[Coordinate:]
        nutrition.append(onlyNum)

    item = {
        "Id": id,
        # "Classification": "riceball",
        "Name": soup.find("h1").text,
        "Calorie": str_to_int(nutrition[0]),
        "Protein": str_to_int(nutrition[1]),
        "Fat": str_to_int(nutrition[2]),
        "Carbohydrate": str_to_int(nutrition[3]),
        "Fibre": str_to_int(nutrition[5]),
        "details": {
            "Id": id,
            # "Classification": "riceball",
            "Name": soup.find("h1").text,
            "Calorie": str_to_int(nutrition[0]),
            "Protein": str_to_int(nutrition[1]),
            "Fat": str_to_int(nutrition[2]),
            "Carbohydrate": str_to_int(nutrition[3]),
            "Fibre": str_to_int(nutrition[5]),
            "Timestamp": timestamp,
        }
    }

    return item


def dynamodb_poi(dynamodb=None) -> bool:
    if not dynamodb:
        dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url='http://localhost:8000',
            region_name='ap-northeast-1'
        )

    table = dynamodb.create_table(
        TableName='Movies',
        KeySchema=[
            {
                'AttributeName': 'year',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'title',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'year',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )

    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName='Movies')

    if table.table_status == 'ACTIVE':
        return True
    return False

# def dynamo_poi(itemData):
#     table_name = "Meal"
#     dynamodb = boto3.resource("dynamodb")
#     table = dynamodb.Table(table_name)

#     def poi(data):
#         return table.put_item(data)

#     poi(itemData)

# def s3_poihuru(file_name, bucket, object_name):
#     if object_name is None:
#         object_name = file_name

#     # Upload the file
#     s3 = boto3.client("s3")
#     try:
#         s3.put_object(
#             Bucket="meal-image-bucket",
#             Key=file_name+".png",
#             Body=requests.get("http://placehold.jp/150x150.png").content,
#         )
#     except ClientError as e:
#         logging.error(e)
#         return False
#     return True
