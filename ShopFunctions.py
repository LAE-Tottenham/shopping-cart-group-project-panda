from rich.console import Console
from rich.table import Table
import questionary
from questionary import Style

from Validation import Validation
from CurrencyExchangeTool import ConvertCurrency

customStyle = Style([
    ('qmark', 'fg:#5F819D bold'),
    ('question', 'fg:#5F819D bold'),
    ('answer', 'fg:#543344 bold'),
    ('pointer', 'fg:#5B9B6E bold'),
    ('highlighted', 'fg:#5B9B6E bold')
])

Items = {
    "Egg Noodles": 1.59,
    "Shin Ramyun Noodles": 1.99,
    "Rice Noodles": 1.79,
    "Hello Panda": 0.99,
    "Pocky": 0.99,
    "Rice Snacks": 0.99,
    "Jasmine Rice": 1.29,
    "Gochujang": 0.59,
    "Shrimp": 3.99,
    "Ramune": 2.54,
}

console = Console()

def PrintProducts(currency):
    table = Table(show_header=True, header_style="#B2E0F6 bold")
    table.add_column("Item", style="#515262 bold", width=25)
    table.add_column("Price", justify="right")

    for item, price in Items.items():
        table.add_row(item, ConvertCurrency(price, currency))

    console.print(table)

def PrintBasket(selection, currency, basketTitle="Basket"):
    totalCost = 0
    totalQuantity = 0
    table = Table(title=f"{basketTitle}:", header_style="#B2E0F6 bold")
    
    table.add_column("Item", justify="left", style="#515262 bold", no_wrap=True)
    table.add_column("Quantity", justify="right", style="bold")
    table.add_column("Price", justify="right", style="bold")

    for item, quantity in selection.items():
        totalCost += quantity * Items[item]
        totalQuantity += quantity
        table.add_row(item, str(quantity), ConvertCurrency(quantity * Items[item], currency))

    table.add_row("Total", str(totalQuantity), ConvertCurrency(totalCost, currency), style="#5F819D bold")
    console.print(table)

def BasketTotal(selection):
    totalCost = 0
    for item, quantity in selection.items():
        totalCost += quantity * Items[item]
    return round(totalCost, 2)

def StartShop(selection={}, currency = "GBP"):
    PrintProducts(currency)

    if len(selection) > 0:
        PrintBasket(selection, currency)
        proceed = questionary.select(
            "You have an existing basket, would you like to proceed with this one?",
            choices=["Existing Basket", "New Basket"],
            style=customStyle
        ).ask()

        selection = selection if proceed == "Existing Basket" else {}

    while True:
        product = questionary.select(
            "Select a product:",
            choices=list(Items.keys()) + ["View Basket"],
            style=customStyle
            ).ask()

        if product == "View Basket":
            break
    
        quantity = int(questionary.text("How many would you like to buy?", validate=Validation.ValidateInteger, style=customStyle).ask())
        if quantity == 0:
            console.print(f"{product} have not been added to basket", style = "#7F7F7F bold")
            continue
        selection[product] = selection.get(product, 0) + quantity
        console.print(f"[#5B9B6E bold]{quantity} x {product}[/] have been added to the basket.")

    PrintBasket(selection, currency)
    return (selection, round(BasketTotal(selection), 2))
