def calculate_bill(prices, items_bought):
    total = 0
    for item in items_bought:
        if item in prices:
            total += prices[item]
    return total

if __name__ == "__main__":
    prices = {"apple": 0.5, "banana": 0.3, "orange": 0.7}
    items_bought = ["apple", "banana", "apple"]

    bill = calculate_bill(prices, items_bought)
    print(bill)  # Output: 1.3
