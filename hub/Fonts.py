import pygame as pg
def get_font(size,style = None):
    if style == 'Arcade':
        return pg.font.Font('games/game_resources/ArcadeGamer.ttf', size)
    if style == 'Nice':
        return pg.font.Font('games/game_resources/niceFont.ttf', size)
    else:
        return pg.font.Font(None,size) 



