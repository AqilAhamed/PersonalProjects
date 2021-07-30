from random import randint

print("Welcome to Guess The Secret Number Game!")
print("Rules of the game are to correctly predict a secret number from the range 1 to the maximum number of your choice.")
print("Have Fun!")
print()

def choice():
    user_choice = input("Would you like to play again? (y/n): ")
    if user_choice == 'y':
        print()
        game()
    elif user_choice == 'n':
        print("Thanks for playing! See you again later :)")
    else:
        choice()
    

def game():
    n = int(input("Choose maximum range number: "))
    sec_num = randint(1, n)
    while True:
        user_input = int(input("Input your guess: "))
        if user_input > sec_num:
            print("Your number is too high. Try again.")
        elif user_input < sec_num:
            print("Your number is too low. Try again.")
        else:
            print("Congratulations! You guessed correctly!")
            break
    choice()
    
game()
