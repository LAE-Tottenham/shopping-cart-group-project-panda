import os
import json

class Account:
    def __init__(self, username, password, firstName, lastName):
        self.Username = username
        self.Password = password
        self.FirstName = firstName.capitalize()
        self.LastName = lastName.capitalize()
        self.Postcode = ""
        self.Currency = "GBP"
        self.Basket = {}
        self.BasketCost = 0
        self.OrderHistory = []

    def ToDict(self):
        return {
            'Username': self.Username,
            'Password': self.Password,
            'FirstName': self.FirstName,
            'LastName': self.LastName,
            'Postcode': self.Postcode,
            'Currency': self.Currency,
            'Basket': self.Basket,
            'BasketCost': self.BasketCost,
            'OrderHistory': self.OrderHistory
        }
    
    @classmethod
    def FromDict(cls, dictData):
        account = cls(
            username=dictData['Username'],
            password=dictData['Password'],
            firstName=dictData['FirstName'],
            lastName=dictData['LastName']
        )
        account.Postcode = dictData['Postcode']
        account.Currency = dictData['Currency']
        account.Basket = dictData['Basket']
        account.BasketCost = dictData['BasketCost']
        account.OrderHistory = dictData['OrderHistory']
        return account

class DataSaving:
    @staticmethod
    def SaveAccountsToFile(accounts):
        with open("Accounts.json", "w") as file:
            json.dump({key: value.ToDict() for key, value in accounts.items()}, file, indent=4) 

    @staticmethod
    def LoadAccountsFromFile():
        if not os.path.exists("Accounts.json") or os.stat("Accounts.json").st_size == 0:
            return {}

        with open("Accounts.json", "r") as file:
            return {key: Account.FromDict(value) for key, value in json.load(file).items()}
