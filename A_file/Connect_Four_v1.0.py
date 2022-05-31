# coding=utf-8

import pygame
import os
import sys
import numpy as np
import math


COLS = 7
ROWS = 6
SQUARE_SIZE = 90
CHIP_SIZE = int(SQUARE_SIZE/2 - 6)
FRAMERATE = 60

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

width = COLS * SQUARE_SIZE
height = (ROWS + 1) * SQUARE_SIZE
size = (width, height)

def create_board():
    board_array = np.zeros((ROWS, COLS))
    return board_array

def player_move(board_array, row, col, chip):
    board_array[row][col] = chip

def valid_move(board_array, col):
    return board_array[ROWS-1][col] == 0

def check_row(board_array, col):
    for r in range(ROWS):
        if board_array[r][col] == 0:
            return r

def print_board(board_array):
    print(np.flip(board_array, 0))

def winning_move(board_array, chip):
    
    for c in range(COLS-3):
        for r in range(ROWS):
            if board_array[r][c] == chip and board_array[r][c+1] == chip and board_array[r][c+2] == chip and board_array[r][c+3] == chip:
                return True

    for c in range(COLS):
        for r in range(ROWS-3):
            if board_array[r][c] == chip and board_array[r+1][c] == chip and board_array[r+2][c] == chip and board_array[r+3][c] == chip:
                return True

    for c in range(COLS-3):
        for r in range(ROWS-3):
            if board_array[r][c] == chip and board_array[r+1][c+1] == chip and board_array[r+2][c+2] == chip and board_array[r+3][c+3] == chip:
                return True

    for c in range(COLS-3):
        for r in range(3, ROWS):
            if board_array[r][c] == chip and board_array[r-1][c+1] == chip and board_array[r-2][c+2] == chip and board_array[r-3][c+3] == chip:
                return True


def draw_ui(board_array):
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c*SQUARE_SIZE, r*SQUARE_SIZE+SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), int(r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2)), CHIP_SIZE)
    
    for c in range(COLS):
        for r in range(ROWS):
            if board_array[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), height-int(r*SQUARE_SIZE+SQUARE_SIZE/2)), CHIP_SIZE)
        
    for c in range(COLS):
        for r in range(ROWS):
            if board_array[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), height-int(r*SQUARE_SIZE+SQUARE_SIZE/2)), CHIP_SIZE)
    pygame.display.update()


board_array = create_board()
print_board(board_array)

no_winner = True
turn = 0

pygame.init()

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
win_msg = pygame.font.SysFont("Comic Sans MS", 75)

draw_ui(board_array)
pygame.display.update()

while no_winner:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARE_SIZE))
            mousex = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (mousex, int(SQUARE_SIZE/2)), CHIP_SIZE)

            else:
                pygame.draw.circle(screen, YELLOW, (mousex, int(SQUARE_SIZE/2)), CHIP_SIZE)
  
        pygame.display.update()
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))

            if turn == 0:
                mousex = event.pos[0]
                col = int(math.floor(mousex/SQUARE_SIZE))

                if valid_move(board_array, col):
                    row = check_row(board_array, col)
                    player_move(board_array, row, col, 1)

                    if winning_move(board_array, 1):
                        msg = win_msg.render("PLAYER 1 WINS!", 1, RED)
                        screen.blit(msg, (30,6))
                        no_winner = False
            else:
                mousex = event.pos[0]
                col = int(math.floor(mousex/SQUARE_SIZE))
                
                if valid_move(board_array, col):
                    row = check_row(board_array, col)
                    player_move(board_array, row, col, 2)

                    if winning_move(board_array, 2):
                        msg = win_msg.render("Player 2 wins!", 1, YELLOW)
                        screen.blit(msg, (40, 10))
                        no_winner = False

            print_board(board_array)
            draw_ui(board_array)

            turn += 1
            turn = turn % 2
            if no_winner == False:
                pygame.time.wait(3000)

    
clock.tick(FRAMERATE) 