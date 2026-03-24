largest = None
smallest = None

while True:
    n = int(input())
    if n == -1:
        break
    if largest is None or n > largest:
        largest = n
    if smallest is None or n < smallest:
        smallest = n

print(largest, smallest)