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

# бои за јаболки
YELLOW    = pygame.color.Color('yellow')
BLUE      = pygame.color.Color('blue')

# snake shades: прва боја надворешна (темна), втора боја внатрешна (светла)
# GREENS
GREENS_tuple = (DARKGREEN, GREEN)
# BLUES
DARKBLUE = (0, 128, 255)
LIGHTBLUE = (204, 229, 255)
BLUES_tuple = (DARKBLUE, LIGHTBLUE)
# ORANGES
DARKORANGE = (255, 128, 0)
LIGHTORANGE = (255, 204, 153)
ORANGES_tuple = (DARKORANGE, LIGHTORANGE)
# PINKS
DARKPINK = (255, 0, 127)
LIGHTPINK = (255, 204, 229)
PINKS_tuple = (DARKPINK, LIGHTPINK)

worm_shades = [GREENS_tuple, BLUES_tuple, ORANGES_tuple, PINKS_tuple]


TIMEOUT = time.time()

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, FPS, FPS_INCREASE

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')
    FPS = 15
    FPS_INCREASE = time.time()



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


    start_ticks_yellow = pygame.time.get_ticks()  # starter tick
    counter_yellow = 9  # додај бројач за жолто јаболко
    flag_yellow = 'hidden'  # знаме за јаболоко; 'hidden'-скриено, 'shown'-прикажано

    start_ticks_blue = pygame.time.get_ticks()  # starter tick
    counter_blue = 15  # додај бројач за жолто јаболко
    flag_blue = 'hidden'  # знаме за јаболоко; 'hidden'-скриено, 'shown'-прикажано

    worm_color = GREENS_tuple
    global FPS, FPS_INCREASE

    # Start the apple in a random place.
    apple        = getRandomLocation()
    yellow_apple = getRandomLocation()  # креирам второ јаболко (идентична постапка како прво)
    blue_apple   = getRandomLocation()  # креирам трето јаболко (идентична постапка како прво)
    while True:  # main game loop
        seconds_yellow = (pygame.time.get_ticks() - start_ticks_yellow) / 1000
        seconds_yellow = int(seconds_yellow)

        seconds_blue = (pygame.time.get_ticks() - start_ticks_blue) / 1000
        seconds_blue = int(seconds_blue)


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
        elif wormCoords[HEAD]['x'] == yellow_apple['x'] and wormCoords[HEAD]['y'] == yellow_apple['y']:
            del wormCoords[-1], wormCoords[-2]
            yellow_apple = getRandomLocation()  # овде влегува само ако изеде жолто; ако е изедено поставува ново
        # проверка за дали плаво јаболо е изедено
        elif wormCoords[HEAD]['x'] == blue_apple['x'] and wormCoords[HEAD]['y'] == blue_apple['y']:
            FPS = temp_FPS
            # blue_apple = getRandomLocation()  # овде влегува само ако изеде плавото; ако е изедено НЕ поставува ново
            # ресетираме се за нови 15 секунди
            counter_blue = 15
            seconds_blue = (pygame.time.get_ticks() - start_ticks_blue) / 1000
            seconds_blue = int(seconds_blue)
            flag_blue = 'hidden'
            worm_color = random.choice(worm_shades)

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
        drawWorm(wormCoords, worm_color)
        drawApple(apple)

        """
        Главна функција за жолто јаболоко: прима на влез:
        - counter_yellow: моментален бројач (или за покажување или за криење на јаболко) 
        - seconds_yellow: секунди што изминуваат 
        - start_ticks_yellow: почетно време од последно започнување на тајмер
        - flag_yellow: генерално знаме за гледање на дали покажуваме или криеме жолто јаболко
        
        """
        counter_yellow, start_ticks_yellow, flag_yellow = appleTimers(counter_yellow,
                                                                      seconds_yellow,
                                                                      start_ticks_yellow,
                                                                      flag_yellow,
                                                                      which='yellow')
        counter_blue, start_ticks_blue, flag_blue       = appleTimers(counter_blue,
                                                                      seconds_blue,
                                                                      start_ticks_blue,
                                                                      flag_blue,
                                                                      which='blue')

        # на излез добиваме 3 параметри од кој еден е знамето: ако е shown - цртај го жолтото
        if flag_yellow == 'shown':
            drawApple(yellow_apple, YELLOW)

        # на излез добиваме 3 параметри од кој еден е знамето: ако е shown - цртај го плавото
        if flag_blue == 'shown':
            drawApple(blue_apple, BLUE)

        drawScore(len(wormCoords) - 3)
        pygame.display.update()

        # брза проверка ја најдов на интернет
        if time.time() - FPS_INCREASE >= 10:
            # слично како тајмерите од 3: проверуваме дали разликата е поголема на времето сега и на тоа од почнување
            # ако е поголемо од 30 (поминале 30 секунди)
            temp_FPS = FPS   # чувај ја последната брзина за барање 4
            FPS += 10  # зголеми FPS за 10 frames per second
            worm_color = random.choice(worm_shades)
            FPS_INCREASE = time.time()
            # слично како кај 3 почетното време постави го пак да биде сегашното (т.е. референтно)

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


def showGameOverScreen():
    global FPS
    FPS = 6  # reset the FPS after the game restarts

    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    text = f'BLUE APPLES: Decrease the FPS (good for you)'
    blueSurf = BASICFONT.render(text, True, BLUE)
    blueRect = blueSurf.get_rect()
    blueRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25 + 185)
    DISPLAYSURF.blit(blueSurf, blueRect)

    text = f'YELLOW APPLES: Decrease score (bad for you)'
    yellowSurf = BASICFONT.render(text, True, YELLOW)
    yellowRect = yellowSurf.get_rect()
    yellowRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25 + 225)
    DISPLAYSURF.blit(yellowSurf, yellowRect)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()


    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

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
def appleTimers(counter, seconds, start_ticks, flag, which):
    # yellow apple: timer 9s
    if which == 'yellow':
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
    # blue apple: timer 15s
    else:
        # HIDDEN: криј го јаболкото
        if flag == 'hidden':
            # 1 проверка: дали тајмерот истече
            if seconds == counter:
                # да, истече
                text = ''
                # испиши текст горе десно под score
                blueSurf = BASICFONT.render(text, True, WHITE)
                blueRect = blueSurf.get_rect()
                blueRect.topleft = (WINDOWWIDTH - 300, 40)
                DISPLAYSURF.blit(blueSurf, blueRect)
                # ресетирај бројач на 15. значи 15 секунди има 15 нема. Тука може да се оди со random.randint(1,10)
                counter = 15
                # најбитно: ресетирај го почетното време на бројачот
                start_ticks = pygame.time.get_ticks()
                # смени знаме на shown за кога ќе излезе да почне да го покажува
                flag = 'shown'
                # врати вредности
                return counter, start_ticks, flag
            else:
                # не е истечен сеуште, започни тајмер (descending) за кога е следното
                display_timer = counter - seconds
                # испиши текст горе десно под score
                text = f'Blue apple appears in: {str(display_timer)}'
                blueSurf = BASICFONT.render(text, True, WHITE)
                blueRect = blueSurf.get_rect()
                blueRect.topleft = (WINDOWWIDTH - 282, 40)
                DISPLAYSURF.blit(blueSurf, blueRect)
                # врати вредности
                return counter, start_ticks, flag

        # SHOWN: покажувај јаболко
        else:
            # 1 проверка: дали тајмерот истече
            if seconds == counter:
                # да, истече
                text = ''
                # испиши текст горе десно под score
                blueSurf = BASICFONT.render(text, True, WHITE)
                blueRect = blueSurf.get_rect()
                blueRect.topleft = (WINDOWWIDTH - 300, 40)
                DISPLAYSURF.blit(blueSurf, blueRect)
                # ресетирај бројач на 15. значи 15 секунди има 15 нема. Тука може да се оди со random.randint(1,10)
                counter = 15
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
                text = f'Blue apples disappear in: {str(display_timer)}'
                blueSurf = BASICFONT.render(text, True, WHITE)
                blueRect = blueSurf.get_rect()
                blueRect.topleft = (WINDOWWIDTH - 300, 40)
                DISPLAYSURF.blit(blueSurf, blueRect)
                # врати вредности
                return counter, start_ticks, flag


def drawWorm(wormCoords, color_shade=GREENS_tuple):
    DARK_color = color_shade[0]
    LIGHT_color = color_shade[1]
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARK_color, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, LIGHT_color, wormInnerSegmentRect)


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