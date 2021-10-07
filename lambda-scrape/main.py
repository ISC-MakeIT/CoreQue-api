import uuid
from model import *
import requests
import pprint

baseURLs = [
    {"url": "https://www.sej.co.jp/products/a/sandwich/", "classification": "sandwich"},
    {"url": "https://www.sej.co.jp/products/a/onigiri/", "classification": "onigiri"},
    {"url": "https://www.sej.co.jp/products/a/bento/", "classification": "bento"},
    {"url": "https://www.sej.co.jp/products/a/bread/", "classification": "bread"},
]


def main():
    try:
        resp = []
        for baseURL in baseURLs:
            print(baseURL)
            html = requests.get(baseURL["url"]).content
            item_urls = get_url_hand_over(html)

            seven_url_prefix = "https://www.sej.co.jp{}"

            for suffix in item_urls:
                url = seven_url_prefix.format(suffix[0])
                html = requests.get(url).content
                timestamp = str(datetime.datetime.now(timezone("Asia/Tokyo")))
                classification = baseURL["classification"]
                resp.append(get_nutrition(html, classification, timestamp))
        pprint.pprint(resp)
    except Exception as e:
        print(resp)
        raise e


if __name__ == "__main__":
    main()
