#1st MiniProject

import random
def game_win(user, computer):
    if user==computer:
        return None
#Snake vs Water
    if user=="s" and computer=="w":
        return True
    if user=="w" and computer=="s":
        return False
#Water vs Gun
    if user=="w" and computer=="g":
        return True
    if user=="g" and computer=="w":
        return False
#Gun vs Snake
    if user=="g" and computer=="s":
        return True
    if user=="s" and computer=="g":
        return False
rand_no = random.randint(1,3)

print("Computer's Turn: Snake(s), Water(w), Gun(g) ")
if rand_no == 1:
    computer="s"
elif rand_no==2:
    computer="w"
else:
    computer="g"

user= input("Your Turn: Snake(s), Water(w), Gun(g):  ").lower()

result= game_win(user,computer)
print(f"You choose {user} ")
print(f"Computer choose {computer} ")

if result is None:
    print("It's a draw!")
elif(result):
    print("You win!")
else:
    print("You loose")