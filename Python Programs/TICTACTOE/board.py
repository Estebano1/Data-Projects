def draw_board(position):
    print(position[0], " |", position[1], " |", position[2])
    print("---|----|---")
    print(position[3], " |", position[4], " |", position[5])
    print("---|----|---")
    print(position[6], " |", position[7], " |", position[8])
    print()

def check_valid(position, move):
    if move < 0 or move > 8 or position[move] != " ":
        print("Ungültiger Zug")
        return False
    else:
        return True

def check_win_condition(position):
    
    # horizontal
    
    if (position[0]==position[1]==position[2] and position[0] !=" "):
        return True
    elif (position[3]==position[4]==position[5] and position[3] !=" "):
        return True
    elif (position[6]==position[7]==position[8] and position[6] !=" "):
        return True
    
    # vertical
    
    elif (position[0]==position[3]==position[6] and position[0] !=" "):
        return True
    elif (position[1]==position[4]==position[7] and position[1] !=" "):
        return True
    elif (position[2]==position[5]==position[8] and position[2] !=" "):
        return True
    
    # diagonal
    
    elif (position[0]==position[4]==position[8] and position[0] !=" "):
        return True
    elif (position[2]==position[4]==position[6] and position[2] !=" "):
        return True

   
def clear_board():
    return [" "] * 9
