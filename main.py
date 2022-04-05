import pygame as pg
import pygame.sprite

import sprites
from sprites import Player, Platform, Weapons, Explosion, Enemy
from settings import *

pg.init()
SCORE = 0

def start_screen():
    bg_image = pg.image.load("assets/oie_18154314jgX7zpnN.jpg")
    bg_image = pg.transform.scale(bg_image, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Space Pirates")

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    running = False

        screen.blit(bg_image, (0, 0))

        start_text = BIG_FONT.render("SPACE", True, BLACK)
        start_text_2 = BIG_FONT.render("PIRATES", True, BLACK)
        start_text_3 = FONT.render("press \"p\" to start", True, WHITE)
        screen.blit(start_text, (240, 400))
        screen.blit(start_text_2, (640, 400))
        screen.blit(start_text_3, (550, 700))

        pygame.display.flip()

        clock.tick(FPS)


def game_over():
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Space Pirates")

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    running = False

        screen.fill(BLACK)
        text = BIG_FONT.render(f"GAME OVER", True, RED)
        text_2 = FONT.render(f"Score:{SCORE}", True, WHITE)
        screen.blit(text, (300, 400))
        screen.blit(text_2, (560, 600))

        start_text_3 = FONT.render("press \"p\" to play again", True, WHITE)
        screen.blit(start_text_3, (500, 700))

        pygame.display.flip()
        clock.tick(FPS)
def play():

    global SCORE
    global switching_level

    bg_image = pg.image.load("assets/sci_fi_bg1.jpg")
    bg_image = pg.transform.scale(bg_image, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
    if switching_level:
        bg_image = pg.image.load("assets/rocky-nowater-demo.png")
        bg_image = pg.transform.scale(bg_image, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

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

    unlocked = False
    level_count = 0
    if switching_level:
        level_count = 1
    def set_layout(levels):
        level = sprites.Level(enemies, levels[level_count])
        return level

    layout = set_layout(levels)

    tile_list = layout.get_physical_tiles()
    bg_tile_list = layout.get_bg_tiles()
    key_tiles = layout.get_keys()
    enemy_list = layout.get_enemy_list()
    player = Player(hero, 100, 850, 50, tile_list, bg_tile_list, key_tiles)
    player_group.add(player)
    print(player)
    enemy = Enemy(enemies, 50, tile_list, bg_tile_list, screen, enemy_list)
    enemy_group.add(enemy)

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
                    playing = False
                if event.key == pg.K_e:
                    shooting = True
                    x = player.get_info()[0]
                    y = player.get_info()[1]
                    laser = Weapons(hero, x, y, screen, tile_list)
                    missile_group.add(laser)
                    print(laser)
                if event.key == pg.K_r:
                    bombing = True
                    x = player.get_info()[0]
                    y = player.get_info()[1]
                    bomb = Weapons(hero, x, y, screen, tile_list)
                    bomb_group.add(bomb)

        screen.blit(bg_image, (0, 0))
        layout.update(screen, unlocked, player.get_info())
        player.update(screen)
        info = player.get_info()
        enemies = enemy.get_enemies()[0]
        keys = enemy.get_enemies()[1]
        enemy.update(info)

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
                elif tile[1].colliderect(laser.rect.x,
                                         laser.rect.y,
                                         laser.rect.width,
                                         laser.rect.height):
                    laser.kill()
            for enemie in enemies:
                if enemie[1].colliderect(laser.rect.x,
                                         laser.rect.y,
                                         laser.rect.width,
                                         laser.rect.height):
                    explosion = Explosion(explosion_sheet, enemie[1].center)
                    laser.kill()
                    big_explosion_group.add(explosion)
                    enemie[1].y += 5000
                    SCORE += 1
            for key in keys:
                if key[1].colliderect(laser.rect.x,
                                         laser.rect.y,
                                         laser.rect.width,
                                         laser.rect.height):
                    explosion = Explosion(explosion_sheet, key[1].center)
                    laser.kill()
                    big_explosion_group.add(explosion)
                    key[1].y += 5000
                    SCORE += 1
                    unlocked = True
                    #layout.unlock(screen)

        for enemie in enemies:
            if enemie[1].colliderect(player.image_rect.x,
                                     player.image_rect.y,
                                     player.image_rect.width,
                                     player.image_rect.height):
                player.image_rect.y += 5000
                playing = False

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
                elif tile[1].colliderect(bomb.bomb_rect.x,
                                       bomb.bomb_rect.y,
                                       bomb.bomb_rect.width,
                                       bomb.bomb_rect.height):
                    explosion = Explosion(explosion_sheet, bomb.bomb_rect.center)
                    bomb.kill()
                    explosion_group.add(explosion)
            for enemie in enemies:
                if enemie[1].colliderect(bomb.bomb_rect.x,
                                         bomb.bomb_rect.y,
                                         bomb.bomb_rect.width,
                                         bomb.bomb_rect.height):
                    explosion = Explosion(explosion_sheet, enemie[1].center)
                    bomb.kill()
                    big_explosion_group.add(explosion)
                    enemie[1].y += 5000

        for key in layout.get_keys():
            if key[1].colliderect(player.image_rect.x,
                                     player.image_rect.y,
                                     player.image_rect.width,
                                     player.image_rect.height):
                level_count = 1
                switching_level = True

                playing = False

        explosion_group.draw(screen)
        big_explosion_group.draw(screen)
        explosion_group.update(1)
        big_explosion_group.update(2)
        pg.display.flip()

        clock.tick(FPS)



start_screen()

if switching_level:
    play()
while True:
    play()
    game_over()


pg.quit()
