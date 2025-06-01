import pygame
import sys
from random import choice

# Constantes
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 1280*9//16
BOX_INTERVAL_X = 15
BOX_WIDTH = 90
BOX_HEIGHT = 130
BOX_MEDIUM_HEIGHT = int(0.3*WINDOW_HEIGHT)

# Cores
LIGHT_GRAY = pygame.Color(150,150,150)
CYAN = pygame.Color(0, 220, 220)
RED = pygame.Color(250,0,0)
YELLOW = pygame.Color(230,220,0)


def set_boxes(num_boxes):
    y = BOX_MEDIUM_HEIGHT - BOX_HEIGHT//2

    total_dx = BOX_INTERVAL_X*(num_boxes-1)
    total_width = BOX_WIDTH*num_boxes + total_dx
    starting_point_x = int(WINDOW_WIDTH/2 - total_width/2)

    dx = BOX_INTERVAL_X + BOX_WIDTH

    boxes = [pygame.Rect(starting_point_x+dx*i, y, BOX_WIDTH, BOX_HEIGHT) for i in range(num_boxes)]
    return boxes



pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("RoubaChavePIX.exe")
boxes = set_boxes(9)

box_colors = {i:CYAN for i,_ in enumerate(boxes)}

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, box in enumerate(boxes):
                if box.collidepoint(event.pos):
                    box_colors[i] = choice([CYAN,RED,YELLOW])

    screen.fill(LIGHT_GRAY)  # gray background
    for i, box in enumerate(boxes):
        pygame.draw.rect(screen, box_colors[i], box)
    pygame.display.flip()
