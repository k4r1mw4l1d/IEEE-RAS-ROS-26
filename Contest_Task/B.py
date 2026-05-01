t = int(input())

for i in range(t):
    n = int(input())
    arr = list(map(int, input().split()))

    if arr[0] == arr[1]:
        common = arr[0]
    else:
        if arr[0] == arr[2]:
            common = arr[0]
        else:
            common = arr[1]

    for i in range(n):
        if arr[i] != common:
            print(i + 1)
            break
