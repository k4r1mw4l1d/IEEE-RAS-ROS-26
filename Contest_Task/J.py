s = input()
result = ""  # ✅ string instead of integer
i = 0
while i < len(s):
    if s[i] == '.':
        result += "0" 
        i += 1
    elif s[i] == '-':
        if i + 1 < len(s) and s[i+1] == '.':
            result += "1"  
            i += 2
        else:
            result += "2" 
            i += 2
    else:
        i += 1

print(result)