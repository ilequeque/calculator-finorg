from decimal import Decimal, ROUND_HALF_UP

import dotenv
from flask import Flask, jsonify, request, send_from_directory

from rates.cbrf_parser import parse_cbrf
from rates.nbkgs_parser import parse_nbkgs
from rates.rates_store import get_all_sources, get_all_currencies, get_rate, rates

dotenv.load_dotenv()

app = Flask(__name__, static_folder="static")

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/api/load_sources")
def load_sources():
    return jsonify(get_all_sources())

@app.route("/api/load_currencies")
def load_currencies():
    return jsonify(get_all_currencies())

@app.route("/api/get-rate-value", methods=["POST"])
def get_rate_value():
    data = request.json
    if not data:
        return jsonify({"error": "Empty JSON body"}), 400

    source = data.get("exchangeSource")
    from_cur = data.get("currencyFrom")
    to_cur = data.get("currencyTo")

    print(rates)
    rate = get_rate(source, from_cur, to_cur)
    if rate == 0:
        return jsonify({"error": "Rate not found"}), 500
    rate = Decimal(str(rate))

    # Входные параметры
    com_ratio = Decimal(data.get("comRatio", 0))
    sum_agent = Decimal(data.get("sumAgent", 0))
    low_agent = Decimal(data.get("lowAgent", 0))
    low_prv = Decimal(data.get("lowPrv", 0))

    ercom = rate - (rate * com_ratio / 100)
    sum_prv = (sum_agent * ercom).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    # Получение курса к базовой валюте (KZT)
    def get_to_kzt(currency):
        if currency == "KZT":
            return Decimal("1")
        kzt_rate = get_rate("НБРК", currency, "KZT")
        return Decimal(str(kzt_rate)) if kzt_rate else Decimal("1")

    # Базис агента и провайдера в KZT
    agent_to_kzt = get_to_kzt(from_cur)
    prv_to_kzt = get_to_kzt(to_cur)

    sum_agent_basis = sum_agent * agent_to_kzt
    sum_prv_basis = sum_prv * prv_to_kzt

    # Расчёт доходов
    income = sum_agent_basis - sum_prv_basis
    gross_income = (
        income
        - (low_agent / 100 * sum_agent_basis)
        + (low_prv / 100 * sum_prv_basis)
    )

    return jsonify({
        "income": float(round(income, 2)),
        "gross_Income": float(round(gross_income, 2))
    })


if __name__ == "__main__":
    from rates.nbkr_parser import parse_nbkr
    from rates.halyk_parser import parse_halyk

    print("Загружаем курсы валют...")
    parse_nbkr()
    parse_halyk()
    parse_cbrf()
    parse_nbkgs()

    app.run(port=5000, debug=True)
