import requests
from .rates_store import set_rate

def parse_halyk():
    url = "https://back.halykbank.kz/common/currency-history"
    try:
        resp = requests.get(url, timeout=10)
        root = resp.json()
    except Exception as e:
        print("❌ Не удалось распарсить JSON:", e)
        return

    if not isinstance(root, dict) or "data" not in root:
        print("❌ Структура не соответствует ожиданиям")
        return

    data = root["data"]
    history = data.get("currencyHistory")
    if not history:
        print("❌ Внутри data нет 'currencyHistory' или оно не словарь")
        return

    # найти запись с самой актуальной датой
    try:
        today_data = history[0]
    except Exception as e:
        print("❌ Ошибка при определении актуальной записи:", e)
        return

    cards = today_data.get("cards", {})

    for pair, value in cards.items():
        if not pair.endswith("/KZT"):
            continue
        currency = pair.replace("/KZT", "")
        if currency not in ["USD", "RUB", "KGS"]:
            continue

        sell = value.get("sell")
        if sell:
            try:
                rate = float(sell)
                set_rate("Народный Банк продажа", currency, "KZT", rate)
                set_rate("Народный Банк продажа", "KZT", currency, 1 / rate)
            except Exception as e:
                print(f"⚠ Ошибка при парсинге {pair}: {e}")
