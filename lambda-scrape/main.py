from model import *
import json

baseURL = "https://www.sej.co.jp/products/a/sandwich/1/l15/"
item_urls_suffix = get_url_hand_over(baseURL)

seven_url_prefix = 'https://www.sej.co.jp{}'
resp = []
for suffix in item_urls_suffix:
    url = seven_url_prefix.format(suffix)
    timestamp = str(datetime.datetime.now(timezone("Asia/Tokyo")))
    resp.append(get_nutrition(url, id, timestamp))

print(resp)
