import pygame as pg
import sprites
from sprites import Player, Platform, Weapons
from settings import *

pg.init()

#bg_image = pg.image.load("assets/centaur_bridge.png")
#bg_image = pg.image.load("assets/oie_18154314jgX7zpnN.jpg")
bg_image = pg.image.load("assets/sci_fi_bg1.jpg")
bg_image = pg.transform.scale(bg_image, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

# Set Base Screen
screen = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pg.display.set_caption("Gunner Game")

playing = True

hero = sprites.SpriteSheet("assets/xeonsheet.bmp")
villain = sprites.SpriteSheet("assets/xeonsheetsupah_0.bmp")

player_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
missile_group = pygame.sprite.Group()


# standing_hero = (0, 0, 70, 80)
# shooting_hero = (535, 160, 100, 80)
# shooting_villain = (535, 160, 100, 80)
layout = sprites.Level()
tile_list = layout.get_physical_tiles()
bg_tile_list = layout.get_bg_tiles()
print(tile_list)
player = Player(hero, 100, 850, 50, tile_list, bg_tile_list)
player_group.add(player)



shooting = False

clock = pg.time.Clock()

while playing:

    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            playing = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                playing == False
            if event.key == pg.K_e:
                shooting = True
                x = player.get_info()[0]
                y = player.get_info()[1]
                laser = Weapons(hero, x, y, screen, tile_list)
                missile_group.add(laser)
                #laser.update(player.right, player.left)


    screen.blit(bg_image, (0, 0))
    layout.update(screen)

    # x = player.get_info()[0]
    # y = player.get_info()[1]
    # laser = Weapons(hero, x, y, screen)
    if shooting:
        for laser in missile_group:
            laser.update(player.right, player.left)
        for tile in tile_list:
            if tile[1].colliderect(laser.rect.x,
                                   laser.rect.y,
                                   laser.rect.width,
                                   laser.rect.height):
                laser.kill()
            if tile[1].colliderect(laser.rect.x,
                                   laser.rect.y,
                                   laser.rect.width,
                                   laser.rect.height):
                laser.kill()
    player.update(screen)
    pg.display.flip()

pg.quit()
