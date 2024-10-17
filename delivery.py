
import requests 
postcode = input("Enter postcode: ")

response=requests.get(f"https://api.postcodes.io/postcodes/{postcode}")

if response.status_code == 200 and response.json()['status'] == 200:  
 print("Postcode is valid.") 

else: print("Invalid postcode.")


import pgeocode

outward_code = input("what is your outward code")
dist = pgeocode.GeoDistance('GB')
dist.query_postal_code('sw1a', 'n17')