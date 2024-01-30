print("Welcome to my computer quiz!")

playing = input("Do you want to play? (y/n): ")

if playing == "n":
    print('Thanks for playing')
    quit


if playing.lower() != "y":
    quit()

print("Okay! Let's play :)")
score = 0

answer = input("What is the capital of Florida? ")
if answer.lower() == "tallahassee":
    print('Correct!')
    score += 1
else:
    print("Incorrect!")

answer = input("What does “www” stand for in a website browser?? ")
if answer.lower() == "world wide web":
    print('Correct!')
    score += 1
else:
    print("Incorrect!")

answer = input("Which country consumes the most chocolate per capita? ")
if answer.lower() == "switzerland":
    print('Correct!')
    score += 1
else:
    print("Incorrect!")

answer = input("What is the most popular video game? ")
if answer.lower() == "minecraft":
    print('Correct!')
    score += 1
else:
    print("Incorrect!")

print("You got " + str(score) + " questions correct!")
print("You got " + str((score / 4) * 100) + "%.")