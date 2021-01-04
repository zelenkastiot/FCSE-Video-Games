"""

 Created on 04-Dec-20
 @author: Kiril Zelenkovski

"""
# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import pygame
import random
import sys
import time
from pygame.locals import *
import numpy as np

FPS = 15
FPS_INCREASE = time.time()
WINDOWWIDTH = 900    # Смени ширина
WINDOWHEIGHT = 660   # Смени висина
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)


#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK
YELLOW    = pygame.color.Color('yellow')
GLAUCOUS = ( 96, 130, 182)

TIMEOUT = time.time()

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

show_flag = True

def main(show_flag = True):
    global FPSCLOCK, DISPLAYSURF, BASICFONT, FPS, FPS_INCREASE
    global START_SURF, START_RECT, QUIT_SURF, QUIT_RECT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')
    FPS = 15
    FPS_INCREASE = time.time()


    if show_flag:
        showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT


    start_ticks = pygame.time.get_ticks()  # starter tick
    counter = 9  # додај бројач за жолто јаболко
    flag = 'hidden'  # знаме за јаболоко; 'hidden'-скриено, 'shown'-прикажано

    global FPS, FPS_INCREASE

    # Start the apple in a random place.
    apple = getRandomLocation()
    yellow_apple1 = getRandomLocation() # креирам второ јаболко (идентична постапка како прво)
    yellow_apple2 = getRandomLocation()  # креирам второ јаболко (идентична постапка како прво)
    yellow_apple3 = getRandomLocation()  # креирам второ јаболко (идентична постапка како прво)

    # плус поени
    score_plu = 0

    while True: # main game loop
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        seconds = int(seconds)
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return # game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return # game over

        # check if worm has eaten an apply
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation() # set a new apple somewhere
        # проверка за дали жолто јаболо е изедено
        elif wormCoords[HEAD]['x'] == yellow_apple1['x'] and wormCoords[HEAD]['y'] == yellow_apple1['y']:
            score_plu += 1
            yellow_apple1 = getRandomLocation()  # овде влегува само ако изеде жолто; ако е изедено поставува ново

        elif wormCoords[HEAD]['x'] == yellow_apple2['x'] and wormCoords[HEAD]['y'] == yellow_apple2['y']:
            score_plu += 1
            yellow_apple2 = getRandomLocation()  # овде влегува само ако изеде жолто; ако е изедено поставува ново
            # проверка за дали жолто јаболо е изедено
        elif wormCoords[HEAD]['x'] == yellow_apple3['x'] and wormCoords[HEAD]['y'] == yellow_apple3['y']:
            score_plu += 1
            yellow_apple3 = getRandomLocation()  # овде влегува само ако изеде жолто; ако е изедено поставува ново

        else:
            del wormCoords[-1]  # remove worm's tail segment

        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawApple(apple)

        """
        Главна функција за жолто јаболоко: прима на влез:
        - counter: моментален бројач (или за покажување или за криење на јаболко) 
        - seconds: секунди што изминуваат 
        - start_ticks: почетно време од последно започнување на тајмер
        - flag: генерално знаме за гледање на дали покажуваме или криеме жолто јаболко
        
        """
        counter, start_ticks, flag = drawYellowAppleTime(counter, seconds, start_ticks, flag)

        # на излез добиваме 3 параметри од кој еден е знамето: ако е shown - цртај го јаболкото
        if flag == 'shown':
            drawApple(yellow_apple1, GLAUCOUS)
            drawApple(yellow_apple2, GLAUCOUS)
            drawApple(yellow_apple3, GLAUCOUS)

        drawScore(len(wormCoords) - 3 + score_plu*2)
        pygame.display.update()

        # # брза проверка ја најдов на интернет
        # if time.time() - FPS_INCREASE >= 30:
        #     # слично како тајмерите од 3: проверуваме дали разликата е поголема на времето сега и на тоа од почнување
        #     # ако е поголемо од 30 (поминале 30 секунди)
        #     FPS += 20  # зголеми FPS за 10 frames per second
        #     FPS_INCREASE = time.time()  # слично како кај 3 почетното време постави го пак да биде сегашното (т.е. референтно)

        FPSCLOCK.tick(FPS)


def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Wormy!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Wormy!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}

def getSpotClicked(board, x, y):
    # from the x & y pixel coordinates, get the x & y board coordinates
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    basicFont = pygame.font.Font('freesansbold.ttf', 40)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    startSurf = basicFont.render('Start from the beginning', True, YELLOW)
    quitSurf = basicFont.render('Quit', True, YELLOW)
    startRect = startSurf.get_rect()
    quitRect = quitSurf.get_rect()

    startRect.midtop = (WINDOWWIDTH / 2, 120)
    quitRect.midtop = (WINDOWWIDTH / 2, 140)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)

    DISPLAYSURF.blit(startSurf, startRect)
    DISPLAYSURF.blit(quitSurf, quitRect)


    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()


    while True:
        for event in pygame.event.get():  # event handling loop
            if event.type == MOUSEBUTTONUP:
                if startRect.collidepoint(event.pos):
                    show_flag = False
                    main(show_flag)
                elif quitRect.collidepoint(event.pos):
                    terminate()

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def my_ceil(a, precision=0):
    return np.round(a + 0.5 * 10**(-precision), precision)

def my_floor(a, precision=0):
    return np.round(a - 0.5 * 10**(-precision), precision)

# Главна функција за цртање на жолто јаболко
def drawYellowAppleTime(counter, seconds, start_ticks, flag):

    # HIDDEN: криј го јаболкото
    if flag == 'hidden':
        # 1 проверка: дали тајмерот истече
        if seconds == counter:
            # да, истече
            text = ''
            # испиши текст горе десно под score
            yellowSurf = BASICFONT.render(text, True, WHITE)
            yellowRect = yellowSurf.get_rect()
            yellowRect.topleft = (WINDOWWIDTH - 300, 25)
            DISPLAYSURF.blit(yellowSurf, yellowRect)
            # ресетирај бројач на 9. значи 9 секунди има 9 нема. Тука може да се оди со random.randint(1,10)
            counter = 9
            # најбитно: ресетирај го почетното време на бројачот
            start_ticks = pygame.time.get_ticks()
            # смени знаме на shown за кога ќе излезе да почне да го покажува
            flag = 'shown'
            # врати вредности
            return counter, start_ticks, flag
        else:
            # не е истечен сеуште, започни тајмер (descending) за кога е следното
            display_timer = counter-seconds
            # испиши текст горе десно под score
            text = f'Yellow apple appears in: {str(display_timer)}'
            yellowSurf = BASICFONT.render(text, True, WHITE)
            yellowRect = yellowSurf.get_rect()
            yellowRect.topleft = (WINDOWWIDTH - 282, 25)
            DISPLAYSURF.blit(yellowSurf, yellowRect)
            # врати вредности
            return counter, start_ticks, flag

    # SHOWN: покажувај јаболко
    else:
        # 1 проверка: дали тајмерот истече
        if seconds == counter:
            # да, истече
            text = ''
            # испиши текст горе десно под score
            yellowSurf = BASICFONT.render(text, True, WHITE)
            yellowRect = yellowSurf.get_rect()
            yellowRect.topleft = (WINDOWWIDTH - 300, 25)
            DISPLAYSURF.blit(yellowSurf, yellowRect)
            # ресетирај бројач на 9. значи 9 секунди има 9 нема. Тука може да се оди со random.randint(1,10)
            counter = 9
            # најбитно: ресетирај го почетното време на бројачот
            start_ticks = pygame.time.get_ticks()
            # смени знаме на hidden за кога ќе излезе да прекине да го покажува
            flag = 'hidden'
            # врати вредности
            return counter, start_ticks, flag
        else:
            # не е истечен сеуште, започни тајмер (descending) колку време ќе го покажуваш
            display_timer = counter - seconds
            # испиши текст горе десно под score
            text = f'Yellow apples disappear in: {str(display_timer)}'
            yellowSurf = BASICFONT.render(text, True, WHITE)
            yellowRect = yellowSurf.get_rect()
            yellowRect.topleft = (WINDOWWIDTH - 305, 25)
            DISPLAYSURF.blit(yellowSurf, yellowRect)
            # врати вредности
            return counter, start_ticks, flag


def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)


def drawApple(coord, color=RED):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, color, appleRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()