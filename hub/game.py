import sys
import pygame
import subprocess
import numpy as np
pygame.init()

height, width = 720, 1280
#Defining the base game class
class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

        self.player = 1 #current player, 1 is for player1 and 2 is for player2

        self.game_over=False
        self.font = pygame.font.Font('games/c4_resources/ArcadeGamer.ttf', 36)
    def switch_turn(self):
        self.player = 3 - self.player     # switches between 1 and 2
    def current_player(self):
        return self.player2 if self.player == 2 else self.player1
    def game_board(self,rows,cols):
        self.board = np.zeros((rows,cols), dtype=int)
        return self.board
    def reset(self): #to reset the board on R key
        self.board.fill(0)
        self.player = 3-self.player
        self.game_over=False
    def board_full(self):
        # To check if game is over
        return 0 not in self.board
    
    def Resign(self,player):
        self.game_over = True
        return self.player1 if player == 2 else self.player2   # other player
    def check_win(self):
        raise NotImplementedError("Must be implemented by subclass")
def main():
    pygame.init()
    #Storing player names
    player1 = sys.argv[1]
    player2 = sys.argv[2]

    screen = pygame.display.set_mode((width, height))
    bg = pygame.image.load("games/game_resources/bg.png").convert_alpha()
    bg= pygame.transform.scale(bg, (width, height))
    slide1= pygame.image.load("games/game_resources/slide1.png").convert_alpha()
    slide1= pygame.transform.scale(slide1, (width, height))
    slide2= pygame.image.load("games/game_resources/slide2.png").convert_alpha()
    slide2= pygame.transform.scale(slide2, (width, height))
    slide3= pygame.image.load("games/game_resources/slide3.png").convert_alpha()
    slide3= pygame.transform.scale(slide3, (width, height))
    slide4= pygame.image.load("games/game_resources/slide4.png").convert_alpha()
    slide4= pygame.transform.scale(slide4, (width, height))
    slide5= pygame.image.load("games/game_resources/slide5.png").convert_alpha()
    slide5= pygame.transform.scale(slide5, (width, height))
    slide6= pygame.image.load("games/game_resources/slide6.png").convert_alpha()
    slide6= pygame.transform.scale(slide6, (width, height))
    # bg5 = pygame.image.load("games/game_resources/bg5.png").convert_alpha()
    # bg5= pygame.transform.scale(bg5, (1280, 720))
    bg4 = pygame.image.load("games/game_resources/bg4.png").convert_alpha()
    bg4= pygame.transform.scale(bg4, (width, height))
    bg1=pygame.image.load("games/game_resources/bg1.png")
    bg1= pygame.transform.scale(bg1, (width, height))
    bg2=pygame.image.load("games/game_resources/bg2.png")
    bg2= pygame.transform.scale(bg2, (width, height))
    bg3=pygame.image.load("games/game_resources/bg3.png")
    bg3= pygame.transform.scale(bg3, (width, height))
    text_font = pygame.font.Font(None, 50)
    ttt = pygame.image.load("games/game_resources/ttt.png").convert_alpha()
    ttt.set_colorkey((255,255,255))
    ttt_rect = ttt.get_rect(midbottom=(1010, 660))
    othello = pygame.image.load("games/game_resources/othello.png").convert_alpha()
    othello.set_colorkey((255,255,255))
    othello_rect = othello.get_rect(midbottom=(615, 660))

    connect4 = pygame.image.load("games/game_resources/Connect4.png").convert_alpha()
    connect4.set_colorkey((255,255,255))
    connect4_rect = connect4.get_rect(midbottom=(220, 660))

    pygame.display.set_caption("MINI Game Hub")
    clock = pygame.time.Clock()
    running = True
    frames = 0
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if ttt_rect.collidepoint(mouse_pos):
                    subprocess.run(["python3", "games/tictactoe.py", player1, player2])
                elif othello_rect.collidepoint(mouse_pos):
                    subprocess.run(["python3", "games/othello.py", player1, player2])
                elif connect4_rect.collidepoint(mouse_pos):
                    subprocess.run(["python3", "games/connect4.py", player1, player2])
        frames+=1
        time = 20
        if frames<time:
            screen.blit(bg, (0, 0))
        elif frames<2*time:
            screen.blit(bg1, (0, 0))
        elif frames<3*time:
            screen.blit(bg2, (0, 0))
        elif frames<4*time:
            screen.blit(bg3, (0, 0))
        elif frames<5*time:
            screen.blit(bg4, (0, 0))
        else:
            rem = frames%80
            if rem <10 or rem > 70:
                screen.blit(slide4, (0, 0))
            elif rem < 20 or rem > 60:
                screen.blit(slide3, (0, 0))
            elif rem < 30 or rem > 75:
                screen.blit(slide2, (0, 0))
            else:
                screen.blit(slide1, (0, 0))
            if frames>6*time:
            # Tic Tac Toe Hover Logic
                if ttt_rect.collidepoint(mouse_pos):
                    # Inflate by 20 pixels in width and height
                    disp_ttt = ttt_rect.inflate(30, 30)
                    img_ttt = pygame.transform.smoothscale(ttt, disp_ttt.size)
                else:
                    disp_ttt = ttt_rect
                    img_ttt = ttt
                screen.blit(img_ttt, disp_ttt)

                # Othello Hover Logic
                if othello_rect.collidepoint(mouse_pos):
                    disp_othello = othello_rect.inflate(30, 30)
                    img_othello = pygame.transform.smoothscale(othello, disp_othello.size)
                else:
                    disp_othello = othello_rect
                    img_othello = othello
                screen.blit(img_othello, disp_othello)

                # Connect 4 Hover Logic
                if connect4_rect.collidepoint(mouse_pos):
                    disp_c4 = connect4_rect.inflate(30, 30)
                    img_c4 = pygame.transform.smoothscale(connect4, disp_c4.size)
                else:
                    disp_c4 = connect4_rect
                    img_c4 = connect4
                screen.blit(img_c4, disp_c4)
        
        pygame.display.update()
        clock.tick(60)
if __name__ == "__main__":
    main()
