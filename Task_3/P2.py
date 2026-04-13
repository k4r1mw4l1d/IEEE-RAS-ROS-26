def MovePlayer(directions, positions):
    x, y = positions
    for i in range(len(directions)):
        d = directions[i]
        if d == "up":
            y += 1
        elif d == "down":
            y -= 1
        elif d == "right":
            x += 1
        elif d == "left":
            x -= 1
        else:
            print("Invalid Instruction")
            break
    return (x, y)

        
if __name__ == "__main__":
    pos = (int(input("Enter X Starting Cordinates: ")),int(input("Enter Y Starting Coordinates: ")))
    n = int(input("Enter number of Instructions: "))
    inst = []
    for i in range(n):
        ins = input(f'Enter Intruction NO. {i+1}: ')
        inst.append(ins)

    print(f'Current Position: {MovePlayer(inst, pos)}')