import uuid
from model import *
import requests

baseURL = "https://www.sej.co.jp/products/a/sandwich/1/l15/"
html = requests.get(baseURL).content
item_urls_suffix = get_url_hand_over(html)

seven_url_prefix = "https://www.sej.co.jp{}"
resp = []
for suffix in item_urls_suffix:
    url = seven_url_prefix.format(suffix)
    timestamp = str(datetime.datetime.now(timezone("Asia/Tokyo")))
    id = str(uuid.uuid4())
    resp.append(get_nutrition(url, id, timestamp))

print(resp)
