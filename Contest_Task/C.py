t = int(input())

for i in range(t):
    s = input()
    new_s = ""
    if len(s) > 10:
        new_s = s[0] + str(len(s) - 2) + s[-1]
        print(new_s)
    else:
        print(s)