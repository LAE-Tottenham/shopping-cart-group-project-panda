from currency_converter import CurrencyConverter
from currencies import Currency

def verify(input):
    if input == "yes":
        return True
    elif input == "no":
        return False
    else:
        print("This is an invalid input. Try again")
    
        

def currency_converter(price):
    converter = CurrencyConverter()
    current = "GBP"
    UserInput = input("\nPlease choose your preferred currency : ").upper()
    
     
    try:
        new_price = converter.convert(price, current, UserInput) 
    except ValueError:
         print(f'\nError! "{UserInput}" may be an invalid input or unsupported currency?')
         return currency_converter(price)
    
    ver = input(f"\nYou have chosen {UserInput} as your chosen currency. Is this correct? : ")

    if verify(ver) == True:
        pass
    elif verify(ver) == False:
        return currency_converter(price)
    else:
        return currency_converter(price)
    currency = Currency(UserInput)
    return f"\nYour total is: {currency.get_money_format(round(new_price, 2))}"

print(currency_converter(100))

    




 


