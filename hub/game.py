#import required modules
import sys
import pygame as pg
import subprocess
import numpy as np
import os
import csv
from datetime import date
import matplotlib
import matplotlib.pyplot as plt
from Fonts import get_font
pg.init()

#global variables
height, width = 720, 1280
screen = pg.display.set_mode((width, height))

def record_result(winner,loser,game_name): #result appended to history.csv
    file_exist_bool = os.path.isfile('history.csv') and os.path.getsize('history.csv') > 0
    today = date.today()
    with open('history.csv','a',newline="") as file:
        csv_writer = csv.writer(file)
        if not file_exist_bool:
            header = ['Winner','Loser','Date','Game']
            csv_writer.writerow(header)
        csv_writer.writerow([winner,loser,today,game_name])
def post_game_options(screen): # Game over now main menu or quit
    title = get_font(42,'Nice').render('Game over...',True,(255,255,255))
    title_rect = title.get_rect(center = (width/2,200))
    play_text = get_font(36,'Nice').render('Main menu',True,(100,255,100))
    exit_text = get_font(36,'Nice').render('quit',True,(255,100,100))
    Background = pg.image.load('games/game_resources/leaderboard_background.png')
    options = [play_text,exit_text]
    while True:
        rects=[]
        screen.blit(Background,(0,0))
        screen.blit(title,title_rect)
        mouse_pos = pg.mouse.get_pos()

        for i in range(2):
            rect = pg.Rect(480,270+90*i,320,60)
            color = (100,100,180) if rect.collidepoint(mouse_pos) else (60,60,100) # color changes on hover
            pg.draw.rect(screen,color,rect,border_radius = 12) #border_radius makes button look nice
            screen.blit(options[i],options[i].get_rect(center = rect.center))
            rects.append(rect)
            pg.display.update()
        for event in pg.event.get():
            if event.type ==pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type ==pg.MOUSEBUTTONDOWN:
                if rects[1].collidepoint(event.pos):
                    pg.quit()
                    sys.exit
                if rects[0].collidepoint(event.pos):
                    return


        
        
def show_sort_options(screen): #Leaderboard sorting options shown on GUI
    title = get_font(42,'Nice').render('Sort Leaderboard by',True,(255,255,255))
    title_rect = title.get_rect(center=(width/2,200))
    wins_text = get_font(36,'Nice').render('Sort By Wins',True,(150,255,150))
    losses_text = get_font(36,'Nice').render('Sort By loss',True,(255,150,150))
    ratio_text = get_font(36,'Nice').render('Sort By W/L',True,(150,150,255))
    options_list = [wins_text,losses_text,ratio_text]
    metric_list = ['wins','losses','ratio']
    Leaderboard_Background = pg.image.load('games/game_resources/leaderboard_background.png')
    while True:
        screen.blit(Leaderboard_Background,(0,0))
        screen.blit(title,title_rect)
        mouse_pos = pg.mouse.get_pos()
        rects=[]
        for i in range(3):
            rect = pg.Rect(480,270+90*i,320,60)
            color = (100,100,180) if rect.collidepoint(mouse_pos) else (60,60,100)
            pg.draw.rect(screen,color,rect,border_radius = 12)
            rects.append(rect)
            screen.blit(options_list[i],options_list[i].get_rect(center = rect.center))
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                for i in range(3):
                    if(rects[i].collidepoint(event.pos)):
                        return_text = get_font(28,'Nice').render(f"Leaderboard sorted by {metric_list[i]} shown on terminal",True,"#f5e342")
                        screen.blit(return_text,return_text.get_rect(center = (width/2,550)))
                        pg.display.update()
                        pg.time.wait(1000)
                        return metric_list[i] #Returned value is the metric used to sort and display leaderboard on Terminal
def show_graphs(screen): #calls matplot.py which creates graphs and we display them on screen
    subprocess.run(["python3","matplot.py"])
    top_text = get_font(36,'Arcade').render('STATISTICS',True,(100,255,255))
    exit_text = get_font(32).render("Press any key to continue", True, (255, 155, 155))
    charts = []
    if os.path.isfile('charts/bar.png'):
        bar_chart = pg.image.load('charts/bar.png')
        bar_chart = pg.transform.smoothscale(bar_chart,(560,570))
        charts.append(bar_chart)
    if os.path.isfile('charts/pie.png'):
        pie_chart = pg.image.load('charts/pie.png')
        pie_chart = pg.transform.smoothscale(pie_chart,(560,570))
        charts.append(pie_chart)
    while True:
        background = pg.image.load('games/game_resources/charts.png')
        screen.blit(background,(0,0))
        screen.blit(exit_text, exit_text.get_rect(center=(640,690)))
        screen.blit(top_text,top_text.get_rect(center =(640,50)))
        chart_no = 0
        for chart in charts:
            screen.blit(chart,(60 + 630*chart_no,100))
            chart_no +=1
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                return
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

#the base game class
class Game:

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.mode = sys.argv[3]

        self.player = 1 #current player,1 is for player1 and 2 is for player2
        self.game_over = False
        self.screen = pg.display.set_mode((width,height))
        self.button = pg.image.load('games/game_resources/button.png')
        self.button = pg.transform.scale(self.button,(200,100))
        
        #Current player is always shown on screen 
        self.turn_text = get_font(28,'Nice').render(f"Turn: {self.current_player()}", True, (255,255,255))
        self.turn_rect = self.turn_text.get_rect(center=(640, 140))
        self.draw_offered = False
        
        #Resign
        self.Resign_text = get_font(36,'Arcade').render("RESIGN",True,(255,100,100))
        #offer Draw
        self.OfferDraw_text = get_font(36,'Arcade').render("DRAW", True, (100, 255, 100))

        self.Resign1_rect = pg.Rect(50, 300, 200, 100)
        self.Resign2_rect = pg.Rect(1030, 300, 200, 100)
        self.OfferDraw1_rect = pg.Rect(50, 400, 200, 100)
        self.OfferDraw2_rect = pg.Rect(1030, 400, 200, 100)
    def switch_turn(self):
        self.player = 3 - self.player     # switches between 1 and 2
        self.turn_text = get_font(28,'Nice').render(f"Turn: {self.current_player()}", True, (255,255,255))
    def current_player(self):
        return "Draw" if self.player == 0 else self.player1 if self.player == 1 else self.player2
    def game_board(self,rows,cols): #initial empty board
        self.board = np.zeros((rows,cols), dtype=int)
        return self.board
    def reset(self): #reset board on R key
        self.board.fill(0)
        self.player=2
        self.switch_turn()
        self.game_over=False
    def board_full(self):
        #check if board is full
        return 0 not in self.board
    
    def make_board(self,background,board_photo,x,y): #make initial buttons and board for gameplay
        
        self.screen.blit(background, (0,0))
        self.screen.blit(board_photo, (x, y))
        self.screen.blit(self.button,(50,40))
        self.screen.blit(self.button,(1030,40))
        self.screen.blit(self.button, (50,300))
        self.screen.blit(self.button, (1030,300))
        self.screen.blit(self.button, (50,400))
        self.screen.blit(self.button, (1030,400))
        self.screen.blit(self.OfferDraw_text, center:=(80,430))
        self.screen.blit(self.OfferDraw_text,center:=(1080,430))
        self.screen.blit(self.Resign_text, center:=(60,330))
        self.screen.blit(self.Resign_text, center:=(1040,330))
        if not self.draw_offered and not self.game_over:
            self.screen.blit(self.turn_text, self.turn_rect) 

        player1_text = get_font(28,'Nice').render(f"{self.player1}", True, (255,0,0))
        self.screen.blit(player1_text, (center:=(80,70)))
        player2_text = get_font(28,'Nice').render(f"{self.player2}", True, (255,255,0))
        self.screen.blit(player2_text, (center:=(1080, 70)))
    
    def Resign(self,player):
        self.game_over = True
        return self.player1 if player == 2 else self.player2   # other player wins
    def show_text(self,text,pos):
        
        #show text in GUI
        self.screen.blit(text, pos)
        pg.display.update()
        pg.time.wait(1000)
        
    def Offer_Draw(self,player):
        self.draw_offered = True
        self.draw()
        opponent =  self.player2 if player == self.player1 else self.player1
        offer_text = get_font(20,'Nice').render(f"{opponent}, {player} offers draw [Y/N]", True, (255,255,255))
        self.screen.blit(offer_text, (420,135))
        pg.display.update()
        while True:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_y:  # Accept draw offer
                        return "Draw"
                    elif event.key == pg.K_n:  # Reject draw offer
                        self.draw_offered = False
                        return None
    def check_buttons_press(self, mouse_pos):
        if(self.Resign1_rect.collidepoint(mouse_pos)):
            self.game_over = True
            winner = self.player2  # player1 resigned 2 wins 
            text = get_font(36,'Nice').render(f"{winner} wins", True, (255,255,0))
            self.show_text(text,(520,670))
            return self.Resign(1)
        if(self.Resign2_rect.collidepoint(mouse_pos)):
            self.game_over = True
            winner = self.player1  # player2 resigned 1 wins
            text = get_font(36,'Nice').render(f"{winner} wins", True, (255,0,0))
            self.show_text(text,(520,670))
            return self.Resign(2)
        if(self.OfferDraw1_rect.collidepoint(mouse_pos)): #Draw offer is shown on screen as text

            result = self.Offer_Draw(self.player1)
            if result is not None:
                self.game_over = True
                tie_text = get_font(36,'Arcade').render("Match tied", True, (255,255,255))
                self.show_text(tie_text,(520,670))
                return "Draw"
        if(self.OfferDraw2_rect.collidepoint(mouse_pos)): #Draw offer is shown on screen as text
            result = self.Offer_Draw(self.player2)
            if result == "Draw":
                self.game_over = True
                tie_text = get_font(36,'Arcade').render("Match tied", True, (255,255,255))
                self.show_text(tie_text,(520,670))
                return "Draw"
    def check_win(self): #will be different for each game so base games will overwrite it.
        raise NotImplementedError("Must be implemented by subclasses")
#stats button
Stats_text = get_font(46,'Nice').render("STATS",True,(100,200,200))
Stats_rect = Stats_text.get_rect(center = (1080,110))

#Leaderboard button
Leaderboard_text = get_font(32,'Nice').render("Leaderboard",True,(100,200,200))
Leaderboard_rect = Leaderboard_text.get_rect(center = (200,110))

def main():
    pg.init()
    #Storing player names from CLI
    player1 = sys.argv[1]
    player2 = sys.argv[2]
    mode = sys.argv[3]
    bg = pg.image.load("games/game_resources/bg.png").convert_alpha()
    bg= pg.transform.scale(bg, (width, height))

    #multiple slides create animation effect
    slide1= pg.image.load("games/game_resources/slide1.png").convert_alpha()
    slide1= pg.transform.scale(slide1, (width, height))
    slide2= pg.image.load("games/game_resources/slide2.png").convert_alpha()
    slide2= pg.transform.scale(slide2, (width, height))
    slide3= pg.image.load("games/game_resources/slide3.png").convert_alpha()
    slide3= pg.transform.scale(slide3, (width, height))
    slide4= pg.image.load("games/game_resources/slide4.png").convert_alpha()
    slide4= pg.transform.scale(slide4, (width, height))
    slide5= pg.image.load("games/game_resources/slide5.png").convert_alpha()
    slide5= pg.transform.scale(slide5, (width, height))
    slide6= pg.image.load("games/game_resources/slide6.png").convert_alpha()
    slide6= pg.transform.scale(slide6, (width, height))

    #backgroundon main menu
    bg4 = pg.image.load("games/game_resources/bg4.png").convert_alpha()
    bg4= pg.transform.scale(bg4, (width, height))
    bg1=pg.image.load("games/game_resources/bg1.png")
    bg1= pg.transform.scale(bg1, (width, height))
    bg2=pg.image.load("games/game_resources/bg2.png")
    bg2= pg.transform.scale(bg2, (width, height))
    bg3=pg.image.load("games/game_resources/bg3.png")
    bg3= pg.transform.scale(bg3, (width, height))

    #tictactoe option
    ttt = pg.image.load("games/game_resources/ttt.png").convert_alpha()
    ttt.set_colorkey((255,255,255))
    ttt_rect = ttt.get_rect(midbottom=(1010, 660))
    #othello option
    othello = pg.image.load("games/game_resources/othello.png").convert_alpha()
    othello.set_colorkey((255,255,255))
    othello_rect = othello.get_rect(midbottom=(615, 660))
    #connect4 option
    connect4 = pg.image.load("games/game_resources/Connect4.png").convert_alpha()
    connect4.set_colorkey((255,255,255))
    connect4_rect = connect4.get_rect(midbottom=(220, 660))

    pg.display.set_caption("MINI Game Hub")
    clock = pg.time.Clock()
    running = True
    frames = 0

    #main loop
    while running:
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                winner = None    # reset har click pe
                game_name = None
                if Leaderboard_rect.collidepoint(mouse_pos): #leaderboard button functioning
                    metric = show_sort_options(screen) 
                    subprocess.run(["bash","leaderboard.sh",metric])                   
                if Stats_rect.collidepoint(mouse_pos): #stats button functioning
                    show_graphs(screen)

                #click on games to start them
                if ttt_rect.collidepoint(mouse_pos):
                    result = subprocess.run(["python3", "games/tictactoe.py", player1, player2,mode], capture_output=True, text=True)
                    print(result.stderr)
                    winner = result.stdout.splitlines()[-1]
                    game_name = "TicTacToe"
                elif othello_rect.collidepoint(mouse_pos):
                    result = subprocess.run(["python3", "games/othello.py", player1, player2,mode], capture_output=True, text=True)
                    print(result.stderr)
                    winner = result.stdout.splitlines()[-1]
                    game_name = "Othello"
                elif connect4_rect.collidepoint(mouse_pos):
                    result = subprocess.run(["python3", "games/connect4.py", player1, player2,mode], capture_output=True, text=True)
                    print(result.stderr)
                    winner = result.stdout.splitlines()[-1]
                    game_name = "Connect4"

                if winner is not None and game_name is not None:
                    if winner == "Draw":
                        loser = "Draw"
                    else:
                        loser = player2 if winner == player1 else player1 
                    record_result(winner, loser, game_name)
                    metric = show_sort_options(screen)
                    subprocess.run(["bash","leaderboard.sh",metric]) #leaderboard displayed on terminal after game ends
                    show_graphs(screen) #graphs shown on GUI
                    post_game_options(screen) #post game menu

        #background display
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
            #for animation effect backgrounds are alternated
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
                    # Inflate by 30 pixels in width and height on hover
                    disp_ttt = ttt_rect.inflate(30, 30)
                    img_ttt = pg.transform.smoothscale(ttt, disp_ttt.size)
                else:
                    disp_ttt = ttt_rect
                    img_ttt = ttt
                screen.blit(img_ttt, disp_ttt)

                # Othello Hover Logic
                if othello_rect.collidepoint(mouse_pos):
                    # Inflate by 30 pixels in width and height on hover
                    disp_othello = othello_rect.inflate(30, 30)
                    img_othello = pg.transform.smoothscale(othello, disp_othello.size)
                else:
                    disp_othello = othello_rect
                    img_othello = othello
                screen.blit(img_othello, disp_othello)

                # Connect 4 Hover Logic
                if connect4_rect.collidepoint(mouse_pos):
                    # Inflate by 30 pixels in width and height on hover
                    disp_c4 = connect4_rect.inflate(30, 30)
                    img_c4 = pg.transform.smoothscale(connect4, disp_c4.size)
                else:
                    disp_c4 = connect4_rect
                    img_c4 = connect4
                screen.blit(img_c4, disp_c4)
        button = pg.image.load('games/game_resources/button.png')
        screen.blit(button,(50,50))
        screen.blit(button,(930,50))
        screen.blit(Stats_text,Stats_rect)
        screen.blit(Leaderboard_text,Leaderboard_rect)
        
        pg.display.update()
        clock.tick(60)
if __name__ == "__main__":
    main()
