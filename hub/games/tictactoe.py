import sys
import os
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
rows,cols=10,10
sq_dim=board_dim//cols
line=2
origin=[(width-board_dim)//2,(height-board_dim)//2 + 50]
#Colors
bgcolor=(128,128,128)
linecolor=(23,145,135)
crosscolor=(50,50,50)
circlecolor=(240,240,240)

class Tic_Tac_Toe(Game):
    def __init__(self, player1, player2): #consturctor
        super().__init__(player1, player2)
        pg.init()
        pg.display.set_caption("10x10 Tic-Tac-Toe")
        self.bg=pg.image.load("games/ttt_resources/bg.png")
       
        self.screen=pg.display.set_mode((width,height))
        self.board=np.zeros((rows,cols)) #numpy array for board 
        self.tttboard=pg.image.load("games/ttt_resources/Wooden tic-tac-toe grid in focus.png").convert_alpha()
        self.tttboard=pg.transform.scale(self.tttboard,(board_dim,board_dim))
        self.cross=pg.image.load("games/ttt_resources/cross.png").convert_alpha()
        self.cross=pg.transform.scale(self.cross,(sq_dim,sq_dim))
        self.circle=pg.image.load("games/ttt_resources/circle1.png").convert_alpha()
        self.circle=pg.transform.scale(self.circle,(sq_dim,sq_dim))
        self.cross_sound=pg.mixer.Sound("games/ttt_resources/cross_sound.mp3")
        self.circle_sound=pg.mixer.Sound("games/ttt_resources/circle_sound.mp3")
        self.ghost_cross = self.cross.copy()
        self.ghost_cross.set_alpha(100)  # Semi-transparent
        self.ghost_circle = self.circle.copy()
        self.ghost_circle.set_alpha(100) # Semi-transparent
        self.small_font = pg.font.Font(None,36)
        self.big_font = pg.font.Font(None,70)
    def make_board(self): #for making board
        self.screen.blit(self.tttboard, (origin[0], origin[1]))

    def mark(self): #make cross or circle
        for r in range(rows):
            for c in range(cols):
                x=origin[0]+c*sq_dim
                y=origin[1]+r*sq_dim
                if self.board[r][c]==1:
                    self.screen.blit(self.cross, (x , y ))
                 
                elif self.board[r][c]==2:
                    self.screen.blit(self.circle, (x , y ))

    def draw_hover(self):
        if self.game_over:
            return
        mX,mY=pg.mouse.get_pos()
        # Check if mouse is inside the board
        if origin[0]<=mX<=origin[0]+board_dim and origin[1]<=mY<=origin[1]+board_dim:
            c=(mX-origin[0])//sq_dim
            r=(mY-origin[1])//sq_dim   
            # Only show hover if the cell is empty
            if self.board[r][c] == 0:
                x=origin[0]+c*sq_dim
                y=origin[1]+r*sq_dim    
                # Draw ghost piece based on current player
                ghost=self.ghost_cross if self.player == 1 else self.ghost_circle
                self.screen.blit(ghost,(x, y)) 
    def check_win(self,player,col,row):
        #win needs to be checked only in the column row or diagonal where last item was placed
        # np.lib.stride_tricks.sliding_window_view(arr,window_shape) lists all fixed size sub segments of arr
        # if True in np.all(arr1 == arr2, axis=1): here used to check if any row of arr1 matches arr2 exactly
        #extracting the specific row and column
        Row=self.board[row]
        Col=self.board[:,col]

        #Win array checks for connected 5
        Win=np.ones(5,dtype=int)
        if player == 2:
            Win += 1

        # Row and col check
        Row_Subsets = np.lib.stride_tricks.sliding_window_view(Row,window_shape=5)
        Col_Subsets = np.lib.stride_tricks.sliding_window_view(Col,window_shape =  5)
        bool_row = True in np.all(Row_Subsets==Win, axis=1)
        bool_col = True in np.all(Col_Subsets==Win, axis=1)
        if bool_row or bool_col:
            return True
        
        #extrcting main diagonal and checking it
        diagonal = np.diag(self.board, k=col - row)
        if diagonal.size >= 5:
            diagonal_Subsets = np.lib.stride_tricks.sliding_window_view(diagonal, window_shape = 5)
            bool_main = True in np.all(diagonal_Subsets == Win, axis=1)
            if(bool_main):
                return True
        #extracting anti diagonal and checking it
        anti_diagonal = np.diag(np.fliplr(self.board), k=(cols - 1) - (col + row))
        if anti_diagonal.size >= 5:
            anti_Subsets = np.lib.stride_tricks.sliding_window_view(anti_diagonal, window_shape = 5)
            bool_anti = True in np.all(anti_Subsets == Win, axis=1)
            if bool_anti:
                return True
               
        return False

    def run(self):
        clock=pg.time.Clock()

        #Resign button
        # self.Resign_text = self.font.render("RESIGN",True,"#00ff00")
        # self.Resign_rect = self.Resign_text.get_rect(center=(400, 670))
        while True:
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type==pg.MOUSEBUTTONDOWN and not self.game_over:
                    sound = self.cross_sound if self.player == 1 else self.circle_sound
                    sound.play(loops=0) # to play sound on click
                    mX,mY=event.pos
                    if origin[0]<=mX<=origin[0]+board_dim and origin[1]<=mY<=origin[1]+board_dim:
                        r,c=(mY-origin[1])//sq_dim,(mX-origin[0])//sq_dim
                        if self.board[r][c]==0:
                            self.board[r][c]=self.player
                            if self.check_win(self.player,c,r):
                                self.game_over=True
                            else:
                                self.switch_turn()
                if event.type==pg.KEYDOWN:
                    if event.key==pg.K_r: #Press R to restart
                        self.reset()
            self.screen.blit(self.bg, (0, 0))
            self.make_board()
            self.draw_hover()
            self.mark()
            font=self.small_font
            turn_text = font.render(f"Turn: {self.current_player()}", True, (255, 255, 255))
            if not self.game_over:
                self.screen.blit(turn_text, (width//2 - turn_text.get_width()//2, 120))
            if self.game_over:
                winner=self.current_player()
                font=self.big_font
                text=font.render(f"{winner} Wins!",True,(255,255,255))
                text_rect=text.get_rect(center=(width//2, 130))
                self.screen.blit(text, text_rect)
            pg.display.update()
            clock.tick(60)

if __name__=="__main__":
    player1 = sys.argv[1]
    player2 = sys.argv[2]

    game = Tic_Tac_Toe(player1, player2)
    winner = game.run()
    print( '\n', f"{winner} wins")
