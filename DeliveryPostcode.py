import postcodes_uk
import pgeocode

def delivery():
    UserInput = input("\nPlease enter your postal code: ").upper()
    if postcodes_uk.validate(UserInput):
        verify = input(f"\nIs this your postcode?(Yes or no) => {UserInput}: ").lower()
        if verify == "yes":
            print("\nThank you! ")
        elif verify == "no":
            return delivery()
        else:
            print("\nThis is not a valid input! : ")    
            return delivery()   
    else:
        print("\nThis is not a valid postcode! ")
        return delivery()
    return UserInput

def distance_price(postcode):
    dist =  pgeocode.GeoDistance("gb")
    distance = dist.query_postal_code("N17 0BX", postcode)
    return round(distance*0.60, 2)
#example of how the code format works:

#postcode = delivery()
#fees = distance_price(postcode)

#print(f"Your additional delivery fees are : {fees}")   


   







