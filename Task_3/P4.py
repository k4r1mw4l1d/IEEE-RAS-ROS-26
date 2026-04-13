import random

def get_unique_lottery():
    numbers = set()

    while len(numbers) < 6:
        numbers.add(random.randint(1, 50))

    return numbers

if __name__ == "__main__":
    print(get_unique_lottery())