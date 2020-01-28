import math
import pygame
import random
import sys
from pygame.locals import *

mainClock = pygame.time.Clock()

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
WIDTH = 4
HEIGHT = 4

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MAROON = (80, 0, 0)

pygame.init()

windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('2048')

moveLeft = False
moveRight = False
moveUp = False
moveDown = False
count = 0


def getNewBoard():
    board = []
    for i in range(WIDTH):
        board.append([0, 0, 0, 0])
    return board

def terminate():
    pygame.quit()
    sys.exit()

def addElement(board):
    if any(0 in sublist for sublist in board):
        while True:
            randy = random.randint(0, HEIGHT - 1)
            randx = random.randint(0, WIDTH - 1)
            if board[randx][randy] == 0:
                num = 2
                randnum = random.randint(1, 10)
                if randnum == 1:
                    num *= 2
                board[randx][randy] = num
                return [randx, randy]



def getBoardCopy(board):
    boardCopy = getNewBoard()

    for x in range(WIDTH):
        for y in range(HEIGHT):
            boardCopy[x][y] = board[x][y]

    return boardCopy


def shiftY(board, initial, final, step):
    done = False
    while not done:
        boardCopy = getBoardCopy(board)
        done = True
        for y in range(initial, final, step):
            for x in range(WIDTH):
                if board[x][y] != 0 and board[x][y + step] == 0:
                    board[x][y + step] = board[x][y]
                    board[x][y] = 0
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if boardCopy[x][y] != board[x][y]:
                    done = False
    for y in range(final, initial, -step):
        for x in range(WIDTH):
            if board[x][y] != 0 and board[x][y - step] == board[x][y]:
                board[x][y] = board[x][y - step] * 2
                board[x][y - step] = 0
    done = False
    while not done:
        boardCopy = getBoardCopy(board)
        done = True
        for y in range(initial, final, step):
            for x in range(WIDTH):
                if board[x][y] != 0 and board[x][y + step] == 0:
                    board[x][y + step] = board[x][y]
                    board[x][y] = 0
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if boardCopy[x][y] != board[x][y]:
                    done = False


def shiftX(board, initial, final, step):
    done = False
    while not done:
        boardCopy = getBoardCopy(board)
        done = True
        for x in range(initial, final, step):
            for y in range(HEIGHT):
                if board[x][y] != 0 and board[x + step][y] == 0:
                    board[x + step][y] = board[x][y]
                    board[x][y] = 0
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if boardCopy[x][y] != board[x][y]:
                    done = False
    for x in range(final, initial, -step):
        for y in range(HEIGHT):
            if board[x][y] != 0 and board[x - step][y] == board[x][y]:
                board[x][y] = board[x - step][y] * 2
                board[x - step][y] = 0
    done = False
    while not done:
        boardCopy = getBoardCopy(board)
        done = True
        for x in range(initial, final, step):
            for y in range(HEIGHT):
                if board[x][y] != 0 and board[x + step][y] == 0:
                    board[x + step][y] = board[x][y]
                    board[x][y] = 0
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if boardCopy[x][y] != board[x][y]:
                    done = False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, BLACK)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    pygame.draw.rect(windowSurface, (255, 255, 255), textrect)
    pygame.draw.rect(windowSurface, (0, 0, 0), textrect,3)
    surface.blit(textobj, textrect)
    pygame.display.update()

def gameOver(board):
    lost = True
    boardcopy = getBoardCopy(board)
    shiftX(boardcopy, 0, WIDTH - 1, 1)
    if not boardcopy == board:
        lost = False
        boardcopy = getBoardCopy(board)
    shiftX(boardcopy, WIDTH - 1, 0, -1)
    if not boardcopy == board:
        lost = False
        boardcopy = getBoardCopy(board)
    shiftY(boardcopy, HEIGHT - 1, 0, -1)
    if not boardcopy == board:
        lost = False
        boardcopy = getBoardCopy(board)
    shiftY(boardcopy, 0, HEIGHT - 1, 1)
    if not boardcopy == board:
        lost = False

    if lost:
        drawText('YOU LOSE',pygame.font.SysFont(None, 170),windowSurface, 1, WINDOWHEIGHT/2 - 60)
        waitForPlayerToPressKey()
        return True
    if any(2048 in sublist for sublist in board):
        drawText('YOU WIN!',pygame.font.SysFont(None, 170),windowSurface, 22, WINDOWHEIGHT/2 - 60)
        waitForPlayerToPressKey()
        return True
    return False


def waitForPlayerToPressKey():
    while True:
        for gameevent in pygame.event.get():
            if gameevent.type == QUIT:
                terminate()
            if gameevent.type == KEYDOWN:
                if gameevent.key == K_ESCAPE:  # Pressing ESC quits.
                    terminate()
                return


while True:
    gameboard = getNewBoard()
    f = addElement(gameboard)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_a:
                    moveRight = False
                    moveLeft = True
                    count = 0
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True
                    count = 0
                if event.key == K_UP or event.key == K_w:
                    moveDown = False
                    moveUp = True
                    count = 0
                if event.key == K_DOWN or event.key == K_s:
                    moveUp = False
                    moveDown = True
                    count = 0
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                    #count = 0
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                    #count = 0
                if event.key == K_UP or event.key == K_w:
                    moveUp = False
                    #count = 0
                if event.key == K_DOWN or event.key == K_s:
                    moveDown = False
                    #count = 0
                if event.key == K_q:
                    pygame.quit()
                    sys.exit()
        windowSurface.fill(WHITE)
        copyboard = []
        if moveDown or moveUp or moveLeft or moveRight and count == 0:
            copyboard = getBoardCopy(gameboard)
        if moveDown and count == 0:
            # print('s')
            shiftX(copyboard, 0, WIDTH - 1, 1)
            if not copyboard == gameboard:
                shiftX(gameboard, 0, WIDTH - 1, 1)
                count = 1
        if moveUp and count == 0:
            # print('w')
            shiftX(copyboard, WIDTH - 1, 0, -1)
            if not copyboard == gameboard:
                shiftX(gameboard, WIDTH - 1, 0, -1)
                count = 1
        if moveLeft and count == 0:
            # print('a')
            shiftY(copyboard, HEIGHT - 1, 0, -1)
            if not copyboard == gameboard:
                shiftY(gameboard, HEIGHT - 1, 0, -1)
                count = 1
        if moveRight and count == 0:
            # print('d')
            shiftY(copyboard, 0, HEIGHT - 1, 1)
            if not copyboard == gameboard:
                shiftY(gameboard, 0, HEIGHT - 1, 1)
                count = 1

        if count == 1:
            f = addElement(gameboard)
            count += 1
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if len(str(gameboard[j][i])) == 1:
                    basicFont = pygame.font.SysFont(None, 200)
                    offsetx = 38
                    offsety = 10
                elif len(str(gameboard[j][i])) == 2:
                    basicFont = pygame.font.SysFont(None, 180)
                    offsetx = 5
                    offsety = 16
                elif len(str(gameboard[j][i])) == 3:
                    basicFont = pygame.font.SysFont(None, 120)
                    offsetx = 2
                    offsety = 34
                else:
                    basicFont = pygame.font.SysFont(None, 90)
                    offsetx = 3
                    offsety = 44
                if gameboard[j][i] == 0:
                    TEXTCOLOR = (0, 0, 0)
                else:
                    factor = math.log(gameboard[j][i], 2)
                    TEXTCOLOR = (255 - 23.1818 * factor, 0, 0)
                text = basicFont.render(str(gameboard[j][i]), True, TEXTCOLOR)
                box = pygame.Rect(0 + (i * WINDOWWIDTH / 4), 0 + (j * WINDOWHEIGHT / 4), WINDOWHEIGHT / 4,
                                  WINDOWWIDTH / 4)
                pygame.draw.rect(windowSurface, BLACK, box, 3)
                if not gameboard[j][i] == 0:
                    windowSurface.blit(text, (box.left + offsetx, box.top + offsety))
        box = pygame.Rect(0 + (f[1] * WINDOWWIDTH / 4), 0 + (f[0] * WINDOWHEIGHT / 4), WINDOWHEIGHT / 4,
                          WINDOWWIDTH / 4)
        pygame.draw.rect(windowSurface, RED, box, 3)
        pygame.display.update()
        if gameOver(gameboard):
            break
        mainClock.tick(40)

        count = 2