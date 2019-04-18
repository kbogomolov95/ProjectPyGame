import pygame
import math
import sys
import os
import random
import logic
from pprint import pprint

all_sprites = pygame.sprite.Group()

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


class Score():
    def __init__(self, x0, y0):
        self.score = 0
        self.font = pygame.font.Font(None, 50)
        self.text = self.font.render("Your score: {}".format(self.score), 1, (0, 0, 0))
        self.text_x = x0
        self.text_y = y0
        self.text_w = self.text.get_width()
        self.text_h = self.text.get_height()

    def draw(self, screen):
        screen.blit(self.text, (self.text_x, self.text_y))

    def tick(self, delta):
        self.score += delta
        self.text = self.font.render("Your score: {}".format(self.score), 1, (0, 0, 0))

    def set_score(self, score):
        self.score = score
        self.text = self.font.render("Your score: {}".format(self.score), 1, (0, 0, 0))


class Object(pygame.sprite.Sprite):
    def __init__(self, name, coords):
        super().__init__(all_sprites)
        self.image = load_image('{}.png'.format(name))
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]
        self.x0 = coords[0]
        self.y0 = coords[1]
        self.selected = False
        self.board_coords = self.get_coords(coords)

    def update(self, params, pos=None):
        if pos != None:
            if self.board_coords != self.get_coords(pos):
                return
            if params['deletion']:
                self.kill()

            if params['selected'] != None:
                self.selected = params['selected']

            if params['move']:
                self.rect.x += params['move'][0]
                self.rect.y += params['move'][1]
                self.x0 = self.rect.x
                self.y0 = self.rect.y
                self.selected = False

            if self.selected:
                self.dergatsa()

    def dergatsa(self):
        self.rect.x = self.x0 + random.randrange(3) - 1
        self.rect.y = self.y0 + random.randrange(3) - 1

    def get_coords(self, coords):
        return int((coords[0] - X0) / 50), int((coords[1] - Y0) / 50)


def get_obj_coords(x, y):
    x = X0 + x * CELL_SIZE
    y = Y0 + y * CELL_SIZE
    return x, y


def generate_map(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            # print(matrix[i][j])
            if matrix[i][j] != 0:
                Object(str(matrix[i][j]), get_obj_coords(j, i))


def update_map(pos1=(), pos2=(), waited=False):
    global matrix
    global all_sprites
    # pprint(matrix)
    if not waited:
        m.swap(pos1, pos2)
    else:
        m.modified_matrix()
    matrix = m.arr
    all_sprites = pygame.sprite.Group()
    # pprint(matrix)
    generate_map(matrix)


def calc(pos1, pos2):
    X1 = int((pos1[0] - X0) / 50)
    X2 = int((pos2[0] - X0) / 50)
    Y1 = int((pos1[1] - Y0) / 50)
    Y2 = int((pos2[1] - Y0) / 50)

    dx = -(X1 - X2)
    dy = -(Y1 - Y2)
    return dx * 5, dy * 5


def get_i_j(pos):
    i = int((pos[0] - X0) / 50)
    j = int((pos[1] - Y0) / 50)
    return (j, i)


def neighbourhood(coord1, coord2):
    a = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for x in a:
        if coord1[0] + x[0] == coord2[0] and coord1[1] + x[1] == coord2[1]:
            return True
    return False

pygame.init()

pygame.mixer.music.load('derevnya-durakov-tp-kalambur.mp3')
pygame.mixer.music.play(111111)
pygame.mixer.music.rewind()

size = width, height = 800, 600
screen = pygame.display.set_mode(size)
fps = 30
clock = pygame.time.Clock()
running = True
screen.fill(pygame.Color('White'))

size = (8, 8)
m = logic.Area(size, 4)
m.matrix()
matrix = m.arr

# нормально подогнать
X0 = 200 - CELL_SIZE * (abs(size[1]) - 7)
Y0 = 200 - CELL_SIZE * (abs(size[0]) - 7)

# Making board
board = Board(matrix)
score_board = Score(220, 100)
generate_map(matrix)

pos1, pos2 = None, None
mov1, mov2 = False, False
params = {'selected': None, 'deletion': False, 'move': False, 'waiting': False}

moving_timer = 0
delay = 15
in_waiting = False

deleting_objects = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type != pygame.MOUSEBUTTONUP:
            continue
        # нажатие на левую кнопку - отмена выбора
        if event.button == 3:
            pos1 = event.pos
            params['selected'] = False
            all_sprites.update(params, pos1)
            # стираем что бы перестало подаваться
            pos1 = None
            pos2 = None
            continue
        # если уже выбрали первую, то выбираем вторую фигурку
        params['selected'] = True
        if pos1 is None:
            pos1 = event.pos
            all_sprites.update(params, pos1)
        else:
            pos2 = event.pos
            params['selected'] = False
            if neighbourhood(get_i_j(pos1), get_i_j(pos2)):
                all_sprites.update(params, pos2)
                mov1 = calc(pos1, pos2)
                mov2 = calc(pos2, pos1)
                moving_timer = 20
            else:
                pos2 = None
                params['selected'] = True

    if delay:
        delay -= 1

    if moving_timer:
        moving_timer -= 1
    else:
        mov1, mov2 = False, False

    if moving_timer == 1:
        moving_timer -= 1
        update_map(get_i_j(pos1), get_i_j(pos2))
        params['waiting'] = True
        delay = 15
        pos1 = None
        pos2 = None
        params['selected'] = False

    elif moving_timer == 10:
        mov1, mov2 = False, False
        params['selected'] = True

    if delay == 1:
        if in_waiting:
            update_map((0, 0), (0, 0))
            in_waiting = False
        else:
            update_map(waited=True)
            in_waiting = True
        delay = 15

    #######ОТРИСОВКА#######
    deleting_objects = logic.new_consequences(matrix, m.size, check = True)
    last_state = params['selected']
    params['move'] = False
    params['selected'] = True
    for coords in deleting_objects:
        all_sprites.update(params, get_obj_coords(coords[1], coords[0]))
    params['selected'] = last_state

    params['move'] = mov1
    all_sprites.update(params, pos1)
    screen.fill((255, 255, 255))
    params['move'] = mov2
    all_sprites.update(params, pos2)
    screen.blit(board.render(), (X0, Y0))
    score_board.set_score(logic.score)
    score_board.draw(screen)
    all_sprites.draw(screen)
    clock.tick(fps)
    pygame.display.flip()
    ######################

pygame.quit()

#c пустыми    update_map(waited=True)
#с рандомными update_map((0, 0), (0, 0))