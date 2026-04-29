# Othello Game by Vedansh Garg

import sys
import pygame as pg 
import numpy as np

#importing parent class
orig_path = sys.path[0]
sys.path[0] += ('/..')
from game import Game
sys.path[0] = orig_path

#Dimensions
width,height=1280,720
board_dim=500
rows,cols=8,8
sq_dim=board_dim//cols
line=2
origin=[(width-board_dim)//2,(height-board_dim)//2 + 50]
#Colors
bgcolor=(128,128,128)

class Othello(Game): 
    def __init__(self, player1, player2): #consturctor for assigning player names and initializing pygame and board
        super().__init__(player1, player2)
        pg.init()
        pg.display.set_caption("Othello")
        self.screen=pg.display.set_mode((width,height))
        self.bg=pg.image.load("games/othello_resources/bg.png")
        self.board=self.game_board(rows,cols) #empty board
        self.gameboard=pg.image.load("games/othello_resources/board.png").convert_alpha()
        self.gameboard=pg.transform.scale(self.gameboard,(board_dim,board_dim))
        self.board1=self.gameboard.get_rect()
        self.board1.topleft=origin
        self.med_font = pg.font.Font(None,36)
        self.big_font = pg.font.Font(None,70)
        # Initial 4 pieces in the center of the board
        self.board[3][3]=1
        self.board[3][4]=2
        self.board[4][3]=2
        self.board[4][4]=1

    def draw(self): # for drawing the board and pieces on the screen
        self.make_board(self.bg,self.gameboard, origin[0], origin[1])   
        self.mark()
        self.draw_hover()
        pg.display.update()
        
    def mark(self): 
    # to draw the pieces on the board based on the current state of the board array 
    # iterations through the board array and checks for the value at each cell 
        for r in range(rows):
            for c in range(cols):
                x=origin[0]+c*sq_dim
                y=origin[1]+r*sq_dim
                if self.board[r][c]==1:
                    pg.draw.circle(self.screen,(255,255,255),(x+sq_dim//2 + 3,y+sq_dim//2),sq_dim//2-5)
                elif self.board[r][c]==2:
                    pg.draw.circle(self.screen,(0,0,0),(x+sq_dim//2 + 3,y+sq_dim//2),sq_dim//2-5)

    def valid_move(self,player,row,col):
     # to check if the move is valid by checking in all 8 directions for opponent pieces followed by a player's piece
        if self.board[row][col]!=0:
            return False
        opponent=3-player # if player is 1 opponent is 2 and vice versa
        directions=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)] # 8 possible directions to check
        for dr,dc in directions:
            r,c = row+dr,col+dc
            has_opponent_between=False
            while 0<=r<rows and 0<=c<cols:
                if self.board[r][c]==opponent:
                    has_opponent_between=True
                elif self.board[r][c]==player and has_opponent_between:
                    return True
                else:
                    break
                r+=dr
                c+=dc
        return False
    def flip_pieces(self, player, row, col): # to flip the opponent pieces after a valid move is made by checking in all 8 directions for opponent pieces followed by a player's piece and flipping them
        opponent=3-player
        directions=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)] # 8 possible directions to check
        for dr,dc in directions:
            r,c = row+dr,col+dc
            to_flip = []
            while 0<=r<rows and 0<=c<cols:
                if self.board[r][c] == opponent:
                    to_flip.append((r,c))
                elif self.board[r][c] == player: 
                    for fr,fc in to_flip:
                        self.board[fr][fc] = player
                    break
                else:
                    break
                r+=dr
                c+=dc

    def check_win(self): 
    # In Othello, the game ends when neither player has a valid move. The winner is the one with the most pieces on the board. If both have the same number of pieces, it's a draw.
    # this function is called after every move to check if the game has ended and to determine the winner by counting the pieces of both players and comparing them. 
    # It also checks if the board is full or if the game is already marked as over.
        black_count = np.count_nonzero(self.board == 1)
        white_count = np.count_nonzero(self.board == 2)
        if self.board_full() or self.game_over:
            if black_count>white_count:
                return self.player1
            elif white_count>black_count:
                return self.player2
            else:
                return "Draw"
        return None

    def has_any_valid_move(self, player): 
        # to check if the current player has any valid move left by iterating through the board and checking for valid moves using the valid_move function. 
        #This is used to determine if the game has ended or if the turn should be switched.
        return any(self.valid_move(player, r, c) for r in range(rows) for c in range(cols))
    
    def draw_hover(self): # to draw a ghost piece on the board to indicate where the current player's piece would be placed if they click
        if self.game_over:
            return
        mX,mY=pg.mouse.get_pos()
        # Check if mouse is inside the board
        if origin[0]<=mX<origin[0]+board_dim and origin[1]<=mY<origin[1]+board_dim:
            c=(mX-origin[0])//sq_dim
            r=(mY-origin[1])//sq_dim   
            if not (0<=r<rows and 0<=c<cols):
                return
            if self.valid_move(self.player,r,c):
            # Only show hover if the cell is empty
                if self.board[r][c] == 0:  
                    pg.draw.circle(self.screen,self.player==1 and (255,255,255) or (0,0,0),(origin[0]+c*sq_dim+sq_dim//2 + 3,origin[1]+r*sq_dim+sq_dim//2),sq_dim//2-5)
                
    def counter(self): # to count the number of pieces of both players and display them on the screen by counting the pieces, it also draws circles next to the counts to indicate which count belongs to which player.
        black = np.count_nonzero(self.board == 1)
        white = np.count_nonzero(self.board == 2)
        font=pg.font.Font(None,36)
        pg.draw.circle(self.screen,(255,255,255),(80,200),40)
        pg.draw.circle(self.screen,(0,0,0),(1030,200),40)
        text_black = font.render(str(black), True, (0,0,0))
        text_white = font.render(str(white), True, (255,255,255))
        self.screen.blit(text_black, (80 - text_black.get_width()//2, 200 - text_black.get_height()//2))
        self.screen.blit(text_white, (1030 - text_white.get_width()//2, 200 - text_white.get_height()//2))
  
    def reset(self): #to reset the board on R key
        self.player=1
        self.game_over=False
        self.board=np.zeros((rows,cols)) #numpy array for board
        self.board[3][3]=1
        self.board[3][4]=2
        self.board[4][3]=2
        self.board[4][4]=1

    def run(self):
        clock=pg.time.Clock()
        while True:
            for event in pg.event.get():
                if event.type==pg.QUIT: # to quit the game when the user clicks the close button on the window
                    pg.quit()
                    sys.exit()
                if event.type==pg.MOUSEBUTTONDOWN: 
                    """ to handle mouse clicks for making moves, offering a draw, or resigning. It checks the position of the click and determines if it's on the board for making a move or on the buttons for offering a draw or resigning.
                      If it's a valid move, it updates the board and checks for game over conditions. If it's a button click, it returns the appropriate result."""

                    mX,mY=event.pos
                    result = self.check_buttons_press((mX,mY))
                    if result is not None:
                        return result
                    if origin[0]<=mX<origin[0]+board_dim and origin[1]<=mY<origin[1]+board_dim and not self.game_over: # Check if click is inside the board and game is not over
                        c=(mX-origin[0])//sq_dim
                        r=(mY-origin[1])//sq_dim
                        if not (0<=r<rows and 0<=c<cols):
                            continue
                        if self.valid_move(self.player,r,c): # Check if the move is valid
                            self.board[r][c]=self.player
                            self.flip_pieces(self.player,r,c)
                            self.switch_turn() # Switch turn after a valid move
                            if not self.has_any_valid_move(self.player): # Check if the next player has any valid move, if not switch back to the current player and check for game over conditions
                                self.switch_turn()
                                if not self.has_any_valid_move(self.player):
                                    self.game_over = True
                if event.type==pg.KEYDOWN: # to reset the game when the user presses the R key, it calls the reset function to clear the board and reset the game state.
                    if event.key==pg.K_r: #Press R to restart
                        self.reset()
            self.screen.blit(self.bg, (0, 0)) # to draw the background and the board on the screen
            self.make_board(self.bg,self.gameboard, origin[0], origin[1]) # to draw the background and the board on the screen
            self.mark() # to draw the pieces on the board based on the current state of the board array
            self.draw_hover() # to draw the hover effect for the current player's piece when the mouse is over a valid move
            self.counter() # to draw the counters for both players on the screen
            font=self.med_font
            for row in range(rows):
               for col in range(cols):
                    if self.valid_move(self.player,row,col): # to draw a circle on the valid moves for the current player by iterating through the board and checking for valid moves
                        pg.draw.circle(self.screen,self.player==1 and (255,255,255) or (0,0,0),(origin[0]+col*sq_dim+sq_dim//2 + 3,origin[1]+row*sq_dim+sq_dim//2),sq_dim//2-5,3)
            if self.game_over: 
            # to check for game over conditions and display the winner or if it's a draw by calling the check_win function to determine the winner and then rendering the appropriate text on the screen.
                winner = self.check_win()
                font=self.nice_font

                if winner == "Draw":
                    text = font.render("Match tied", True, (255,255,255))
                else:
                    text = font.render(f"{winner} Wins!", True, (255,255,255))
                self.show_text(text,(500,670))

                pg.display.update()
                pg.time.wait(3000)  # show result for 3 sec
                return winner   
            pg.display.update()
            clock.tick(60)      

if __name__=="__main__": # to run the game by creating an instance of the Othello class with player names and calling the run method, it also prints the winner in the console after the game ends.
    player1 = sys.argv[1] # to get player names from command line arguments
    player2 = sys.argv[2]
    game = Othello(player1, player2) # to create an instance of the Othello class with player names
    winner = game.run() # to run the game and get the winner
    if winner == "Draw": # to print the result in the terminal after the game ends
        print( '\n' , "Match tied")
    else :    
        print( '\n', f"{winner} wins")  