

secret_word = "Giraffe"
guess = ""
guess_count = 0
guess_limit = 3
out_of_guesses = False #out of guess nahi hai

while guess != secret_word and not(out_of_guesses):
    if guess_count < guess_limit:
        guess = input("Enter Your Guess :")
        guess_count += 1
    else:
        out_of_guesses = True
if out_of_guesses:
    print("out of guess, u lose")
else:
    print("You are correct!!")

