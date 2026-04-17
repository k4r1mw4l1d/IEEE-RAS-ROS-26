def safe_divide():
    try:
        num1 = float(input("Enter the numerator: "))
        num2 = float(input("Enter the denominator: "))
        result = num1 / num2
        print(f"Result: {num1} / {num2} = {result}")
    except ValueError:
        print("Error: Please enter valid numbers, not text!")
    except ZeroDivisionError:
        print("Error: Cannot divide by zero!")

if __name__ == "__main__":
    safe_divide()