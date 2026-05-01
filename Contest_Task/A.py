t = int(input())

for i in range(t):
    n = int(input())
    s, t = input().split()

    if sorted(s) == sorted(t):
        print("Yes")
    else:
        print("No")