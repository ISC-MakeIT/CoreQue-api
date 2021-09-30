import requests
import unittest
import re
from model import *
from bs4 import BeautifulSoup
import datetime
from pytz import timezone
import boto3
from logging import getLogger

logger = getLogger(__name__)


def get_url_hand_over(html: str) -> list:
    result = []
    soup = BeautifulSoup(html, "html.parser")
    tentative = soup.find_all("figure")
    number_of_times = len(tentative)
    for i in range(0, number_of_times):
        tentative = soup.find_all("figure")[i]
        link = tentative.find("a")
        url = link.get("href")
        result.append(url)
    return result


def get_nutrition(url: str, id: str, classification: str, timestamp: str) -> dict:
    def str_to_int(value: str) -> int:
        return int(float(value))

    res = requests.get(url)
    if res.status_code != 200:
        return False
    soup = BeautifulSoup(res.content, "html.parser")

    td = soup.find_all("td")
    nutrient_component = td[1].text

    nutrition = []
    column = re.sub(r"[g|kcal]", ",", nutrient_component)
    b = re.split(r"（|）|kcal |、", column)
    d = ",".join(b)
    c = d.split("," "")
    strandint = list(filter(None, c))
    for i in strandint:
        Coordinate = i.find("：") + 1
        onlyNum = i[Coordinate:]
        nutrition.append(onlyNum)

    item = {
        "Id": id,
        "Classification": classification,
        "Name": soup.find("h1").text,
        "Calorie": str_to_int(nutrition[0]),
        "Protein": str_to_int(nutrition[1]),
        "Fat": str_to_int(nutrition[2]),
        "Carbohydrate": str_to_int(nutrition[3]),
        "Fibre": str_to_int(nutrition[5]),
        "details": {
            "Id": id,
            "Classification": classification,
            "Name": soup.find("h1").text,
            "Calorie": str_to_int(nutrition[0]),
            "Protein": str_to_int(nutrition[1]),
            "Fat": str_to_int(nutrition[2]),
            "Carbohydrate": str_to_int(nutrition[3]),
            "Fibre": str_to_int(nutrition[5]),
            "Timestamp": timestamp,
        },
    }
    return item


def dynamodb_poi(item: dict, table_name: str, dynamodb=None) -> dict:
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-1")
    try:
        table = dynamodb.Table(table_name)
        response = table.put_item(Item=item)
    except Exception as e:
        logger.error("Error put item")
        raise (e)
    return response


def s3_poi(file_name: str, content: bytes, bucket_name: str, s3=None):
    if not s3:
        s3 = boto3.client("s3", region_name="us-east-1")
    try:
        response = s3.put_object(
            Bucket=bucket_name,
            Key=file_name + ".png",
            Body=content,
        )
    except Exception as e:
        logger.error("Error put item")
        raise (e)
    return response
