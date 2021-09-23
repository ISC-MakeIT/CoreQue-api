import requests
import unittest
import re
from model import *
from bs4 import BeautifulSoup
import datetime
from pytz import timezone
# testこーど実行するときpipenv run testを実行するとテストできる


class TestModel(unittest.TestCase):
    def test_get_url_hand_over(self):
        """
        ベースURLに商品URLが一覧されてるので、全てのURLをリストで返す。
        """

        want = [
            "/products/a/item/050922/",
            "/products/a/item/050949/",
            "/products/a/item/050942/",
            "/products/a/item/050940/",
            "/products/a/item/050941/",
            "/products/a/item/050939/",
            "/products/a/item/050943/",
            "/products/a/item/050925/",
            "/products/a/item/050918/",
            "/products/a/item/050944/",
            "/products/a/item/050935/",
            "/products/a/item/050933/",
            "/products/a/item/050926/",
            "/products/a/item/050937/",
            "/products/a/item/050731/"
        ]
        baseURL = "https://www.sej.co.jp/products/a/sandwich/1/l15/"
        got = get_url_hand_over(baseURL)

        self.assertEqual(want, got)

    def test_get_nutrition(self):
        """
        URLを受け取って栄養素と名前をを含むdictを返す
        熱量：456kcal、たんぱく質：17.6g、脂質：27.7g、炭水化物：34.6g（糖質：33.3g、食物繊維：1.3g）、食塩相当量：2.5g
        """
        timestamp = str(datetime.datetime.now(timezone("Asia/Tokyo")))
        seven_url_prefix = 'https://www.sej.co.jp{}'
        item_url_suffix = '/products/a/item/050922/'
        url = seven_url_prefix.format(item_url_suffix)

        want = {
            "Id": "hogefuga",
            # "Classification": "riceball",
            "Name": "玉子焼き＆海老カツサンド",
            "Calorie": 456,
            "Protein": 17,
            "Fat": 27,
            "Carbohydrate": 34,
            "Fibre": 1,
            "details": {
                "Id": "hogefuga",
                # "Classification": "riceball",
                "Name": "玉子焼き＆海老カツサンド",
                "Calorie": 456,
                "Protein": 17,
                "Fat": 27,
                "Carbohydrate": 34,
                "Fibre": 1,
                "Timestamp": timestamp,
            }
        }

        id = "hogefuga"

        got = get_nutrition(url, id, timestamp)
        self.assertEqual(want, got)


if __name__ == "__main__":
    unittest.main()
