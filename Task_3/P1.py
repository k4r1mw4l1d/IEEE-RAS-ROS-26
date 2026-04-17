import random

def pick_winner(names):
    return random.choice(names)


if __name__ == "__main__":
    list = []
    n = int(input("Enter number of names: "))
    for i in range(n):
        Name = input("Enter Name: ")
        list.append(Name)
    print("The Winner: " + pick_winner(list))