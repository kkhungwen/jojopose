import pygame as pg
import utils
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# 初始化 Pygame
pg.init()

# 获取显示信息
info = pg.display.Info()

SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

WP = pg.image.load(resource_path("images\\wallpaper.jpg"))
WP = utils.scale_image(WP,SCREEN_HEIGHT-80)

BG0 = pg.image.load(resource_path("images\\bg.jpg"))
BG0 = pg.transform.scale(BG0,(SCREEN_WIDTH,SCREEN_HEIGHT))
BG1 = pg.image.load(resource_path("images\\bg1.jpg"))
BG1 = pg.transform.scale(BG1,(SCREEN_WIDTH,SCREEN_HEIGHT))
BG2 = pg.image.load(resource_path("images\\bg2.jpg"))
BG2 = pg.transform.scale(BG2,(SCREEN_WIDTH,SCREEN_HEIGHT))
BG3 = pg.image.load(resource_path("images\\bg3.jpg"))
BG3 = pg.transform.scale(BG3,(SCREEN_WIDTH,SCREEN_HEIGHT))
BG4 = pg.image.load(resource_path("images\\bg4.jpg"))
BG4 = pg.transform.scale(BG4,(SCREEN_WIDTH,SCREEN_HEIGHT))
BG6 = pg.image.load(resource_path("images\\bg6.jpg"))
BG6 = pg.transform.scale(BG6,(SCREEN_WIDTH,SCREEN_HEIGHT))
BG7 = pg.image.load(resource_path("images\\bg7.jpg"))
BG7 = pg.transform.scale(BG7,(SCREEN_WIDTH,SCREEN_HEIGHT))


JO1 = pg.image.load(resource_path("images\\jo1-removebg-preview.png"))
JO2 = pg.image.load(resource_path("images\\jo2-removebg-preview.png"))
JO3 = pg.image.load(resource_path("images\\jo3-removebg-preview.png"))
JO4 = pg.image.load(resource_path("images\\jo4-removebg-preview.png"))
JO5 = pg.image.load(resource_path("images\\jo5-removebg-preview.png"))


DONDONDON = pg.image.load(resource_path("images\\dondondon-removebg.png"))


LINE_EFFECT_0 = pg.image.load(resource_path("images\\bound1-removebg.png"))
LINE_EFFECT_0 = pg.transform.scale(LINE_EFFECT_0,(SCREEN_WIDTH,SCREEN_HEIGHT))
LINE_EFFECT_1 = pg.image.load(resource_path("images\\bound2-removebg.png"))
LINE_EFFECT_1 = pg.transform.scale(LINE_EFFECT_1,(SCREEN_WIDTH,SCREEN_HEIGHT))