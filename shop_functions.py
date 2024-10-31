from pprint import pprint
Items = {
    "egg noodles" : 1.59,
    "shin ramyun noodles" : 1.99,
    "rice noodles" : 1.79,
    "hello panda" : 0.99,
    "pocky" : 0.99,
    "rice snacks" : 0.99,
    "jasmine rice" : 1.29,
    "gochujang" : 0.59,
    "shrimp" : 3.99,
    "ramune" : 2.54,

    }
#repeatable input to have one input then do the anything blah lah blah, need to prob function
print("What would you like to buy?: ")  
print('\n'.join([f"{key} : {value}" for key, value in Items.items()]))
print("\nType FINISH once you are satisfied! ")
def S_E():
    UserInput = input("Select an item! => ").lower()
    if UserInput in Items.keys():
        print("Excellent choice! Anything else")
        return (UserInput, Items[UserInput])
    elif UserInput == "finish":
        return None
    else:
        print(f"Unfortunately we do not sell {UserInput}! ")
        return S_E()

 
def start_shop():
    selection = []
    total_cost = 0
    while True:
        choice = S_E()
        if choice == None:
            break
        else:
            selection.append(choice[0])
            total_cost += choice[1]
        
            
    

    return {
        'items': selection,
        'total_cost': round(total_cost, 2)
    }
print(start_shop())
        
        
