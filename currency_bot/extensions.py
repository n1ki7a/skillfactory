import json
import requests
from datetime import date

from config import keys


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote.lower()]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}.')

        try:
            base_ticker = keys[base.lower()]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}.')

        r = requests.get('https://www.cbr-xml-daily.ru/latest.js')
        # Базовая валюта в этом API RUB поэтому ститаем от нее

        resp_obj = json.loads(r.content)
        fdate = date.fromisoformat(resp_obj['date']).strftime('%d.%m.%Y')

        if base_ticker == 'RUB':
            rate = resp_obj['rates'][quote_ticker]
            total = float(amount) / rate
        elif quote_ticker == 'RUB':
            rate = resp_obj['rates'][base_ticker]
            total = float(amount) * rate
        else:
            rate_quote = resp_obj['rates'][quote_ticker]
            rate_base = resp_obj['rates'][base_ticker]
            total = float(amount) / rate_quote * rate_base

        return {'total': total, 'date': fdate}


if __name__ == '__main__':
    print(Converter.get_price( 'доллар', 'рубль', '100'))
