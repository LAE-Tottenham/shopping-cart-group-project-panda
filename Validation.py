import postcodes_uk
from currency_converter import CurrencyConverter

class Validation:
    @staticmethod
    def ValidateFloat(userInput, minValue=0, maxValue=1000):
        try:
            number = round(float(userInput), 2)
            if number < minValue:
                return f"Number must be at least {minValue}."
            if number > maxValue:
                return f"Number must be no more than {maxValue}."
            return True
        except ValueError:
            return "Invalid number. Please enter a valid float."


        
    @staticmethod
    def ValidateString(userInput, minLength = 1, maxLength = 20, allowNumbers = False, allowSymbols = False, matchArray = [], shouldMatch = True, matchError = "Input does not match", quittable = False):
        if userInput.lower() == 'quit' and quittable:
            return True
        if allowNumbers and not allowSymbols and not userInput.isalnum():
            return "Input must contain only alphanumeric characters."
        if not allowNumbers and not allowSymbols and not userInput.isalpha():
            return "Input must contain only letters."
        if len(userInput) < minLength:
            return f"Input must be at least {minLength} characters long."
        if len(userInput) > maxLength:
            return f"Input must be no more than {maxLength} characters long."
        
        if len(matchArray) > 0:
            if shouldMatch and userInput not in matchArray:
                return matchError
            elif not shouldMatch and userInput in matchArray:
                return f"Already exists"

        return True
        
    @staticmethod
    def ValidateInteger(userInput, minValue=0, maxValue=1000):
        try:
            number = int(userInput)
            if number < minValue:
                return f"Number must be at least {minValue}."
            if number > maxValue:
                return f"Number must be no more than {maxValue}."
            return True
        except ValueError:
            return "Invalid number. Please enter a valid integer."

    @staticmethod
    def ValidatePostcode(userInput):
        if not postcodes_uk.validate(userInput.upper()):
            return "Invalid Postcode"
        return True
        
    @staticmethod
    def ValidateCurrency(userInput):
        try:
            CurrencyConverter().convert(1, "GBP", userInput.upper())
            return True
        except:
            return "Invalid or Unsupported Currency"