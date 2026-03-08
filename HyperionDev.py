# Guess the Number
# ----------------------------------------
# The computer picks a random number between 1 and 10.
# The player has to guess the number.
# The game gives hints if the guess is too high or too low.
# The game ends when the player guesses correctly.

import random

print("Welcome to 'Guess the Number'!")
print("I'm thinking of a number between 1 and 10...")

# Computer chooses a random number
secret_number = random.randint(1, 10)
guess = None

# Keep asking until the player guesses correctly
while guess != secret_number:
    # Make sure the input is a number
    try:
        guess = int(input("Take a guess: "))
    except ValueError:
        print("That's not a valid number! Try again.")
        continue

    # Provide a response based on whether the guess
    # was higher or lower or spot on
    if guess < secret_number:
        print("Too low! Try again.")
    elif guess > secret_number:
        print("Too high! Try again.")
    else:
        print("🎉 You got it! The number was", secret_number)

        # Prompt the player for a rematch or "It's past my bedtime" option
        restart = input("Do you wish to play again? y/n : ")

        if restart.lower() == "y":
            guess = None
            secret_number = random.randint(1, 10)
        elif restart.lower() == "n":
            print("Good game!")
        else:
            print("I'll take that as a no, good game though!")
