import os
import pyfiglet
import questionary
from questionary import Style
from rich.console import Console
from rich.text import Text
import pgeocode
import requests

from CurrencyExchangeTool import ConvertCurrency
from ShopFunctions import StartShop, PrintBasket, BasketTotal
from Validation import Validation
from DataSaving import DataSaving, Account

customStyle = Style([
    ('qmark', 'fg:#5F819D bold'),
    ('question', 'fg:#5F819D bold'),
    ('answer', 'fg:#543344 bold'),
    ('pointer', 'fg:#5B9B6E bold'),
    ('highlighted', 'fg:#5B9B6E bold')
])

console = Console()

class State:
    def __init__(self, shoppingStateMachine):
        self.context = shoppingStateMachine

    def OnEnter(self):
        pass

    def UpdateState(self):
        pass

def ClearConsole():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

class MenuState(State):
    def OnEnter(self):
        console.print(Text(pyfiglet.figlet_format("Panda"), style="bold black"))
        console.print(Text(pyfiglet.figlet_format("Mini Market"), style="#5B9B6E bold"))
        optionsList = ["View Products"] + (["Checkout"] if len(self.context.currentBasket) > 0 else []) + (["Login", "Sign up"] if self.context.currentAccount is None else ["Account"]) + ["Quit"]
        answers = questionary.select("Select an option:", choices=optionsList, style=customStyle).ask()
        match answers:
            case "View Products":
                return 'products'
            case "Checkout":
                return 'checkout'
            case "Login":
                return 'login'
            case "Sign up":
                return 'signup'
            case "Account":
                return 'account'
            case "Quit":
                console.print("Exiting Store.", style="#FF9999 bold")
                raise SystemExit()

class LoginState(State):
    def OnEnter(self):
        console.print(Text(pyfiglet.figlet_format("Login"), style="#5B9B6E bold"))

        if len(self.context.accounts) == 0:
            console.print("There are no existing accounts.", style="#FF9999 bold")
            input("Press Enter to Continue...")
            return 'menu'

        print("\nType 'quit' at any point to cancel\n")

        username = questionary.text(
            "Username:", 
            validate=lambda u: Validation.ValidateString(u, matchArray=list(self.context.accounts.keys()), quittable=True),
            style=customStyle
        ).ask()

        if username.lower() == 'quit':
            return 'menu'

        password = questionary.password(
            "Password:", 
            validate=lambda u: Validation.ValidateString(
                u, 
                minLength=8, 
                maxLength=20, 
                allowNumbers=True, 
                allowSymbols=True,
                matchArray=[self.context.accounts[username].Password], 
                matchError="Password is invalid",
                quittable=True
            ),
            style=customStyle
        ).ask()

        if password.lower() == 'quit':
            return 'menu'

        self.context.currentAccount = self.context.accounts[username]

        oldBasketFilled = len(self.context.currentAccount.Basket) > 0
        newBasketFilled = len(self.context.currentBasket) > 0

        if oldBasketFilled and newBasketFilled:
            currency = "GBP" if self.context.currentAccount == None else self.context.currentAccount.Currency
            prevString = f"Previous session basket: {len(self.context.currentAccount.Basket)} items - {ConvertCurrency(self.context.currentAccount.BasketCost, currency)}"
            currString = f"Current session basket: {len(self.context.currentBasket)} items - {ConvertCurrency(self.context.currentBasketCost, currency)}"
            mergeString = f"Merge Baskets: {len(self.context.currentAccount.Basket) + len(self.context.currentBasket)} items - {ConvertCurrency(self.context.currentAccount.BasketCost + self.context.currentBasketCost, currency)}"

            answers = questionary.select("You have a basket from a previous session:", choices=[prevString, currString, mergeString], style=customStyle).ask()

            if answers == prevString:
                self.context.currentBasket = self.context.currentAccount.Basket.copy()
                self.context.currentBasketCost = self.context.currentAccount.BasketCost
            elif answers == currString:
                self.context.currentAccount.Basket = self.context.currentBasket.copy()
                self.context.currentAccount.BasketCost = self.context.currentBasketCost
            elif answers == mergeString:
                allKeys = set(self.context.currentBasket.keys()).union(set(self.context.currentAccount.Basket.keys()))
                mergedBasket = {key: self.context.currentBasket.get(key, 0) + self.context.currentAccount.Basket.get(key, 0) for key in allKeys}
                mergedCost = self.context.currentAccount.BasketCost + self.context.currentBasketCost

                self.context.currentAccount.Basket = mergedBasket.copy()
                self.context.currentBasket = mergedBasket
                self.context.currentAccount.BasketCost = mergedCost
                self.context.currentBasketCost = mergedCost
        elif oldBasketFilled:
            self.context.currentBasket = self.context.currentAccount.Basket.copy()
            self.context.currentBasketCost = self.context.currentAccount.BasketCost
        elif newBasketFilled:
            self.context.currentAccount.Basket = self.context.currentBasket.copy()
            self.context.currentAccount.BasketCost = self.context.currentBasketCost

        DataSaving.SaveAccountsToFile(self.context.accounts)
        return 'menu'

class SignUpState(State):
    def OnEnter(self):
        console.print(Text(pyfiglet.figlet_format("Sign Up"), style="#5B9B6E bold"))

        print("\nType 'quit' at any point to cancel\n")

        username = questionary.text(
            "Create a username:", 
            validate=lambda u: Validation.ValidateString(
                u, 
                minLength=3, 
                maxLength=15, 
                allowNumbers=True,
                matchArray=list(self.context.accounts.keys()), 
                shouldMatch=False,
                quittable=True
            ),
            style=customStyle
        ).ask()

        if username.lower() == 'quit':
            return 'menu'

        password = questionary.password(
            "Create a password:", 
            validate=lambda u: Validation.ValidateString(
                u, 
                minLength=8, 
                maxLength=20, 
                allowNumbers=True, 
                allowSymbols=True,
                quittable=True
            ),
            style=customStyle
        ).ask()

        if password.lower() == 'quit':
            return 'menu'

        confirmPassword = questionary.password(
            "Please confirm your password:", 
            validate=lambda u: Validation.ValidateString(
                u, 
                minLength=8, 
                maxLength=20, 
                allowNumbers=True, 
                allowSymbols=True, 
                matchArray=[password], 
                matchError="Passwords must match",
                quittable=True
            ),
            style=customStyle
        ).ask()

        if confirmPassword.lower() == 'quit':
            return 'menu'

        firstName = questionary.text("Enter your first name:", validate=Validation.ValidateString, style=customStyle).ask()
        if firstName.lower() == 'quit':
            return 'menu'

        lastName = questionary.text("Enter your last name:", validate=Validation.ValidateString, style=customStyle).ask()
        if lastName.lower() == 'quit':
            return 'menu'

        console.print("Account Successfully Created.", style="#98FB98 bold")
        self.context.accounts[username] = Account(username, password, firstName, lastName)
        self.context.currentAccount = self.context.accounts[username]
        self.context.currentAccount.Basket = self.context.currentBasket.copy()
        self.context.currentAccount.BasketCost = self.context.currentBasketCost

        DataSaving.SaveAccountsToFile(self.context.accounts)

        input("Press Enter to Continue...")
        return 'menu'

class AccountState(State):
    def OnEnter(self):
        console.print(Text(pyfiglet.figlet_format("Account"), style="#5B9B6E bold"))

        console.print(f"Username: [#515262 bold]{self.context.currentAccount.Username}[/]")
        console.print(f"Name: [#515262 bold]{self.context.currentAccount.FirstName} {self.context.currentAccount.LastName}[/]")
        console.print(f"Postcode: [#515262 bold]{self.context.currentAccount.Postcode if len(self.context.currentAccount.Postcode) > 0 else 'No location set'}[/]")
        console.print(f"Currency: [#515262 bold]{self.context.currentAccount.Currency}[/]")

        if len(self.context.currentAccount.Basket) > 0:
            currency = "GBP" if self.context.currentAccount == None else self.context.currentAccount.Currency
            PrintBasket(self.context.currentAccount.Basket, currency, basketTitle = "Current Basket")

        print()
        answers = questionary.select("Select an option:", choices=(["View Order History"] if len(self.context.currentAccount.OrderHistory) > 0 else [])
                                     + ["Change Postcode", "Change Currency", "Menu", "Logout"], style=customStyle).ask()
        match answers:
            case "View Order History":
                count = 1
                for orderData in self.context.currentAccount.OrderHistory:
                    currency = "GBP" if self.context.currentAccount == None else self.context.currentAccount.Currency
                    PrintBasket(orderData[0], currency, basketTitle = f"Order {count}")
                    currency = "GBP" if self.context.currentAccount == None else self.context.currentAccount.Currency
                    console.print(f"Total cost including delivery was [#515262 bold]{ConvertCurrency(orderData[1], currency)}[/]")
                    count += 1
                input("Press Enter to Continue...")
                return 'account'
            case "Change Postcode":
                self.context.currentAccount.Postcode = questionary.text("Enter the new postcode:", validate=Validation.ValidatePostcode, style=customStyle).ask().upper()
                DataSaving.SaveAccountsToFile(self.context.accounts)
                return 'account'
            case "Change Currency":
                self.context.currentAccount.Currency = questionary.text("Enter the new currency:", validate=Validation.ValidateCurrency, style=customStyle).ask().upper()
                DataSaving.SaveAccountsToFile(self.context.accounts)
                return 'account'
            case "Logout":
                self.context.currentAccount = None
                self.context.currentBasket = {}
                self.context.currentBasketCost = 0
                return 'menu'
            case "Menu":
                return 'menu'

class ProductsState(State):
    def OnEnter(self):
        console.print(Text(pyfiglet.figlet_format("Products"), style="#5B9B6E bold"))
        currency = "GBP" if self.context.currentAccount == None else self.context.currentAccount.Currency
        self.context.currentBasket, self.context.currentBasketCost = StartShop(self.context.currentBasket, currency)
        if self.context.currentAccount != None:
            self.context.currentAccount.Basket = self.context.currentBasket.copy()
            self.context.currentAccount.BasketCost = self.context.currentBasketCost
            DataSaving.SaveAccountsToFile(self.context.accounts)
        answers = questionary.select("Select an option:", choices=(["Proceed to Checkout"] if len(self.context.currentBasket) > 0 else []) + ["Back to Menu"], style=customStyle).ask()
        return 'checkout' if answers == "Proceed to Checkout" else 'menu'

class CheckoutState(State):
    def OnEnter(self):
        console.print(Text(pyfiglet.figlet_format("Checkout"), style="#5B9B6E bold"))
        currency = "GBP" if self.context.currentAccount == None else self.context.currentAccount.Currency
        PrintBasket(self.context.currentBasket, currency)
        answers = questionary.select("Select an option:", choices=
        (["Login to Checkout", "Sign up to Checkout"] if self.context.currentAccount == None else ["Proceed to Delivery"])
        +["Add More Products", "Back to Menu"], style=customStyle).ask()
        match answers:
            case "Login to Checkout":
                return 'login'
            case "Sign up to Checkout":
                return 'signup'
            case "Proceed to Delivery":
                return 'delivery'
            case "Add More Products":
                return 'products'
            case "Back to Menu":
                return 'menu'

class DeliveryState(State):
    def OnEnter(self):
        console.print(Text(pyfiglet.figlet_format("Delivery"), style="#5B9B6E bold"))
        
        if len(self.context.currentAccount.Postcode) == 0:
            postcode = questionary.text(
                "Please enter a delivery postcode:", 
                validate=lambda u: Validation.ValidatePostcode(u),
                style=customStyle
            ).ask().upper()

            self.context.currentAccount.Postcode = postcode
            DataSaving.SaveAccountsToFile(self.context.accounts)

        area = requests.get(f"https://api.postcodes.io/postcodes/{self.context.currentAccount.Postcode}").json()['result']['admin_district']
        console.print(f"Delivery to [#515262 bold]{self.context.currentAccount.Postcode}[/] in [#515262 bold]{area}[/]")

        dist = pgeocode.GeoDistance("GB")
        distance = dist.query_postal_code("N17 0BX", self.context.currentAccount.Postcode)

        deliveryCost = round(distance * 0.6, 2)
        totalCost = round(self.context.currentBasketCost + deliveryCost, 2)

        answers = questionary.select(
            f"Delivery cost is {ConvertCurrency(deliveryCost, self.context.currentAccount.Currency)}, total cost is {ConvertCurrency(totalCost, self.context.currentAccount.Currency)}. Proceed?",
            choices=["Purchase", "Change Currency", "Change Delivery Location", "Cancel"],
            style=customStyle
            ).ask()
        
        match answers:
            case "Purchase":
                self.context.currentAccount.OrderHistory.append((self.context.currentBasket, totalCost))
                self.context.currentAccount.Basket = {}
                self.context.currentAccount.BasketCost = 0
                self.context.currentBasket = {}
                self.context.currentBasketCost = 0
                DataSaving.SaveAccountsToFile(self.context.accounts)
                console.print("Purchase complete! Thank you for shopping with us.", style="#98FB98 bold")
                input("Press Enter to Continue...")
                return 'menu'
            case "Change Currency":
                self.context.currentAccount.Currency = questionary.text("Enter the new currency:", validate=Validation.ValidateCurrency, style=customStyle).ask().upper()
                DataSaving.SaveAccountsToFile(self.context.accounts)
                return 'delivery'
            case "Change Delivery Location":
                self.context.currentAccount.Postcode = questionary.text("Enter the new postcode:", validate=Validation.ValidatePostcode, style=customStyle).ask().upper()
                DataSaving.SaveAccountsToFile(self.context.accounts)
                return 'delivery'
            case "Cancel":
                input("Press Enter to Continue...")
                return 'menu'

class ShoppingStateMachine:
    def __init__(self):
        self.accounts = DataSaving.LoadAccountsFromFile()
        self.currentAccount = None
        self.currentBasket = {}
        self.currentBasketCost = 0

        self.states = {
            'menu': MenuState(self),
            'login': LoginState(self),
            'signup': SignUpState(self),
            'account': AccountState(self),
            'products': ProductsState(self),
            'checkout': CheckoutState(self),
            'delivery': DeliveryState(self),
        }
        self.currentState = 'menu'
        ClearConsole()

    def TransitionState(self):
        nextState = self.states[self.currentState].OnEnter()
        if nextState != self.currentState:
            self.currentState = nextState
            if nextState in self.states:
                ClearConsole()
        else:
            ClearConsole()
        return True