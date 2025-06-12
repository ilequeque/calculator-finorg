import requests
import xml.etree.ElementTree as ET
from .rates_store import set_rate

def parse_nbkr():
    url = "http://www.nationalbank.kz/rss/rates_all.xml"
    resp = requests.get(url, timeout=10)
    tree = ET.fromstring(resp.content)

    for item in tree.findall(".//item"):
        title = item.findtext("title")  # например "USD"
        description = item.findtext("description")  # курс: "456.2"
        if title in ["USD", "RUB", "KGS", "KZT"]:
            set_rate("НБРК", title, "KZT", description)
            # можно также сразу добавить обратную пару:
            set_rate("НБРК", "KZT", title, 1 / float(description))
