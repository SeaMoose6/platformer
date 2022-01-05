import pygame as pg
import sprites
from settings import *

pg.init()

# Set Base Screen
screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pg.display.set_caption("Card Game")

playing = True

#bg_image = pg.image.load("assets/deck_of_cards - Copy.png")

card = sprites.SpriteSheet("assets/deck_of_cards - Copy.png")
hero = sprites.SpriteSheet("assets/xeonsheetsupah_0.bmp")
villain = sprites.SpriteSheet("assets/xeonsheet.bmp")
x_margin = 11
y_margin = 2
x_pad = 22
y_pad = 4

standing_hero = hero.image_at((425, 85, 416, 70), -1)
standing_villain = villain.image_at((0, 0, 70, 80), -1)
ace_hearts = card.image_at((9, 2, 44, 59))
print(standing_hero)

card_list = card.load_grid_images(4, 14, x_margin, x_pad, y_margin, y_pad)

clock = pg.time.Clock()

while playing:

   clock.tick(FPS)

   for event in pg.event.get():
       if event.type == pg.QUIT:
           playing = False
       if event.type == pg.KEYDOWN:    # allow for q key to quit the game
           if event.key == pg.K_q:
               playing == False

   screen.fill(BLUE)

   screen.blit(standing_hero, (100, 100))
   screen.blit(standing_villain, (150, 100))

   pg.display.flip()

pg.quit()
