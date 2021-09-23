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
        # result = []
        # res = requests.get(baseURL)
        # if res.status_code != 200:
        #     return False
        # soup = BeautifulSoup(res.content, 'html.parser')
        # tentative = soup.find_all('figure')
        # number_of_times = len(tentative) - 1
        # for i in range(number_of_times):
        #     tentative = soup.find_all('figure')[i]
        #     link = tentative.find("a")
        #     url = link.get('href')
        #     result.append(url)
        # return result


if __name__ == "__main__":
    unittest.main()
