import requests
import xml.etree.ElementTree as ET
from .rates_store import set_rate

def parse_nbkgs():
    url = "https://www.nbkr.kg/XML/daily.xml"
    allowed = {"USD", "KZT", "RUB", "KGS"}

    try:
        response = requests.get(url, timeout=10)
        tree = ET.fromstring(response.content)
    except Exception as e:
        print("❌ Не удалось загрузить или распарсить XML от НБКР:", e)
        return

    for currency in tree.findall("Currency"):
        code = currency.get("ISOCode")
        if code not in allowed or code == "KGS":
            continue

        try:
            nominal = int(currency.find("Nominal").text)
            value_text = currency.find("Value").text.replace(",", ".")
            value = float(value_text)
            rate = value / nominal

            set_rate("Национальный Банк Кыргызстана", code, "KGS", rate)
            set_rate("Национальный Банк Кыргызстана", "KGS", code, 1 / rate)
        except Exception as e:
            print(f"⚠ Ошибка при обработке {code}: {e}")