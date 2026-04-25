class Calculator:
    def add(a,b):
        return a + b
    
    def subtract(a,b):
        return a - b
    
    def multiply(a,b):
        return a*b
    
print(f"3 + 2 = {Calculator.add(3, 2)}")
print(f"3 - 2 = {Calculator.subtract(3, 2)}")
print(f"3 x 2 = {Calculator.multiply(3, 2)}")