class Player:
    def __init__(self):
        self.name = ""
        self.symbol = ""

    def choose_name(self):
        while True:
            name = input("Enter Your Name: ")
            if name.isalpha():
                self.name = name
                break
            print("Invalid Name Please use letters only")

    def choose_symbol(self):
        while True:
            symbol = input(f"{self.name}, Choose your symbol: ")
            if symbol.isalpha() and len(symbol) == 1:
                self.symbol = symbol.upper()
                break
            print("Please choose single letter only")

class Menu:
    def display_main_menu(self):
        print("Welcome to TIC-TAC-TOE game")
        print("1. Start game")
        print("2. Quit game")

        choice = input("Enter Your Choice (1 or 2): ")
        return choice
    
    def display_endgame_menu(self):
        menu_text = """
Game Over!
1. Restart Game
2. Quit Game
Enter Choice (1 or 2): """
        choice = input(menu_text)
        return choice
    
class Board:
    def __init__(self):
        self.board = []
        for i in range(1,10):
            self.board.append(str(i))
    
    def display_board(self):
        for i in range(0,9,3):
            print("|".join(self.board[i:i+3]))
            if i < 6:
                print("-"*5)

    def update_board(self, choice, symbol):
        if self.is_valid_move(choice):
            self.board[choice-1] = symbol
            return True
        return False

    def is_valid_move(self, choice):
        if self.board[choice-1].isdigit():
            return True
        
    def reset_board(self):
        self.board = [str(i) for i in range(1,10)]

class Game:
    def __init__(self):
        self.players = [Player(), Player()]
        self.board = Board()
        self.menu = Menu()
        self.current_player_index = 0
    
    def start_game(self):
        choice = self.menu.display_main_menu()
        if choice == "1":
            self.setup_players()
            self.play_game()
        else:
            self.quit_game()

    def setup_players(self):
        for player in self.players:
            player.choose_name()
            player.choose_symbol()
            print("-"*20)

    def play_game(self):
        while True:
            self.play_turn()
            if self.check_win() or self.check_draw():
                choice = self.menu.display_endgame_menu()
                if choice == "1":
                    self.restart_game()
                else:
                    self.quit_game()
                    break
                
    def restart_game(self):
        self.board.reset_board()
        self.current_player_index = 0
        self.play_game()

    def check_win(self):
        win_combination = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]

        for combo in win_combination:
            if self.board.board[combo[0]] == self.board.board[combo[1]] == self.board.board[combo[2]]:
                winner = self.players[1 - self.current_player_index]
                self.board.display_board()
                print(f"\n1{winner.name} ({winner.symbol}) wins!")
                return True

        return False


    def check_draw(self):
        return all(not cell.isdigit() for cell in self.board.board)

    def play_turn(self):
        while True:
            player = self.players[self.current_player_index]
            self.board.display_board()
            print(f"{player.name}'s turn ({player.symbol})")

            try:
                cell_choice = int(input("Choose cell (1-9): "))
                if 1 <= cell_choice <= 9 and self.board.update_board(cell_choice, player.symbol):
                    break
                else:
                    print("Invalid Move")
            except ValueError:
                print("Please Enter Number from 1 To 9")

        self.switch_player()

    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index

    def quit_game(self):
        print("Thank You for Playing")

game = Game()
game.start_game()