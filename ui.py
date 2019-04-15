import pygame
import math

class Board()
    def __init__(self, matrix):
        self.board = []

    def matrix_parse(self):
        self.board =
        for string in matrix:
            for obj in string:


pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
fps = 30
clock = pygame.time.Clock()
running = True
screen.fill(pygame.Color('Black'))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
        if event.type == pygame.MOUSEBUTTONUP:
            pass
    clock.tick(fps)
    pygame.display.flip()

pygame.quit()