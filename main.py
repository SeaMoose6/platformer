import pygame as pg
import sprites
from sprites import Player, Platform
from settings import *

pg.init()

#bg_image = pg.image.load("assets/centaur_bridge.png")
bg_image = pg.image.load("assets/oie_18154314jgX7zpnN.jpg")
bg_image = pg.transform.scale(bg_image, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

# Set Base Screen
screen = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pg.display.set_caption("Gunner Game")

playing = True

hero = sprites.SpriteSheet("assets/xeonsheet.bmp")
villain = sprites.SpriteSheet("assets/xeonsheetsupah_0.bmp")

player_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


# standing_hero = (0, 0, 70, 80)
# shooting_hero = (535, 160, 100, 80)
# shooting_villain = (535, 160, 100, 80)
player = Player(hero)
player_group.add(player)
all_sprites.add(player)


layout = sprites.Level()

clock = pg.time.Clock()

while playing:

   clock.tick(FPS)

   for event in pg.event.get():
       if event.type == pg.QUIT:
           playing = False
       if event.type == pg.KEYDOWN:
           if event.key == pg.K_q:
               playing == False

   screen.blit(bg_image, (0, 0))
   layout.update(screen)

   player.update(screen)




   pg.display.flip()

pg.quit()
