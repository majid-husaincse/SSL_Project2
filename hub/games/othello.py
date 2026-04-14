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
    def __init__(self, player1, player2): #consturctor
        super().__init__(player1, player2)
        pg.init()
        pg.display.set_caption("Othello")
        self.screen=pg.display.set_mode((width,height))
        self.bg=pg.image.load("games/othello_resources/bg.png")
        self.board=np.zeros((rows,cols)) #numpy array for board
        self.gameboard=pg.image.load("games/othello_resources/board.png").convert_alpha()
        self.gameboard=pg.transform.scale(self.gameboard,(board_dim,board_dim))
        self.board1=self.gameboard.get_rect()
        self.board1.topleft=origin
        self.small_font = pg.font.Font(None,36)
        self.big_font = pg.font.Font(None,70)
        self.board[3][3]=1
        self.board[3][4]=2
        self.board[4][3]=2
        self.board[4][4]=1
    def make_board(self): #for making board
        self.screen.blit(self.gameboard, self.board1)
        
    def mark(self): #make cross or circle
        for r in range(rows):
            for c in range(cols):
                x=origin[0]+c*sq_dim
                y=origin[1]+r*sq_dim
                if self.board[r][c]==1:
                    #self.screen.blit(self.black, (x , y ))
                    pg.draw.circle(self.screen,(255,255,255),(x+sq_dim//2 + 3,y+sq_dim//2),sq_dim//2-5)
                elif self.board[r][c]==2:
                    #self.screen.blit(self.white, (x , y ))
                    pg.draw.circle(self.screen,(0,0,0),(x+sq_dim//2 + 3,y+sq_dim//2),sq_dim//2-5)

    def valid_move(self,player,row,col):
        if self.board[row][col]!=0:
            return False
        opponent=3-player
        directions=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
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
    def flip_pieces(self, player, row, col):
        opponent=3-player
        directions=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
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
        black_count = np.count_nonzero(self.board == 1)
        white_count = np.count_nonzero(self.board == 2)
        if black_count+white_count == 64 or self.game_over:
            if black_count>white_count:
                return self.player1
            elif white_count>black_count:
                return self.player2
            else:
                return "Tie"
        return None

    def has_any_valid_move(self, player):
        return any(self.valid_move(player, r, c) for r in range(rows) for c in range(cols))
    
    def draw_hover(self):
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
                
    def counter(self):
        black = np.count_nonzero(self.board == 1)
        white = np.count_nonzero(self.board == 2)
        font=pg.font.Font(None,36)
        score_text = font.render(f"{self.player1}: {black}  |  {self.player2}: {white}", True, (255,255,255))
        self.screen.blit(score_text, (20, 20))
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
                if event.type==pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type==pg.MOUSEBUTTONDOWN and not self.game_over:
                    mX,mY=event.pos
                    if origin[0]<=mX<origin[0]+board_dim and origin[1]<=mY<origin[1]+board_dim:
                        c=(mX-origin[0])//sq_dim
                        r=(mY-origin[1])//sq_dim
                        if not (0<=r<rows and 0<=c<cols):
                            continue
                        if self.valid_move(self.player,r,c):
                            self.board[r][c]=self.player
                            self.flip_pieces(self.player,r,c)
                            # Switch player
                            self.switch_turn()
                            # Check if next player has any valid moves
                            if not self.has_any_valid_move(self.player):
                                self.switch_turn()
                                if not self.has_any_valid_move(self.player):
                                    self.game_over = True
                if event.type==pg.KEYDOWN:
                    if event.key==pg.K_r: #Press R to restart
                        self.reset()
            self.screen.blit(self.bg, (0, 0))
            self.make_board()   
            self.draw_hover()
            self.mark()
            self.counter()
            font=self.small_font
            turn_text = font.render(f"Turn: {self.current_player()}", True, (255, 255, 255))
            if not self.game_over:
                self.screen.blit(turn_text, (width//2 - turn_text.get_width()//2, 120))
            for row in range(rows):
               for col in range(cols):
                    if self.valid_move(self.player,row,col):
                        pg.draw.circle(self.screen,self.player==1 and (255,255,255) or (0,0,0),(origin[0]+col*sq_dim+sq_dim//2 + 3,origin[1]+row*sq_dim+sq_dim//2),sq_dim//2-5,3)
            if self.game_over:
                winner = self.check_win()
                font=self.big_font

                if winner == "Tie":
                    text = font.render("It's a Tie!", True, (255,255,255))
                else:
                    text = font.render(f"{winner} Wins!", True, (255,255,255))
                text_rect=text.get_rect(center=(width//2, 130))
                self.screen.blit(text, text_rect)

                pg.display.update()
                pg.time.wait(3000)  # show result for 3 sec
                return winner   
            pg.display.update()
            clock.tick(60)      

if __name__=="__main__":
    player1 = sys.argv[1]
    player2 = sys.argv[2]
    game = Othello(player1, player2)
    winner = game.run()
    print( '\n', f"{winner} wins")