# rates/rates_store.py
rates = {}  # ключ: (source, from, to), значение: float курс

def set_rate(source, currency_from, currency_to, value):
    rates[(source, currency_from, currency_to)] = float(value)

def get_rate(source, currency_from, currency_to):
    if currency_from == currency_to:
        return 1.0

    # 1. Прямой курс
    rate = rates.get((source, currency_from, currency_to))
    if rate:
        print(f"[INFO] Прямой курс найден: {currency_from}/{currency_to} = {rate}")
        return rate

    # 2. Обратный курс
    reverse_rate = rates.get((source, currency_to, currency_from))
    if reverse_rate:
        print(f"[INFO] Используется обратный курс: {currency_from}/{currency_to} = 1 / {reverse_rate}")
        return 1 / reverse_rate

    # 3. Кросс-курс через KZT
    if currency_from != "KZT" and currency_to != "KZT":
        to_kzt = rates.get((source, currency_from, "KZT"))
        from_kzt = rates.get((source, currency_to, "KZT"))
        if to_kzt and from_kzt:
            rate = to_kzt / from_kzt
            print(f"[INFO] Кросс-курс через KZT: {currency_from}/{currency_to} = {to_kzt} / {from_kzt} = {rate}")
            return rate

        # Альтернативный путь: KZT → from и KZT → to
        kzt_to_from = rates.get((source, "KZT", currency_from))
        kzt_to_to = rates.get((source, "KZT", currency_to))
        if kzt_to_from and kzt_to_to:
            rate = kzt_to_to / kzt_to_from
            print(f"[INFO] Кросс-курс через обратный KZT: {currency_from}/{currency_to} = {kzt_to_to} / {kzt_to_from} = {rate}")
            return rate

    raise ValueError(f"❌ Курс не найден: {source} {currency_from} → {currency_to}")


def get_all_sources():
    return list(set(src for (src, _, _) in rates.keys()))

def get_all_currencies():
    return list(set(cur for (_, cur, _) in rates.keys()) | set(cur for (_, _, cur) in rates.keys()))
