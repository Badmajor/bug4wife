import pygame as pg

GAME_OVER_TYPE = pg.USEREVENT + 1
GAME_OVER = pg.event.Event(GAME_OVER_TYPE, message="Game Over Triggered!")
