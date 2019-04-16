import pygame
import math
import sys
import os
import random

all_sprites = pygame.sprite.Group()
X0 = 200
Y0 = 200
CELL_SIZE = 50

def load_image(name, colorkey=None):
    fullname = os.path.join('photos', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    #image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


class Board():
    cell_image = load_image('cell.png')

    def __init__(self, matrix):
        self.cell_size = 50
        self.matrix = matrix
        self.size = (len(matrix[0]) * self.cell_size, len(matrix) * self.cell_size)

    def render(self):
        self.board_screen = pygame.Surface(self.size)

        # make net
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                self.board_screen.blit(Board.cell_image, self.get_left_top_corner_coords(j, i))

        return self.board_screen

    def get_left_top_corner_coords(self, x, y):
        return x * self.cell_size, y * self.cell_size


class Object(pygame.sprite.Sprite):
    images = {'O_object': load_image("O_photo.png"),
             'T_object': load_image("T_photo.png", -1)}

    def __init__(self, type, coords):
        super().__init__(all_sprites)
        self.image = Object.images[type]
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]
        self.x0 = coords[0]
        self.y0 = coords[1]

    def update(self, event=None, deletion=False):
        if not (event is None):
            if self.rect.collidepoint(event.pos):
                if deletion:
                    self.kill()
        else:
            self.rect.x = self.x0 + random.randrange(3) - 1
            self.rect.y = self.y0 + random.randrange(3) - 1

def get_obj_coords(x, y):
    x = X0 + x * CELL_SIZE + 10
    y = Y0 + y * CELL_SIZE + 10
    return x, y

def generate_map(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 1:
                Object('O_object', get_obj_coords(j, i))
            if matrix[i][j] == 2:
                Object('T_object', get_obj_coords(j, i))


def update_map():
    matrix = [[1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1],
              [1, 1, 2, 1, 1, 1],
              [1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 0],
              ]

    generate_map(matrix)

pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
fps = 30
clock = pygame.time.Clock()
running = True
screen.fill(pygame.Color('White'))

matrix = [[1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1],
          [1, 1, 2, 1, 1, 1],
          [1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 0],
          ]


board = Board(matrix)
generate_map(matrix)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
        if event.type == pygame.MOUSEBUTTONUP:
            all_sprites.update(event, True)

    #Making board
    all_sprites.update()
    screen.blit(board.render(), (200, 200))
    all_sprites.draw(screen)

    #Drawing board
    clock.tick(fps)
    pygame.display.flip()

pygame.quit()