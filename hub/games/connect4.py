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

#Game defining class
class Connect4(Game):

    def __init__(self, player1, player2):
        super().__init__(player1, player2)

        #Board-Size:
        self.ROWS = 7
        self.COLS = 7
        self.board = np.zeros((self.ROWS,self.COLS) , dtype = int) #empty board

    def drop(self,col,player):
        #returns the row where item gets placed
        for i in np.arange(self.ROWS-1,-1,-1):
            if self.board[i][col] == 0:
                self.board[i][col] = player
                return i
        return None
    
    def draw(self,screen):
        #gray screen and green borders
        screen.fill((255,255,255))
        for r in range(self.ROWS):
            for c in range(self.COLS):
                #red for player1 blue for player2
                pygame.draw.rect(screen, (0,255,0), (c*80+50, r*80+50, 80, 80), 5)
                if self.board[r][c] == 1:
                    pygame.draw.rect(screen, (255,0,0), (c*80+55, r*80+55, 70, 70))
                elif self.board[r][c] == 2:
                    pygame.draw.rect(screen, (0,0,255), (c*80+55, r*80+55, 70, 70))

        screen.blit(self.Resign_text,self.Resign_rect)
        pygame.display.update()

    def show_text(self,text,pos = (150,600)):
        
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

    #Main Loop
    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        global screen
        screen = pygame.display.set_mode((width, height ))
        pygame.display.set_caption('Connect FOUR')
        running = True
        #font
        self.font = pygame.font.Font('games/c4_resources/ArcadeGamer.ttf', 36)

        #Resign button
        self.Resign_text = self.font.render("RESIGN",True,"#00ff00")
        self.Resign_rect = self.Resign_text.get_rect(center=(400, 670))
        self.draw(screen)

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
                    if(self.Resign_rect.collidepoint(mouse_pos)):
                        self.game_over = True
                        winner = self.current_player() #winner name
                        text = self.font.render(f"{winner} wins", True, ((255,0,0) if player == 1 else (0,0,255)))
                        self.show_text(text)
                        return self.Resign(self.player)
                    
                    if(mouse_pos[1]) > 650:
                        continue
                    col = (mouse_pos[0] - 50)//80
                    if col > 6 or col < 0:
                        continue
                    player = self.player
                    row = self.drop(col,player)
                    if row is not None:
                        if self.check_win(player, col, row):
                            self.game_over = True
                            #if Winner found:
                            self.draw(screen)
                            winner = self.current_player() #winner name
                            text = self.font.render(f"{winner} wins", True, ((255,0,0) if player == 1 else (0,0,255)))

                            self.show_text(text)
                            return winner
                        
                        #move on with next move
                        self.switch_turn()
                    if self.board_full():
                        self.game_over = True

                        #Board full but no winner...
                        self.draw(screen)
                        tie_text = self.font.render("Match tied", True, (0, 0, 0))
                        self.show_text(tie_text)
                        return "Nobody"
            self.draw(screen)
            pygame.display.update()
            clock.tick(60)

if __name__ == "__main__":
    player1 = sys.argv[1]
    player2 = sys.argv[2]
    game = Connect4(player1, player2)
    winner = game.run()
    print( '\n', f"{winner} wins")