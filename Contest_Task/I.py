t = int(input())
total = 0

for i in range(t):
    p, q = map(int, input().split())
    if p < q:
        total += 1

print(total)