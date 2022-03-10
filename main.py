import pygame as pg
import pygame.sprite

import sprites
from sprites import Player, Platform, Weapons, Explosion, Enemy
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
explosion_sheet = sprites.SpriteSheet("assets/explosion.png")
enemies = sprites.SpriteSheet("assets/ScifiCritters4 - Copy.PNG")
print(enemies)

player_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
missile_group = pygame.sprite.Group()
bomb_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
big_explosion_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()


# standing_hero = (0, 0, 70, 80)
# shooting_hero = (535, 160, 100, 80)
# shooting_villain = (535, 160, 100, 80)
layout = sprites.Level(enemies)
tile_list = layout.get_physical_tiles()
bg_tile_list = layout.get_bg_tiles()
enemy_list = layout.get_enemy_list()
print(enemy_list)
player = Player(hero, 100, 850, 50, tile_list, bg_tile_list)
player_group.add(player)
enemy = Enemy(enemies, 50, tile_list, bg_tile_list, screen, enemy_list)
print(enemy)



shooting = False
bombing = False

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
            if event.key == pg.K_r:
                bombing = True
                x = player.get_info()[0]
                y = player.get_info()[1]
                bomb = Weapons(hero, x, y, screen, tile_list)
                bomb_group.add(bomb)

    enemy_group.add(enemy)
    screen.blit(bg_image, (0, 0))
    layout.update(screen)
    player.update(screen)
    info = player.get_info()
    enemy.update(info)
    enemies = enemy.get_enemies()
    #print(enemy_group, missile_group)

    if shooting:
        for laser in missile_group:
            laser.laser_update(player.right, player.left)
    for laser in missile_group:
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
        for enemie in enemies:
            if enemie[1].colliderect(laser.rect.x,
                                   laser.rect.y,
                                   laser.rect.width,
                                   laser.rect.height):
                explosion = Explosion(explosion_sheet, enemy.image_rect.center)
                laser.kill()
                big_explosion_group.add(explosion)

    if bombing:
        for bomb in bomb_group:
            bomb.bomb_update(player.right, player.left)
    for bomb in bomb_group:
        for tile in tile_list:
            if tile[1].colliderect(bomb.bomb_rect.x,
                                   bomb.bomb_rect.y,
                                   bomb.bomb_rect.width,
                                   bomb.bomb_rect.height):
                explosion = Explosion(explosion_sheet, bomb.bomb_rect.center)
                bomb.kill()
                explosion_group.add(explosion)
            if tile[1].colliderect(bomb.bomb_rect.x,
                                   bomb.bomb_rect.y,
                                   bomb.bomb_rect.width,
                                   bomb.bomb_rect.height):
                explosion = Explosion(explosion_sheet, bomb.bomb_rect.center)
                bomb.kill()
                explosion_group.add(explosion)
    #pygame.sprite.groupcollide(missile_group, enemy_group, True, True)
    explosion_group.draw(screen)
    big_explosion_group.draw(screen)
    explosion_group.update(1)
    big_explosion_group.update(2)
    pg.display.flip()

pg.quit()
