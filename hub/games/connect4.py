import sys
import os
import numpy as np
import pygame as pg

#importing parent class and Fonts
orig_path = sys.path[0]
sys.path[0] += ('/..')
from game import Game
from Fonts import get_font
sys.path[0] = orig_path

#global variables
width, height = 1280,720
row_size = 64
column_size = 69
board_origin = (370,160)
circles_size = (87,87)
origin = [370,160]

#Game defining class
class Connect4(Game):

    def __init__(self, player1, player2): # constructor to initialize the game state, load images, and set up the board dimensions 
        super().__init__(player1, player2) #initialise variables from parent class
        pg.init()
        #Board-Size:
        self.ROWS = 7
        self.COLS = 7
        self.board = self.game_board(self.ROWS,self.COLS) #empty board
        self.screen = pg.display.set_mode((width, height))

        self.bg = pg.image.load('games/c4_resources/Connect4bg.png')
        self.board_photo = pg.image.load('games/c4_resources/board_photo.png')
        self.red = pg.image.load('games/c4_resources/red.png')
        self.red = pg.transform.scale(self.red, circles_size)
        self.yellow = pg.image.load('games/c4_resources/yellow.png')
        self.yellow = pg.transform.scale(self.yellow, circles_size)
        self.red_transparent = self.red.copy() # transparent version of the piece for hover effect
        self.red_transparent.set_alpha(100) 
        self.yellow_transparent = self.yellow.copy() 
        self.yellow_transparent.set_alpha(100)

    def find_row(self, col): # finds the lowest empty row in the specified column to drop a piece (lowest empty index in the column)
        # returns the row index if found and None if column is full
        for i in np.arange(self.ROWS-1, -1, -1):
            if self.board[i][col] == 0:
                return i
        return None

    def drop(self,col,player):
        #adds the piece to the specific row
        for i in np.arange(self.ROWS-1,-1,-1):
            if self.board[i][col] == 0:
                self.board[i][col] = player
                return i
        return None
    
    def mark(self): # to draw the board based on current state of board array
        for r in range(self.ROWS):
            for c in range(self.COLS):
                #red for player1 yellow for player2
                if self.board[r][c] == 1:
                    self.screen.blit(self.red, (board_origin[0]+c*column_size, board_origin[1]+r*row_size-7))
                elif self.board[r][c] == 2:
                    self.screen.blit(self.yellow, (board_origin[0]+c*column_size, board_origin[1]+r*row_size-7))

    def draw_hover(self): # semi transparent piece (ghost piece) on the board to indicate where the piece would be placed if they click
        mouse_pos = pg.mouse.get_pos()
        #semi transparent piece
        if self.inside_board(mouse_pos):
            col = (mouse_pos[0] - board_origin[0])// column_size
            row = self.find_row(col)
            if row is not None:
                if self.board[0][col] == 0:
                        if self.player == 1:
                            self.screen.blit(self.red_transparent, (board_origin[0]+col*column_size, board_origin[1] + row*row_size-7))
                        elif self.player == 2:
                            self.screen.blit(self.yellow_transparent, (board_origin[0]+col*column_size, board_origin[1] + row*row_size-7))
        
    def draw(self):
        self.make_board(self.bg,self.board_photo, origin[0], origin[1]) # to draw the background and board every frame
        self.mark() #draw the pieces on the board based on the current state
        self.draw_hover() # to draw ghost piece based on mouse position and player
        pg.display.update()
    def check_win(self,player,col,row):
        #win needs to be checked only in the column row or diagonal where last item was placed
        # np.lib.stride_tricks.sliding_window_view(arr,window_shape) lists all fixed size sub segments of arr
        # if True in np.all(arr1 == arr2, axis=1): here used to check if any row of arr1 matches arr2 exactly

        #extracting the specific row and column
        Row=self.board[row]
        Col=self.board[:,col]

        #Win array checks for connected 4
        Win=np.ones(4,dtype=int)
        if player == 2:
            Win += 1

        # Row and col check
        Row_Subsets = np.lib.stride_tricks.sliding_window_view(Row,window_shape=4)
        Col_Subsets = np.lib.stride_tricks.sliding_window_view(Col,window_shape =  4)
        bool_row = True in np.all(Row_Subsets==Win, axis=1)
        bool_col = True in np.all(Col_Subsets==Win, axis=1)
        if bool_row or bool_col:
            return True
        
        #extrcting main diagonal and checking it
        diagonal = np.diag(self.board, k=col - row)
        if diagonal.size >= 4:
            diagonal_Subsets = np.lib.stride_tricks.sliding_window_view(diagonal, window_shape = 4)
            bool_main = True in np.all(diagonal_Subsets == Win, axis=1)
            if(bool_main):
                return True
        #extracting anti diagonal and checking it
        anti_diagonal = np.diag(np.fliplr(self.board), k=(self.COLS - 1) - (col + row))
        if anti_diagonal.size >= 4:
            anti_Subsets = np.lib.stride_tricks.sliding_window_view(anti_diagonal, window_shape = 4)
            bool_anti = True in np.all(anti_Subsets == Win, axis=1)
            if bool_anti:
                return True
               
        return False
    def inside_board(self,mouse_pos): # checks if mouse position is inside board
        return (board_origin[0] <= mouse_pos[0] < board_origin[0] + self.COLS*column_size) and (board_origin[1] <= mouse_pos[1] < board_origin[1] + self.ROWS*row_size)
    #Main Loop
    def run(self):
        pg.init()
        clock = pg.time.Clock()
        screen = pg.display.set_mode((width, height ))
        pg.display.set_caption('Connect FOUR')
        running = True

        self.draw()        
        while running:

            #To quit
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game_over = True
                    pg.quit()
                    return None
                #User inputs
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r: #Press R to restart
                        self.reset()
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    result = self.check_buttons_press(mouse_pos)
                    if result is not None:
                        return result
                    
                    if(self.inside_board(mouse_pos)): # checking if click was inside board
                        col = (mouse_pos[0] - board_origin[0])// column_size
                        player = self.player
                        row = self.drop(col,player)
                        if row is not None:
                            if self.check_win(player, col, row):
                                self.game_over = True
                                #if Winner is found:
                                self.draw()
                                winner = self.current_player() #winner name
                                text = get_font(36,'Nice').render(f"{winner} wins", True, ((255,0,0) if self.player == 1 else (255,255,0)))

                                self.show_text(text,(520,670))
                                return winner
                        
                        #move on to next move
                            self.switch_turn()
                    if self.board_full():
                        self.game_over = True

                        #Board full but no winner...
                        self.draw()
                        tie_text = self.font.render("Match tied", True, (255, 255, 255))
                        self.show_text(tie_text,(520,670))
                        return "Game Drawn"
            self.draw()
            pg.display.update()
            clock.tick(60)

if __name__ == "__main__":
    player1 = sys.argv[1] # player names from CLI
    player2 = sys.argv[2]
    game = Connect4(player1, player2) #instance of the Connect4 class for the gameplay
    winner = game.run() 
    print(f"{winner}")  
