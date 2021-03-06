import pygame

from settings import *

import pygame as pg


class SpriteSheet:

    def __init__(self, filename):
        """Load the sheet."""
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)

    def image_at(self, rectangle, colorkey = None):
        """Load a specific image from a specific rectangle."""
        """rectangle is a tuple with (x, y, x+offset, y+offset)"""
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey = None):
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_grid_images(self, num_rows, num_cols, x_margin=0, x_padding=0,
            y_margin=0, y_padding=0, width=None, height=None, colorkey = None):
        """Load a grid of images.
        x_margin is the space between the top of the sheet and top of the first
        row. x_padding is space between rows. Assumes symmetrical padding on
        left and right.  Same reasoning for y. Calls self.images_at() to get a
        list of images.
        """

        sheet_rect = self.sheet.get_rect()
        sheet_width, sheet_height = sheet_rect.size

        if width and height:
            x_sprite_size = width
            y_sprite_size = height
        else:
            x_sprite_size = (sheet_width - 2 * x_margin
                    - (num_cols - 1) * x_padding) / num_cols
            y_sprite_size = (sheet_height - 2 * y_margin
                    - (num_rows - 1) * y_padding) / num_rows

        sprite_rects = []
        for row_num in range(num_rows):
            for col_num in range(num_cols):
                # Position of sprite rect is margin + one sprite size
                #   and one padding size for each row. Same for y.
                x = x_margin + col_num * (x_sprite_size + x_padding)
                y = y_margin + row_num * (y_sprite_size + y_padding)
                sprite_rect = (x, y, x_sprite_size, y_sprite_size)
                sprite_rects.append(sprite_rect)

        return self.images_at(sprite_rects, colorkey)


class Player(pygame.sprite.Sprite):
    def __init__(self, sheet, x, y, tile_size, tile_set, bg_tile_set, key_tiles):
        pygame.sprite.Sprite.__init__(self)
        self.sheet = sheet
        self.tile_size = tile_size
        self.tile_set = tile_set
        self.bg_tile_set = bg_tile_set
        self.key_tiles = key_tiles
        self.nothing = self.sheet.image_at((1, 1, 5, 5,), -1)
        self.standing_right = self.sheet.image_at((15, 13, 50, 64), -1)
        self.standing_left = pg.transform.flip(self.standing_right, True, False)
        self.jumping_right = self.sheet.image_at((140, 474, 50, 78), -1)
        self.jumping_left = pg.transform.flip(self.jumping_right, True, False)
        # self.falling_right = self.sheet.image_at((330, 465, 50, 72), -1)
        # self.falling_left = pg.transform.flip(self.falling_right, True, False)
        # self.bomb_right = self.sheet.image_at((535, 160, 100, 80), -1)
        self.shooting_right = sheet.image_at((425, 90, 73, 63), -1)
        self.shooting_left = pg.transform.flip(self.shooting_right, True, False)
        self.bombing_right = sheet.image_at((260, 670, 63, 64), -1)
        self.bombing_left = pg.transform.flip(self.bombing_right, True, False)
        self.run_right = [self.sheet.image_at((23, 174, 51, 65), -1), self.sheet.image_at((106, 175, 51, 65), -1),
                          self.sheet.image_at((182, 175, 51, 65), -1), self.sheet.image_at((257, 175, 51, 65), -1)]
        self.run_left = [pg.transform.flip(player, True, False) for player in self.run_right]
        self.image = self.standing_right
        self.tile_dx = 0
        self.frame = 0
        self.frame_rate = 50
        self.previous_update = pygame.time.get_ticks()
        self.image_delay = 100
        self.velo_y = 0
        self.image_rect = self.image.get_rect()
        self.image_rect.center = DISPLAY_WIDTH//5, DISPLAY_HEIGHT - self.image_rect.height
        self.right = True
        self.left = False
        self.walking = False
        self.jumping = False
        self.falling = False
        self.shooting = False
        self.bombing = True

    def update(self, display):
        self.current = pygame.time.get_ticks()
        dx = 0
        dy = 0
        tile_dx = 0
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        if keys[pygame.K_d]:
            if self.image_rect.x < 1100:
                dx = 15
                self.right = True
                self.left = False
                now = pygame.time.get_ticks()
                if now - self.previous_update >= self.image_delay:
                    self.previous_update = now
                    if self.frame >= len(self.run_right):
                        self.frame = 0
                    self.image = self.run_right[self.frame]
                    self.frame = self.frame + 1
            else:
                tile_dx = -15
                self.right = True
                self.left = False
                self.walking = True
                now = pygame.time.get_ticks()
                if now - self.previous_update >= self.image_delay:
                    self.previous_update = now
                    if self.frame >= len(self.run_right):
                        self.frame = 0
                    self.image = self.run_right[self.frame]
                    self.frame = self.frame + 1

        elif keys[pygame.K_a]:
            if self.image_rect.x > 300:
                dx = -15
                self.right = False
                self.left = True
                now = pygame.time.get_ticks()
                if now - self.previous_update >= self.image_delay:
                    self.previous_update = now
                    if self.frame >= len(self.run_left):
                        self.frame = 0
                    self.image = self.run_left[self.frame]
                    self.frame = self.frame + 1
            else:
                tile_dx = 15
                self.right = False
                self.left = True
                self.walking = True
                now = pygame.time.get_ticks()
                if now - self.previous_update >= self.image_delay:
                    self.previous_update = now
                    if self.frame >= len(self.run_left):
                        self.frame = 0
                    self.image = self.run_left[self.frame]
                    self.frame = self.frame + 1

        else:
            dx = 0
            self.frame = 0
            if self.right:
                self.image = self.standing_right
            elif self.left:
                self.image = self.standing_left
        if keys[pygame.K_SPACE] and not self.jumping and not self.falling:
            self.velo_y = -16
            self.jumping = True
        if not keys[pygame.K_SPACE]:
            self.jumping = False
        self.velo_y += 0.8
        if self.velo_y < 0:
            self.jumping = True
            self.falling = False
        else:
            self.jumping = False
            self.falling = True
        if self.velo_y >= 10:
            self.velo_y = 10
            dy = 5
        if self.jumping and self.right:
            self.image = self.jumping_right
        if self.jumping and self.left:
            self.image = self.jumping_left

        dy += self.velo_y
        for tile in self.tile_set:
            if self.image_rect.colliderect(tile[1].x + tile_dx,
                                           tile[1].y,
                                           tile[1].width,
                                           tile[1].height):
                tile_dx = 0
            if tile[1].colliderect(self.image_rect.x + dx,
                                   self.image_rect.y,
                                   self.image_rect.width,
                                   self.image_rect.height):
                dx = 0
            if tile[1].colliderect(self.image_rect.x,
                                   self.image_rect.y + dy,
                                   self.image_rect.width,
                                   self.image_rect.height):

                if self.jumping:
                    dy = tile[1].bottom - self.image_rect.top
                    self.velo_y = 0
                    self.falling = True
                    self.jumping = False

                elif self.falling:
                    dy = tile[1].top - self.image_rect.bottom
                    self.velo_y = 0
                    self.falling = False
        if keys[pygame.K_e]:
            self.shooting = True
            if self.shooting and self.right:
                self.image = self.nothing
                display.blit(self.shooting_right, (self.image_rect.x, self.image_rect.y + 2))
            if self.shooting and self.left:
                self.image = self.nothing
                display.blit(self.shooting_left, (self.image_rect.x-23, self.image_rect.y+2))
        if keys[pygame.K_r]:
            self.bombing = True
            if self.bombing and self.right:
                self.image = self.bombing_right
            if self.bombing and self.left:
                self.image = self.nothing
                display.blit(self.bombing_left, (self.image_rect.x-12, self.image_rect.y))

        if dx == 0 and tile_dx == 0:
            self.walking = False

        self.image_rect.x += dx
        self.image_rect.y += dy
        #print(tile_dx)
        for tile in self.tile_set:
            tile_rect = tile[1]
            tile_rect.x += tile_dx
        for tile in self.bg_tile_set:
            bg_tile_rect = tile[1]
            bg_tile_rect.x += tile_dx

        if self.image_rect.left <= self.tile_size:
            self.image_rect.left = self.tile_size
        display.blit(self.image, (self.image_rect.x, self.image_rect.y))
        self.tile_dx = tile_dx

    def get_info(self):
        return self.image_rect.x, self.image_rect.y, self.shooting, self.bombing, \
               self.right, self.left, self.walking, self.tile_dx


class Enemy(pygame.sprite.Sprite):
    def __init__(self, sheet, tile_size, tile_set, bg_tile_set, display, enemy_list, enemy_list_2):
        pygame.sprite.Sprite.__init__(self)
        self.sheet = sheet
        self.tile_size = tile_size
        self.tile_set = tile_set
        self.bg_tile_set = bg_tile_set
        self.display = display
        self.bug_alien = self.sheet.image_at((99, 99, 31, 31), -1)
        self.bug_alien_left = pg.transform.scale2x(self.bug_alien)
        self.bug_alien_right = pg.transform.flip(self.bug_alien_left, True, False)
        self.tankbot = self.sheet.image_at((132, 0, 31, 31), -1)
        self.tankbot_right = pg.transform.scale2x(self.tankbot)
        self.tankbot_left = pg.transform.flip(self.tankbot_right, True, False)

        self.enemy_list = enemy_list
        self.image = self.tankbot_right
        self.image_rect = self.enemy_list[0][1]
        self.image_rect_2 = self.enemy_list[1][1]
        self.image_rect_3 = self.enemy_list[2][1]
        self.rectangles = [self.image_rect, self.image_rect_2, self.image_rect_3]

        self.image_2 = self.bug_alien_right
        self.bug_rect = self.enemy_list[3][1]
        self.bug_rect_2 = self.enemy_list[4][1]
        self.bug_rect_3 = self.enemy_list[5][1]
        self.bugs = [self.bug_rect]

        self.enemy_list_2 = enemy_list_2
        self.flying_robot = self.sheet.image_at((132, 99, 31, 31), -1)
        self.flying_robot_right = pg.transform.scale2x(self.flying_robot)
        self.flying_robot_left = pg.transform.flip(self.flying_robot, True, False)

        self.x_loc = self.image_rect.x
        self.x_loc_2 = self.image_rect_2.x
        self.x_loc_3 = self.image_rect_3.x
        self.right = True
        self.left = False
        self.bug_right = True
        self.bug_left = False
        self.enemies = []
        self.key = []
        self.dx = 0
        self.dy = 3
        self.bug_dx = 10
        self.bug_dy = 3
        self.bot_dx = 5
        self.bot_dy = 5

    def update(self, player_info):
        screen_dx = 0
        self.player_info = player_info
        for rect in self.rectangles:
            for tile in self.tile_set:
                if tile[1].colliderect(rect.x + self.dx,
                                       rect.y,
                                       rect.width,
                                       rect.height):
                    self.dx = 0
                if tile[1].colliderect(rect.x,
                                       rect.y + self.dy,
                                       rect.width,
                                       rect.height):
                    self.dy = tile[1].top - rect.bottom

        for bug in self.bugs:
            for tile in self.tile_set:
                if tile[1].colliderect(bug.x + self.bug_dx,
                                       bug.y,
                                       bug.width,
                                       bug.height):
                    bug_current_collied = pygame.time.get_ticks()
                    if bug_current_collied - bug_previous_collied > BUG_DELAY:
                        pass
                        self.bug_dx *= -1
                if tile[1].colliderect(bug.x,
                                       bug.y + self.bug_dy*10,
                                       bug.width,
                                       bug.height):
                    self.bug_dy = 0

        for enemy in self.enemy_list_2:
            #print(self.enemy_list_2)
            for tile in self.tile_set:
                #print(enemy[0][1], enemy[1])
                if tile[1].colliderect(enemy[0][1].x + enemy[1],
                                       enemy[0][1].y,
                                       enemy[0][1].width,
                                       enemy[0][1].height):
                    enemy[1] *= -1
                    print("collided", enemy[1])
                if tile[1].colliderect(enemy[0][1].x,
                                       enemy[0][1].y + enemy[2],
                                       enemy[0][1].width,
                                       enemy[0][1].height):
                    enemy[2] *= -1
                    print("collided", self.bot_dy)


        if self.right:
            if self.image_rect.x <= self.x_loc+360:
                self.dx = 3
            else:
                self.dx = -3
                self.right = False
                self.left = True
                self.image = self.tankbot_left
        if self.left:
            if self.image_rect.x >= self.x_loc-90:
                self.dx = -3
            else:
                self.dx = 3
                self.right = True
                self.left = False
                self.image = self.tankbot_right
        if self.bug_dx < 0:
            self.bug_left = True
            self.bug_right = False
            self.image_2 = self.bug_alien_left
        elif self.bug_dx > 0:
            self.bug_left = False
            self.bug_right = True
            self.image_2 = self.bug_alien_right

        # if self.player_info[0] < 1100:
        #     pass
        # elif self.player_info[0] > 1100 and self.player_info[6]:
        #     screen_dx = -15
        # if self.player_info[0] > 300:
        #     pass
        # elif self.player_info[0] < 300 and self.player_info[6]:
        #     screen_dx = 15
        screen_dx = player_info[7]
        self.x_loc += screen_dx
        for rect in self.rectangles:
            rect.x += self.dx
            rect.y += self.dy
            rect.x += screen_dx
            self.enemies.append((self.image, rect))
            if rect.y >= 5000:
                pass
            else:
                self.display.blit(self.image, rect)
        for bug in self.bugs:
            bug.x += self.bug_dx
            bug.y += self.bug_dy
            bug.x += screen_dx
            self.key.append((self.image_2, bug))
            if bug.y >= 5000:
                pass
            else:
                self.display.blit(self.image_2, bug)
        for enemy in self.enemy_list_2:
            enemy[0][1].x += screen_dx
            enemy[0][1].x += enemy[1]
            enemy[0][1].y += enemy[2]
            self.display.blit(self.flying_robot_right, enemy[0][1])

    def get_enemies(self):
        return self.enemies, self.key


class Weapons(pygame.sprite.Sprite):
    def __init__(self, sheet, x, y, display, tile_set):
        pygame.sprite.Sprite.__init__(self)
        self.sheet = sheet
        self.x = x
        self.y = y+25
        self.display = display
        self.tile_set = tile_set
        self.velo = 0

        self.laser_right = self.sheet.image_at((322, 694, 44, 18), -1)
        self.laser_left = pg.transform.flip(self.laser_right, True, False)
        self.image = self.sheet.image_at((322, 693, 45, 18), -1)
        self.rect = self.image.get_rect()

        self.bomb_right = self.sheet.image_at((480, 700, 40, 20), -1)
        self.bomb_left = pg.transform.flip(self.bomb_right, True, False)
        self.bomb_image = self.bomb_right
        self.bomb_rect = self.bomb_image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y
        self.bomb_rect.x = self.x
        self.bomb_rect.y = self.y

    def laser_update(self, right, left):
        if right:
            if self.x < self.rect.centerx < self.x+40:
                self.velo = 20
                self.image = self.laser_right
        if left:
            if self.x < self.rect.centerx < self.x + 40:
                self.velo = -20
                self.image = self.laser_left
        self.rect.x += self.velo
        self.display.blit(self.image, (self.rect.x, self.rect.y))

    def bomb_update(self, right, left):
        if right:
            if self.x < self.bomb_rect.centerx < self.x+40:
                self.velo = 6
                self.bomb_image = self.bomb_right
        if left:
            if self.x < self.bomb_rect.centerx < self.x + 40:
                self.velo = -6
                self.bomb_image = self.bomb_left
        self.bomb_rect.x += self.velo
        self.display.blit(self.bomb_image, (self.bomb_rect.x, self.bomb_rect.y))


class Explosion(pygame.sprite.Sprite):
    def __init__(self, sheet, center):
        pygame.sprite.Sprite.__init__(self)
        self.sheet = sheet
        self.EXPLOSION_LIST = [self.sheet.image_at((0, 0, 31, 31), -1), self.sheet.image_at((32, 0, 31, 31), -1),
                               self.sheet.image_at((65, 0, 31, 31), -1), self.sheet.image_at((96, 0, 31, 31), -1),
                               self.sheet.image_at((128, 0, 31, 31), -1), self.sheet.image_at((160, 0, 31, 31), -1)]
        self.new_explosion_list = [pg.transform.scale2x(explosion) for explosion in self.EXPLOSION_LIST]
        self.image = self.EXPLOSION_LIST[0]
        self.image_2 = self.new_explosion_list[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.frame_rate = 50
        self.kill_center = center
        self.previous_update = pygame.time.get_ticks()

    def update(self, num):
        if num == 1:
            current = pygame.time.get_ticks()
            if current - self.previous_update > self.frame_rate:
                self.previous_update = current
                self.frame += 1
            elif self.frame == len(self.EXPLOSION_LIST):
                self.kill()
            else:
                self.image = self.EXPLOSION_LIST[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = self.kill_center
        if num == 2:
            current = pygame.time.get_ticks()
            if current - self.previous_update > self.frame_rate:
                self.previous_update = current
                self.frame += 1
            elif self.frame == len(self.new_explosion_list):
                self.kill()
            else:
                self.image = self.new_explosion_list[self.frame]
                self.rect = self.image_2.get_rect()
                self.rect.center = self.kill_center


class Platform(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        self.change_x = 0


class Level:
    def __init__(self, sheet, layout):
        pygame.sprite.Sprite.__init__(self)
        self.sheet = sheet
        self.layout = layout
        brick_block = pg.image.load("assets/tile116.png")
        brick_block = pg.transform.scale(brick_block, (TILE_SIZE, TILE_SIZE))
        bottom_block = pg.image.load("assets/tile094.png")
        bottom_block = pg.transform.scale(bottom_block, (TILE_SIZE, TILE_SIZE))
        wall_block = pg.image.load("assets/tile095.png")
        wall_block = pg.transform.scale(wall_block, (TILE_SIZE, TILE_SIZE))
        door_block = pg.image.load("assets/door_red.png")
        door_block = pg.transform.scale(door_block, (TILE_SIZE*2, TILE_SIZE*2))
        blue_door = pg.image.load("assets/door_blue.png")
        blue_door = pg.transform.scale(blue_door, (TILE_SIZE * 2, TILE_SIZE * 2))
        blue_brick = pg.image.load("assets/tile065.png")
        blue_brick = pg.transform.scale(blue_brick, (TILE_SIZE, TILE_SIZE))
        blue_bottom = pg.image.load("assets/tile073.png")
        blue_bottom = pg.transform.scale(blue_bottom, (TILE_SIZE, TILE_SIZE))
        blue_bottom2 = pg.image.load("assets/tile074.png")
        blue_bottom2 = pg.transform.scale(blue_bottom2, (TILE_SIZE, TILE_SIZE))
        blue_wall = pg.image.load("assets/tile087.png")
        blue_wall = pg.transform.scale(blue_wall, (TILE_SIZE, TILE_SIZE))
        key_door = pg.image.load("assets/door_surp.png")
        self.key_door = pg.transform.scale(key_door, (TILE_SIZE*2, TILE_SIZE*2))
        key_block = pg.image.load("assets/tile125.png")
        key_block = pg.transform.scale(key_block, (TILE_SIZE, TILE_SIZE))
        desert_floor = pg.image.load("assets/tile089.png")
        desert_floor = pg.transform.scale(desert_floor, (TILE_SIZE, TILE_SIZE))
        desert_tile = pg.image.load("assets/tile106.png")
        desert_tile = pg.transform.scale(desert_tile, (TILE_SIZE, TILE_SIZE))
        desert_block = pg.image.load("assets/tile091.png")
        desert_block = pg.transform.scale(desert_block, (TILE_SIZE, TILE_SIZE))
        sand_block = pg.image.load("assets/tile092.png")
        sand_block = pg.transform.scale(sand_block, (TILE_SIZE, TILE_SIZE))
        self.tankbot = self.sheet.image_at((132, 0, 31, 31), -1)
        self.tankbot_right = pg.transform.scale2x(self.tankbot)
        self.tankbot_left = pg.transform.flip(self.tankbot_right, True, False)
        self.bug_alien = self.sheet.image_at((99, 99, 31, 31), -1)
        self.bug_alien_right = pg.transform.scale2x(self.bug_alien)
        self.bug_alien_left = pg.transform.flip(self.bug_alien_right, True, False)
        self.flying_robot = self.sheet.image_at((132, 99, 31, 31), -1)
        self.flying_robot_right = pg.transform.scale2x(self.flying_robot)
        self.flying_robot_left = pg.transform.flip(self.flying_robot, True, False)
        self.tile_list = []
        self.background_tiles = []
        self.all_tiles = []
        self.enemies = []
        self.key_tiles = []
        self.level_2_enemies = []
        self.exit_x = 0
        self.exit_y = 0

        for i, row in enumerate(self.layout):
            for j, col in enumerate(row):
                x_val = j * TILE_SIZE
                y_val = i * TILE_SIZE

                if col == "1":
                    image_rect = brick_block.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (brick_block, image_rect)
                    self.tile_list.append(tile)
                    self.all_tiles.append(tile)
                if col == "2":
                    image_rect = bottom_block.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (bottom_block, image_rect)
                    self.tile_list.append(tile)
                    self.all_tiles.append(tile)
                if col == "3":
                    image_rect = wall_block.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (wall_block, image_rect)
                    self.tile_list.append(tile)
                    self.all_tiles.append(tile)
                if col == "4":
                    image_rect = door_block.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (door_block, image_rect)
                    self.background_tiles.append(tile)
                    self.all_tiles.append(tile)
                if col == "5":
                    image_rect = blue_door.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (blue_door, image_rect)
                    self.background_tiles.append(tile)
                    self.all_tiles.append(tile)
                if col == "6":
                    image_rect = blue_brick.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (blue_brick, image_rect)
                    self.tile_list.append(tile)
                    self.all_tiles.append(tile)
                if col == "7":
                    image_rect = blue_bottom.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (blue_bottom, image_rect)
                    self.tile_list.append(tile)
                    self.all_tiles.append(tile)
                if col == "8":
                    image_rect = blue_bottom2.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (blue_bottom2, image_rect)
                    self.tile_list.append(tile)
                    self.all_tiles.append(tile)
                if col == "9":
                    image_rect = blue_wall.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (blue_wall, image_rect)
                    self.tile_list.append(tile)
                    self.all_tiles.append(tile)
                if col == "E":
                    image_rect = self.tankbot_right.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val - 12
                    enemy = (self.tankbot_right, image_rect)
                    self.enemies.append(enemy)
                if col == "A":
                    image_rect = self.bug_alien.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val - 100
                    alien = (self.bug_alien_right, image_rect)
                    self.enemies.append(alien)
                if col == "K":
                    # image_rect = key_door.get_rect()
                    # image_rect.x = x_val
                    # image_rect.y = y_val
                    # tile = (key_door, image_rect)
                    # self.key_tiles.append(tile)
                    self.exit_x = x_val
                    self.exit_y = y_val
                if col == "B":
                    image_rect = key_block.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (key_block, image_rect)
                    self.tile_list.append(tile)
                    self.all_tiles.append(tile)
                if col == "a":
                    image_rect = desert_tile.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (desert_tile, image_rect)
                    self.tile_list.append(tile)
                    self.all_tiles.append(tile)
                if col == "b":
                    image_rect = desert_floor.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (desert_floor, image_rect)
                    self.tile_list.append(tile)
                    self.all_tiles.append(tile)
                if col == "c":
                    image_rect = desert_block.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (desert_block, image_rect)
                    self.tile_list.append(tile)
                    self.all_tiles.append(tile)
                if col == "d":
                    image_rect = sand_block.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (sand_block, image_rect)
                    self.tile_list.append(tile)
                    self.all_tiles.append(tile)
                if col == "F":
                    image_rect = self.flying_robot_right.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val - 12
                    enemy = (self.flying_robot_right, image_rect)
                    x_change = 5
                    y_change = 5
                    self.level_2_enemies.append([enemy, x_change, y_change])

    def update(self, display, unlocked, player_info):
        self.display = display
        self.unlocked = unlocked
        x_change = player_info[7]
        self.exit_x += x_change
        if unlocked:
            x_change = 0
            #print(self.exit_x, self.exit_y)
            image_rect = self.key_door.get_rect()
            image_rect.x = self.exit_x
            image_rect.y = self.exit_y
            display.blit(self.key_door, image_rect)
            door = (self.key_door, image_rect)
            self.key_tiles.append(door)

        for tile in self.tile_list:
            self.display.blit(tile[0], tile[1])
        for tile in self.background_tiles:
            self.display.blit(tile[0], tile[1])
        for tile in self.all_tiles:
            self.display.blit(tile[0], tile[1])


    def unlock(self, display):
        self.display = display
        for tile in self.key_tiles:
            self.display.blit(tile[0], tile[1])

    def get_physical_tiles(self):
        return self.tile_list

    def get_all_tiles(self):
        return self.all_tiles

    def get_bg_tiles(self):
        return self.background_tiles

    def get_enemy_list(self):
        return self.enemies

    def get_keys(self):
        return self.key_tiles

    def get_enemy_list_2(self):
        return self.level_2_enemies
