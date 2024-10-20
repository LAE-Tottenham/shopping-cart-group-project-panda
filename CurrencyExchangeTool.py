from currency_converter import CurrencyConverter
from currencies import Currency       

converter = CurrencyConverter()
def ConvertCurrency(price, currency):
    current = "GBP"
    if currency == current:
        return f"£{price:.2f}"
    new_price = converter.convert(price, current, currency) 
    return f"{Currency(currency).get_money_format(round(new_price, 2))}"