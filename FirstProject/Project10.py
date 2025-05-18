
is_male = False
is_tall = False

if is_male and is_tall:
    print("Your are male or tall or both")
elif not(is_male) and (is_tall):
    print("You are not a male but are tall")
elif (is_male) and not (is_tall):
    print("You are a short male")
else:
    print("Your are not male nor tall")