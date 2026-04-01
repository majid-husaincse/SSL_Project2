import sys
import numpy as np
from games.tictactoe import TicTacToe
from games.othello import Othello
from games.connect4 import Connect4

#Storing player names
player1 = sys.argv[1]
player2 = sys.argv[2]

#Temporary command line interface menu for game selection
def menu():
    print("Game Menu:")
    print("1. TictacToe")
    print("2. othello")
    print("3. connect4")
    choice = int(input("Enter your choice: "))
    if (choice == 1 or choice == 2 or choice == 3):
        return choice
    else:
        print("Invalid choice try again.")
        return menu()
    
choice = menu()     
if choice == 1:
    game = TicTacToe(player1, player2)
elif choice == 2:
    game = Othello(player1, player2)
else:
    game = Connect4(player1, player2)

#Defining the base game class
class Game:
    def __init__(self, player1, player2,size):
        self.player1 = player1
        self.player2 = player2
        self.board_size = size
        self.turn = 0 #0 is for player1 and 1 is for player2
        self.board = np.zeros((self.board_size,self.board_size))
    def switch_turn(self):
        self.turn = 1 - self.turn     # switches between 0 and 1
    def current_player(self):
        return self.player2 if self.turn else self.player1
    def check_win(self):
        pass
