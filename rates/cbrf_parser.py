import requests
import xml.etree.ElementTree as ET
from .rates_store import set_rate

def parse_cbrf():
    url = "http://www.cbr.ru/scripts/XML_daily.asp"
    try:
        resp = requests.get(url, timeout=10)
        root = ET.fromstring(resp.content)
    except Exception as e:
        print("❌ Не удалось загрузить или распарсить XML:", e)
        return

    for valute in root.findall("Valute"):
        char_code = valute.find("CharCode").text
        nominal = int(valute.find("Nominal").text)
        value_str = valute.find("Value").text.replace(",", ".")
        if char_code not in ["USD", "RUB", "KGS"]:
            continue
        try:
            value = float(value_str)
            rate = value / nominal
            # ЦБ РФ даёт курс валюты к RUB, поэтому: currency/RUB
            set_rate("ЦБРФ", char_code, "RUB", rate)
            set_rate("ЦБРФ", "RUB", char_code, 1 / rate)
        except Exception as e:
            print(f"⚠ Ошибка при обработке {char_code}: {e}")
