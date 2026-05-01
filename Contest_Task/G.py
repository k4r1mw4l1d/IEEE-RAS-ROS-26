n = int(input())
current = 0
max_cap = 0
for i in range(n):
    a, b = map(int, input().split())
    current -= a
    current += b
    max_cap = max(max_cap, current)
print(max_cap)