t = int(input())
total = 0

for i in range(t):
    p, v, t = map(int, input().split())
    if p + v + t >= 2:
        total+=1

print(total)
