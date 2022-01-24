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
    def __init__(self, sheet):
        pygame.sprite.Sprite.__init__(self)
        self.sheet = sheet
        standing_right = self.sheet.image_at((5, 5, 70, 75), -1)
        shooting_right = self.sheet.image_at((535, 160, 100, 80), -1)
        walking_right = [self.sheet.image_at((18, 172, 68, 68), -1), self.sheet.image_at((101, 173, 68, 68), -1),
                         self.sheet.image_at((177, 173, 68, 68), -1), self.sheet.image_at((252, 173, 68, 68), -1),
                         self.sheet.image_at((0, 0, 70, 80), -1)]
        self.image = walking_right[3]
        self.frame = 0
        self.frame_rate = 50
        self.previous_update = pygame.time.get_ticks()
        self.rect = self.image.get_rect()
        self.rect.center = DISPLAY_WIDTH//2, DISPLAY_HEIGHT - self.rect.height*1.15
        self.change_x = 0

    def update(self, display):
        self.rect.x += self.change_x

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.change_x = 3
        elif keys[pygame.K_LEFT]:
            self.change_x = -3
        else:
            self.change_x = 0

        if self.rect.x < 0:
            self.change_x = 0
            self.rect.x = 1
        elif self.rect.x > DISPLAY_WIDTH-self.rect.width:
            self.change_x = 0
            self.rect.x = DISPLAY_WIDTH-self.rect.width-1
        display.blit(self.image, (self.rect.x, self.rect.y))
        #pygame.draw.rect(display, WHITE, self.rect, 2)

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
        brick_block = pg.image.load("assets/tile116.png")
        brick_block = pg.transform.scale(brick_block, (TILE_SIZE, TILE_SIZE))
        bottom_block = pg.image.load("assets/tile094.png")
        bottom_block = pg.transform.scale(bottom_block, (TILE_SIZE, TILE_SIZE))
        wall_block = pg.image.load("assets/tile095.png")
        wall_block = pg.transform.scale(wall_block, (TILE_SIZE, TILE_SIZE))
        door_block = pg.image.load("assets/door_red.png")
        door_block = pg.transform.scale(door_block, (TILE_SIZE*2, TILE_SIZE*2))
        self.tile_list = []

        for i, row in enumerate(LAYOUT):
            for j, col in enumerate(row):
                x_val = j * TILE_SIZE
                y_val = i * TILE_SIZE

                if col == "1":
                    image_rect = brick_block.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (brick_block, image_rect)
                    self.tile_list.append(tile)
                if col == "2":
                    image_rect = bottom_block.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (bottom_block, image_rect)
                    self.tile_list.append(tile)
                if col == "3":
                    image_rect = wall_block.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (wall_block, image_rect)
                    self.tile_list.append(tile)
                if col == "4":
                    image_rect = door_block.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (door_block, image_rect)
                    self.tile_list.append(tile)

    def update(self, display):
        self.display = display
        for tile in self.tile_list:
            self.display.blit(tile[0], tile[1])


