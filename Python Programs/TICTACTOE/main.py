# main.py
import board
import KI

def new_game():
    spieler = input("Bitte gib deinen Namen ein: ")
    
    spieler_wins = 0
    computer_wins = 0
    
    while True:
        position = board.clear_board()

        while True:
            board.draw_board(position)
            current_pos = int(input(f"{spieler}, wo möchtest du deinen Zug platzieren? [0 bis 8]"))
            
            while not board.check_valid(position, current_pos):
                current_pos = int(input(f"{spieler}, dieser Zug ist nicht möglich, versuch es nochmal"))
                
            position[current_pos] = "X"
            board.draw_board(position)

            if board.check_win_condition(position):
                spieler_wins += 1
                print(f"{spieler} du geile Sau... you made it!!\n")
                break
            
            elif all(pos != " " for pos in position):
                print("Unentschieden\n")
                break
            
    
            move = KI.make_random_move(position)
            
            if move is not None:
                position[move] = "O"
                board.draw_board(position)

                if board.check_win_condition(position):
                    computer_wins += 1
                    print("Der Computer hat gewonnen!\n")
                    break
            else:
                print("Unentschieden\n")
                break
            
          

        print("****************************************************\n")        
        print("So hier kommt der aktuelle Spielstand:\n")
        print(f"{spieler}: Du hast {spieler_wins} mal gewonnen\n")
        print(f"Der computer hat {computer_wins} mal gewonnen\n")

        nochmal = input("Möchtest du ein weiteres Spiel spielen? (Ja/Nein): ")
        if nochmal.lower() != "ja":
            print("Tschüssikowski!")
            break

if __name__ == "__main__":
    new_game()

