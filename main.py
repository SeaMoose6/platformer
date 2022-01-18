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
platform = pg.image.load("assets/steelstrip.png")
big_platform = pg.transform.scale(platform, (750, 100))
platform = pg.transform.scale(platform, (300, 50))

player_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# standing_hero = hero.image_at((0, 0, 100, 80), -1)
# shooting_hero = hero.image_at((535, 160, 100, 80), -1)
# shooting_villain = villain.image_at((535, 160, 100, 80), -1)

player = Player(hero, 0, 0, 70, 80)
player_group.add(player)
all_sprites.add(player)

big_platform = Platform(big_platform, 700, 750)
platform_one = Platform(platform, 300, 500)
platform_two = Platform(platform, 1100, 500)
platform_group.add(platform_one)
platform_group.add(platform_two)
platform_group.add(big_platform)
all_sprites.add(big_platform)
all_sprites.add(platform_one)
all_sprites.add(platform_two)

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
   player_group.draw(screen)
   #platform_group.draw(screen)
   all_sprites.update()



   pg.display.flip()

pg.quit()
