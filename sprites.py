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
            x_sprite_size = ( sheet_width - 2 * x_margin
                    - (num_cols - 1) * x_padding ) / num_cols
            y_sprite_size = ( sheet_height - 2 * y_margin
                    - (num_rows - 1) * y_padding ) / num_rows

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
    def __init__(self, sheet, x, y, tile_size, tile_set):
        pygame.sprite.Sprite.__init__(self)
        self.sheet = sheet
        self.tile_size = tile_size
        self.tile_set = tile_set
        self.standing_right = self.sheet.image_at((15, 7, 50, 72), -1)
        self.standing_left = pg.transform.flip(self.standing_right, True, False)
        self.jumping_right = self.sheet.image_at((138, 465, 50, 102), -1)
        self.jumping_left = pg.transform.flip(self.jumping_right, True, False)
        self.falling_right = self.sheet.image_at((330, 465, 50, 72), -1)
        self.falling_left = pg.transform.flip(self.falling_right, True, False)
        self.shooting_right = self.sheet.image_at((535, 160, 100, 80), -1)
        self.run_right = [self.sheet.image_at((23, 172, 51, 68), -1), self.sheet.image_at((106, 173, 51, 68), -1),
                         self.sheet.image_at((182, 173, 51, 68), -1), self.sheet.image_at((257, 173, 51, 68), -1)]
        self.run_left = [pg.transform.flip(player, True, False) for player in self.run_right]
        self.image = self.standing_right
        self.frame = 0
        self.frame_rate = 50
        self.previous_update = pygame.time.get_ticks()
        self.image_delay = 100
        self.velo_y = 0
        self.image_rect = self.image.get_rect()
        self.image_rect.center = DISPLAY_WIDTH//7, DISPLAY_HEIGHT - self.image_rect.height*0.5
        self.right = True
        self.left = False
        self.jumping = False
        self.falling = False
        self.shooting = False

    def update(self, display):
        self.current = pygame.time.get_ticks()
        dx = 0
        dy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            dx = 4
            self.right = True
            self.left = False
            now = pygame.time.get_ticks()
            if now - self.previous_update >= self.image_delay:
                self.previous_update = now
                if self.frame >= len(self.run_right):
                    self.frame = 0
                self.image = self.run_right[self.frame]
                self.frame = self.frame + 1

        elif keys[pygame.K_a]:
            dx = -4
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
            dx = 0
            self.frame = 0
            if self.right:
                self.image = self.standing_right
            elif self.left:
                self.image = self.standing_left
        if keys[pygame.K_SPACE] and not self.jumping and not self.falling:
            self.velo_y = -10
            self.jumping = True
        if not keys[pygame.K_SPACE]:
            self.jumping = False
        self.velo_y += 0.3
        if self.velo_y < 0:
            self.jumping = True
            self.falling = False
        else:
            self.jumping = False
            self.falling = True
        if self.velo_y >= 5:
            self.velo_y = 5
            dy = 5
        if self.jumping and self.right:
            self.image = self.jumping_right
        if self.jumping and self.left:
            self.image = self.jumping_left

        dy += self.velo_y
        for tile in self.tile_set:
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
        # for event in pg.event.get():
        #     if event.type == pg.KEYUP:
        #         if event.key == pg.K_e:
        #             self.shooting = False

        self.image_rect.x += dx
        self.image_rect.y += dy

        if self.image_rect.left <= self.tile_size:
            self.image_rect.left = self.tile_size
        display.blit(self.image, (self.image_rect.x, self.image_rect.y))
        pygame.draw.rect(display, WHITE, self.image_rect, 2)
    def get_info(self):
        return self.image_rect.x, self.image_rect.y, self.shooting


class Weapons(pygame.sprite.Sprite):
    def __init__(self, sheet, x, y, display, tile_set):
        pygame.sprite.Sprite.__init__(self)
        self.sheet = sheet
        self.x = x
        self.y = y+25
        self.display = display
        self.tile_set = tile_set
        self.velo = 0
        self.laser_right = self.sheet.image_at((322, 690, 45, 22), -1)
        self.laser_left = pg.transform.flip(self.laser_right, True, False)
        self.image = self.sheet.image_at((322, 690, 45, 22), -1)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self, right, left):
        if right == True:
            if self.x < self.rect.centerx < self.x+40:
                self.velo = 5
                self.image = self.laser_right
        if left == True:
            if self.x < self.rect.centerx < self.x + 40:
                self.velo = -5
                self.image = self.laser_left
        self.rect.x += self.velo
        self.display.blit(self.image, (self.rect.x, self.rect.y))


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
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        brick_block = pg.image.load("assets/tile116.png")
        brick_block = pg.transform.scale(brick_block, (TILE_SIZE, TILE_SIZE))
        bottom_block = pg.image.load("assets/tile094.png")
        bottom_block = pg.transform.scale(bottom_block, (TILE_SIZE, TILE_SIZE))
        wall_block = pg.image.load("assets/tile095.png")
        wall_block = pg.transform.scale(wall_block, (TILE_SIZE, TILE_SIZE))
        door_block = pg.image.load("assets/door_red.png")
        door_block = pg.transform.scale(door_block, (TILE_SIZE*2, TILE_SIZE*2))
        self.tile_list = []
        self.background_tiles = []
        self.all_tiles = []

        for i, row in enumerate(LAYOUT):
            for j, col in enumerate(row):
                x_val = j * TILE_SIZE - 1000
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

    def update(self, display):
        self.display = display
        for tile in self.tile_list:
            self.display.blit(tile[0], tile[1])
        for tile in self.background_tiles:
            self.display.blit(tile[0], tile[1])
        for tile in self.all_tiles:
            self.display.blit(tile[0], tile[1])
    def get_physical_tiles(self):
        return self.tile_list
    def get_all_tiles(self):
        return self.all_tiles