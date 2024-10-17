import math # you'll probably need this
import requests

url = "https://v6.exchangerate-api.com/v6/581c3caead82c23e72b538e3/latest/GBP"

response = requests.get(url)
data=response.json()
data = data["conversion_rates"]


#exchange_rates = {
    #'GBP' : 1,
    #'USD': 1.31,
    #'EUR': 1.19,
    #'CAD' : 1.8,
    #'AUD' : 1.94,
    #'JPY' : 195.21
#}

def check_currency_exists(currency):
    return currency in data.keys()

def currency_convert(original_c, new_c, amount):
    newAmount = amount
    if check_currency_exists(original_c):
        newAmount /= data[original_c]
    if check_currency_exists(new_c):
        newAmount *= data[new_c]
    return newAmount

old_currency="GBP"
new_currency=input("What currency would you like to convert to?").upper()
amount=int(input("How much?"))
new= currency_convert(old_currency,new_currency,amount)
print (round(new,2))