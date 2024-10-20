from ShoppingStateMachine import ShoppingStateMachine

shoppingStateMachine = ShoppingStateMachine()

while True:
    if not shoppingStateMachine.TransitionState():
        break