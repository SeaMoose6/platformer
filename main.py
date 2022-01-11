import pygame as pg
import sprites
from sprites import Player
from settings import *

pg.init()

bg_image = pg.image.load("assets/centaur_bridge.png")
bg_image = pg.transform.scale(bg_image, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

# Set Base Screen
screen = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pg.display.set_caption("Gunner Game")

playing = True

hero = sprites.SpriteSheet("assets/xeonsheet.bmp")
villain = sprites.SpriteSheet("assets/xeonsheetsupah_0.bmp")

player_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

#
# shooting_hero = hero.image_at((535, 160, 100, 80), -1)
# shooting_villain = villain.image_at((535, 160, 100, 80), -1)
# standing_hero = hero.image_at((0, 0, 100, 80), -1)


player = Player(hero)
player_group.add(player)
all_sprites.add(player)

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

   #screen.blit(villain_run[0], (100, 100))

   #screen.blit(standing_hero, (100, 100))
   #screen.blit(standing_villain, (200, 100))

   #screen.blit(player, (200, 200))
   player_group.draw(screen)
   all_sprites.update()

   pg.display.flip()

pg.quit()
