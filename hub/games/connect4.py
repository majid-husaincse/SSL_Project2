import sys
import pygame
import numpy as np

#Game defining class
class Connect4():

    def __init__(self, player1, player2):
        super().__init__()
        #initialising players
        self.player1 = player1
        self.player2 = player2

        self.turn = 0 #0 is for player1 and 1 is for player2

        #Board-Size:
        self.ROWS = 6
        self.COLS = 7
        self.board = np.zeros((self.ROWS,self.COLS) , dtype = int) #empty board

    def current_player(self):
        return self.player1 if self.turn ==0 else self.player2
    
    def drop(self,col,player):
        #returns the row where item gets placed
        for i in [5,4,3,2,1,0]:
            if self.board[i][col] == 0:
                self.board[i][col] = player
                return i
        return None
    def switch_turn(self):
        self.turn = 1 - self.turn     #switching between 0 and 1

    def draw(self,screen):
        #gray screen and green borders
        screen.fill((255,255,255))
        for r in range(self.ROWS):
            for c in range(self.COLS):
                #red for player1 blue for player2
                pygame.draw.rect(screen, (0,255,0), (c*90+50, r*90+50, 90, 90), 5) 
                if self.board[r][c] == 1:
                    pygame.draw.rect(screen, (255,0,0), (c*90+55, r*90+55, 80, 80))
                elif self.board[r][c] == 2:
                    pygame.draw.rect(screen, (0,0,255), (c*90+55, r*90+55, 80, 80))

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
        
        #main diagonal
        diagonal = np.diag(self.board, k=col - row)
        if diagonal.size >= 4:
            diagonal_Subsets = np.lib.stride_tricks.sliding_window_view(diagonal, window_shape = 4)
        #anti diagonal
        anti_diagonal = np.diag(np.fliplr(self.board), k=(cols - 1) - (col + row))
        if anti_diagonal.size >= 4:
            anti_Subsets = np.lib.stride_tricks.sliding_window_view(anti_diagonal, window_shape = 4)

        bool_main = True in np.all(diagonal_Subsets == Win, axis=1)
        bool_anti = True in np.all(anti_Subsets == Win, axis=1)
        if bool_main or bool_anti:
            return True
               
        return False
    
    def board_full(self):
        # To check if game is over
        return 0 not in self.board

    #Main Loop
    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        global screen
        screen = pygame.display.set_mode((800,700))
        pygame.display.set_caption('Connect FOUR')
        self.draw(screen)
        running = True

        while running:

            #To quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                #User inputs
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    col = (mouse_pos[0] - 50)//90
                    if col > 6 or col < 0:
                        continue
                    player = 1 if self.turn == 0 else 2
                    row = self.drop(col,player)
                    if row is not None:
                        if self.check_win(player, col, row):
                            #if Winner found:
                            self.draw(screen)
                            winner = self.current_player()
                            font = pygame.font.Font(None, 50)
                            text = font.render(f"{winner} wins", True, ((255,0,0) if player == 1 else (0,0,255)))

                            screen.blit(text, (250, 600))
                            pygame.display.update()
                            pygame.time.wait(3000)
                            return winner
                        
                        #move on with next move
                        self.switch_turn()
                    if self.board_full():

                        #Board full but no winner...
                        self.draw(screen)
                        text_font = pygame.font.Font(None, 50)
                        tie_text = text_font.render("Match tied", True, (0, 0, 0))
                        screen.blit(tie_text, (250, 600))
                        pygame.display.update()
                        pygame.time.wait(3000)
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
