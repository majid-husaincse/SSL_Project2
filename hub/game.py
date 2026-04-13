import sys
import pygame
import subprocess
import numpy as np

#Defining the base game class
class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

        self.player = 1 #current player, 1 is for player1 and 2 is for player2

        self.game_over=False
    def switch_turn(self):
        self.player = 3 - self.player     # switches between 1 and 2

    def current_player(self):
        return self.player1 if self.player == 1 else self.player2
    
    def reset(self): #to reset the board on R key
        self.board.fill(0)
        self.player = 1
        self.game_over=False
    def board_full(self):
        # To check if game is over
        return 0 not in self.board
    
    def Resign(self,player):
        self.game_over = True
        return self.player1 if player == 2 else self.player2   # other player
    def check_win(self):
        raise 
def main():
    pygame.init()
    #Storing player names
    player1 = sys.argv[1]
    player2 = sys.argv[2]

    screen = pygame.display.set_mode((800, 600))
    text_font = pygame.font.Font(None, 50)
    Games = text_font.render("Select a Game:", True, (0, 0, 0))
    Game1 = text_font.render("1. Tic Tac Toe", True, (255,0,0), (200,200,200))
    Game2 = text_font.render("2. Othello", True, (0,255,0), (200,200,200))
    Game3 = text_font.render("3. Connect 4", True, (0,0,255), (200,200,200))
    Game1_rect = Game1.get_rect(topleft=(250, 150))
    Game2_rect = Game2.get_rect(topleft=(250, 250))
    Game3_rect = Game3.get_rect(topleft=(250, 350))
    pygame.display.set_caption("MINI Game Hub")
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if Game1_rect.collidepoint(mouse_pos):
                    subprocess.run(["python3", "games/tictactoe.py", player1, player2])
                elif Game2_rect.collidepoint(mouse_pos):
                    subprocess.run(["python3", "games/othello.py", player1, player2])
                elif Game3_rect.collidepoint(mouse_pos):
                    subprocess.run(["python3", "games/connect4.py", player1, player2])
        screen.fill((255, 255, 255))
        screen.blit(Game1,Game1_rect)
        screen.blit(Game2, Game2_rect)
        screen.blit(Game3, Game3_rect)
        screen.blit(Games, (250, 50))
        mouse_pos = pygame.mouse.get_pos()
        pygame.display.update()
        clock.tick(60)
if __name__ == "__main__":
    main()