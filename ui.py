import pygame
import math
import sys
import os


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
    #здесь будут фоточки
    cell_image = load_image('cell.png')

    def __init__(self, matrix):
        self.cell_size = 50
        self.matrix = matrix
        self.size = (len(matrix[0]) * self.cell_size, len(matrix) * self.cell_size)
        self.board_screen = pygame.Surface(self.size)

    def render(self):
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                self.board_screen.blit(Board.cell_image, (j * self.cell_size, i * self.cell_size))
        return self.board_screen

pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
fps = 30
clock = pygame.time.Clock()
running = True
screen.fill(pygame.Color('White'))

matrix = [[0 for i in range(3)] for _ in range(4)]
board = Board(matrix)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
        if event.type == pygame.MOUSEBUTTONUP:
            pass
    screen.blit(board.render(), (0,0))
    clock.tick(fps)
    pygame.display.flip()

pygame.quit()