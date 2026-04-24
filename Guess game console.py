import random

def guess_game():
    print("=== Guess the Number Game ===")
    print("I'm thinking of a number between 1 and 100.")

    secret = random.randint(1, 100)
    attempts = 0
    max_attempts = 10

    while attempts < max_attempts:
        try:
            guess = int(input(f"\nAttempt {attempts + 1}/{max_attempts} - Enter your number: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        attempts += 1

        if guess < secret:
            print("Too low!")
        elif guess > secret:
            print("Too high!")
        else:
            print(f"\n Congratulations! You found {secret} in {attempts} attempt(s)!")
            return

    print(f"\n Game over! The number was {secret}.")

guess_game()