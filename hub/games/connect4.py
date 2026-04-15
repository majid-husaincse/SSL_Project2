import sys
import os
import pygame
import numpy as np

#importing parent class
orig_path = sys.path[0]
sys.path[0] += ('/..')
from game import Game
sys.path[0] = orig_path

#global variables
width, height = 1280,720
row_size = 64
column_size = 69
board_origin = (370,160)
circles_size = (87,87)

#Game defining class
class Connect4(Game):

    def __init__(self, player1, player2):
        super().__init__(player1, player2)
        #Board-Size:
        self.ROWS = 7
        self.COLS = 7
        self.board = self.game_board(self.ROWS,self.COLS) #empty board

    def find_row(self, col):
        for i in np.arange(self.ROWS-1, -1, -1):
            if self.board[i][col] == 0:
                return i
        return None

    def drop(self,col,player):
        #returns the row where item gets placed
        for i in np.arange(self.ROWS-1,-1,-1):
            if self.board[i][col] == 0:
                self.board[i][col] = player
                return i
        return None
    def Offer_Draw(self,player):
        opponent = self.player1 if player == 2 else self.player2
        font = pygame.font.Font('games/c4_resources/niceFont.ttf', 20)
        offer_text = font.render(f"{opponent}, {self.current_player()} offers draw [Y/N]", True, (255,255,255))
        self.show_text(offer_text,(400,630))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:  # Accept draw
                        return "Draw"
                    elif event.key == pygame.K_n:  # Reject draw
                        return None
    
    def draw(self,screen):
        screen.blit(self.bg,(0,0))
        screen.blit(self.board_photo,board_origin)
        font = pygame.font.Font('games/c4_resources/niceFont.ttf', 28)
        turn_text = font.render(f"Turn: {self.current_player()}", True, (255,255,255))
        turn_rect = turn_text.get_rect(center=(640, 140))
        screen.blit(turn_text, turn_rect)
        button = pygame.image.load('games/c4_resources/button.png')
        button = pygame.transform.scale(button,(200,100))
        screen.blit(button,(50,40))
        screen.blit(button,(1030,40))
        screen.blit(button, (50,300))
        screen.blit(button, (1030,300))
        screen.blit(button, (50,400))
        screen.blit(button, (1030,400))
        screen.blit(self.OfferDraw_text, (80,430))
        screen.blit(self.OfferDraw_text,(1080,430))
        screen.blit(self.Resign_text, (60,330)) 
        screen.blit(self.Resign_text, (1040,330))
        play_turn = font.render(f"{self.player1}", True, (255,0,0))
        screen.blit(play_turn, (100,70))
        play_turn = font.render(f"{self.player2}", True, (255,255,0))
        screen.blit(play_turn, (1070, 70))
        for r in range(self.ROWS):
            for c in range(self.COLS):
                #red for player1 blue for player2
                if self.board[r][c] == 1:
                    screen.blit(self.red, (board_origin[0]+c*column_size, board_origin[1]+r*row_size-7))
                elif self.board[r][c] == 2:
                    screen.blit(self.yellow, (board_origin[0]+c*column_size, board_origin[1]+r*row_size-7))

        mouse_pos = pygame.mouse.get_pos()
        #ghost piece
        red_transparent = self.red.copy()
        red_transparent.set_alpha(100) 
        yellow_transparent = self.yellow.copy()
        yellow_transparent.set_alpha(100)
        if self.inside_board(mouse_pos):
            col = (mouse_pos[0] - board_origin[0])// column_size
            row = self.find_row(col)
            if row is not None:
                if self.board[0][col] == 0:
                        if self.player == 1:
                            screen.blit(red_transparent, (board_origin[0]+col*column_size, board_origin[1] + row*row_size-7))
                        elif self.player == 2:
                            screen.blit(yellow_transparent, (board_origin[0]+col*column_size, board_origin[1] + row*row_size-7))
        pygame.display.update()

    def show_text(self,text,pos):
        
        #show text in GUI
        screen.blit(text, pos)
        pygame.display.update()
        pygame.time.wait(3000)
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
    def inside_board(self,mouse_pos):
        return (board_origin[0] <= mouse_pos[0] < board_origin[0] + self.COLS*column_size) and (board_origin[1] <= mouse_pos[1] < board_origin[1] + self.ROWS*row_size)
    #Main Loop
    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        global screen
        screen = pygame.display.set_mode((width, height ))
        pygame.display.set_caption('Connect FOUR')
        running = True
        self.bg = pygame.image.load('games/c4_resources/Connect4bg.png')
        self.board_photo = pygame.image.load('games/c4_resources/board_photo.png')
        self.red = pygame.image.load('games/c4_resources/red.png')
        self.red = pygame.transform.scale(self.red, circles_size)
        self.yellow = pygame.image.load('games/c4_resources/yellow.png')
        self.yellow = pygame.transform.scale(self.yellow, circles_size)

        #Resign button
        self.Resign_text = self.font.render("RESIGN",True,(255,100,100))
        #offer-Draw
        self.OfferDraw_text = self.font.render("DRAW", True, (100, 255, 100))
        self.draw(screen)
        
        self.Resign1_rect = pygame.Rect(50, 300, 200, 100)
        self.Resign2_rect = pygame.Rect(1030, 300, 200, 100)
        self.OfferDraw1_rect = pygame.Rect(50, 400, 200, 100)
        self.OfferDraw2_rect = pygame.Rect(1030, 400, 200, 100)
        while running:

            #To quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    pygame.quit()
                    return None
                #User inputs
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: #Press R to restart
                        self.reset()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if(self.Resign1_rect.collidepoint(mouse_pos)):
                        self.game_over = True
                        winner = sys.argv[2] # one resigned 2 wins
                        font = pygame.font.Font('games/c4_resources/niceFont.ttf', 36)
                        text = font.render(f"{winner} wins", True, (255,255,0))
                        self.show_text(text,(450,620))
                        return self.Resign(1)
                    if(self.Resign2_rect.collidepoint(mouse_pos)):
                        self.game_over = True
                        winner = sys.argv[1] # two resigned 1 wins
                        font = pygame.font.Font('games/c4_resources/niceFont.ttf', 36)
                        text = font.render(f"{winner} wins", True, (255,0,0))
                        self.show_text(text,(450,620))
                        return self.Resign(2)
                    if(self.OfferDraw1_rect.collidepoint(mouse_pos)):
                        result = self.Offer_Draw(1)
                        if result is not None:
                            self.game_over = True
                            tie_text = self.font.render("Match tied", True, (255,255,255))
                            self.show_text(tie_text,(520,670))
                            return "Draw"
                    if(self.OfferDraw2_rect.collidepoint(mouse_pos)):
                        result = self.Offer_Draw(2)
                        if result == "Draw":
                            self.game_over = True
                            tie_text = self.font.render("Match tied", True, (255,255,255))
                            self.show_text(tie_text,(520,670))
                            return "Draw"
                    
                    if(self.inside_board(mouse_pos)):
                        col = (mouse_pos[0] - board_origin[0])// column_size
                        player = self.player
                        row = self.drop(col,player)
                        if row is not None:
                            if self.check_win(player, col, row):
                                self.game_over = True
                                #if Winner found:
                                self.draw(screen)
                                winner = self.current_player() #winner name
                                font = pygame.font.Font('games/c4_resources/niceFont.ttf', 36)
                                text = font.render(f"{winner} wins", True, ((255,0,0) if self.player == 1 else (255,255,0)))

                                self.show_text(text,(900,350))
                                return winner
                        
                        #move on with next move
                            self.switch_turn()
                    if self.board_full():
                        self.game_over = True

                        #Board full but no winner...
                        self.draw(screen)
                        tie_text = self.font.render("Match tied", True, (255, 255, 255))
                        self.show_text(tie_text,(520,670))
                        return "Game Drawn"
            self.draw(screen)
            pygame.display.update()
            clock.tick(60)

if __name__ == "__main__":
    player1 = sys.argv[1]
    player2 = sys.argv[2]
    game = Connect4(player1, player2)
    winner = game.run()
    if winner == "Draw":
        print( '\n' , "Match tied")
    if winner is not None:
        print( '\n', f"{winner} wins")