"""

 Created on 25-Dec-20
 @author: Kiril Zelenkovski

"""

# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys
from pygame.locals import *

FPS = 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
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
YELLOW    = pygame.color.Color('yellow')

# Трошки боја
GLAUCOUS = ( 96, 130, 182)

# Втор црв: темно и светло плава
DARKBLUE =  (  0, 128, 255)
LIGHTBLUE = (204, 229, 255)

BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

directions = [UP, DOWN, LEFT, RIGHT]
directions_dict = {'left': LEFT, 'down': DOWN, 'right':RIGHT, 'up':UP}
HEAD = 0  # syntactic sugar: index of the worm's head
HEAD2 = 0  # глава на вториот црв

show_flag = True

def main(flag=True):
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')

    if flag:
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

    wormCoords2 = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]

    direction = RIGHT
    direction2 = LEFT
    # дефинирај глава на втор црв
    HEAD2 = 0

    # Тајмер црв
    start_ticks_worm = pygame.time.get_ticks()  # start ticks црв
    counter = 45  # додај бројач за нов црв 45сек
    flag = 'hidden'  # знаме за црв; 'hidden'-скриено, 'shown'-прикажано

    # Тајмер елементи
    start_ticks_ele = pygame.time.get_ticks()  # start ticks елементи
    counter_elements = 5 # додај бројач за елементи 5сек
    flag_elements = 'hidden'


    # Start the apple in a random place.
    apple = getRandomLocation()

    # дефиниција на елементи
    point_element1 = getRandomLocation()  # креирам прв елемент за плус поени
    point_element2 = getRandomLocation()  # креирам прв елемент за плус поени
    point_element3 = getRandomLocation()  # креирам прв елемент за плус поени

    # минусирање од резултат
    score_sub = 0
    # плус поени за резултат
    score_plu = 0

    while True: # main game loop
        # земи време за црв
        seconds_worm = (pygame.time.get_ticks() - start_ticks_worm) / 1000
        seconds_worm = int(seconds_worm)
        # земи време за елементи
        seconds_ele = (pygame.time.get_ticks() - start_ticks_ele ) / 1000
        seconds_ele = int(seconds_ele)


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
        if wormCoords[HEAD]['x'] == -1 \
                or wormCoords[HEAD]['x'] == CELLWIDTH \
                or wormCoords[HEAD]['y'] == -1 \
                or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return # game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return # game over



        if flag == 'shown':
            flag_direction = True
            while flag_direction:
                direction2 = random.choice(directions)
                # најлево
                position_x = wormCoords2[0]['x']
                position_y = wormCoords2[0]['y']
                # најлево
                if direction2 == 'left' and position_x == 0:  # најлево
                    if position_y == 0:  # најлево, најдолу
                        direction2 = UP
                        break
                    elif position_y == (CELLHEIGHT-1):  # најлево, најгоре
                        direction2 = DOWN
                        break
                    else:  # најлево, но некаде на средина во игра
                        direction2 = random.choice([UP, DOWN])
                        direction2 = directions_dict[direction2]
                        break
                # најдесно
                elif direction2 == 'right' and position_x == (CELLWIDTH-1):  # најдесно
                    if position_y == 0:  # најдесно, најдолу
                        direction2 = UP
                        break
                    elif position_y == (CELLHEIGHT-1):  # најдесно, најгоре
                        direction2 = DOWN
                        break
                    else:  # најдесно, но некаде на средина во висина
                        direction2 = random.choice([UP, DOWN])
                        direction2 = directions_dict[direction2]
                        break
                # најгоре
                elif direction2 == 'up' and position_y == 0:  # најгоре
                    if position_x == 0:  # најгоре, најлево
                        direction2 = RIGHT
                        break
                    elif position_x == (CELLWIDTH-1): # најгоре, најдесно
                        direction2 = LEFT
                        break
                    else:
                        direction2 = random.choice([LEFT, RIGHT])
                        direction2 = directions_dict[direction2]
                        break
                # најдолу
                elif direction2 == 'down' and position_y == (CELLHEIGHT-1):   # најдолу
                    if position_x == 0:  # најдолу, најлево
                        direction2 = RIGHT
                        break
                    elif position_x == (CELLWIDTH-1):  # најдолу, најдесно
                        direction2 = LEFT
                        break
                    else:
                        direction2 = random.choice([LEFT, RIGHT])
                        direction2 = directions_dict[direction2]
                        break

                    # ако нема конфликтни ситуации, врати ја вредноста што е доделена прва
                direction2 = directions_dict[direction2]
                flag_direction = False

        jump_flag = False  # знаме за проверка дали 2 црв го допира 1
        for wormBody in wormCoords:  # врти ги сите сегменти на прв црв
            for wormBody2 in wormCoords2:  # врти ги сите сегменти на втор црв
                if wormBody['x'] == wormBody2['x'] and wormBody['y'] == wormBody2['y']:  # проверка
                    jump_flag = True
                    break
            if jump_flag:
                break

        hit_flag = False  # знаме за проверка дали 1 црв го допира 2 (некаде по телото)
        for wormBody in wormCoords2:
            if wormCoords[HEAD]['x'] == wormBody['x'] and wormCoords[HEAD]['y'] == wormBody['y']:
                hit_flag = True
                break


        # проверки за колизии
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation() # set a new apple somewhere

        elif flag == 'shown' and jump_flag:  # проверка дали 2 го допира прв било каде
            if hit_flag: # тука уствари и 2та црва се доприаат, 1иот со глава, другиот со било кој сегмент
                # pass  # двата црва растат за сегмент
                score_sub += 1
            else:
                del wormCoords[-1]  # 2иот го допира 1иот продолжуваме за 1, но 1иот се намалува

        elif flag == 'shown':
            del wormCoords[-1]
            del wormCoords2[-1]  # remove worm's tail segment

        else:
            del wormCoords[-1]


        # Проверки за плус елементи
        if wormCoords[HEAD]['x'] == point_element1['x'] and wormCoords[HEAD]['y'] == point_element1['y']:
            score_plu += 1
            point_element1 = getRandomLocation()  # го изел првиот елемент, додели нова локација

        elif wormCoords[HEAD]['x'] == point_element2['x'] and wormCoords[HEAD]['y'] == point_element2['y']:
            score_plu += 1
            point_element2 = getRandomLocation()  # го изел вториот елемент, додели нова локација

        elif wormCoords[HEAD]['x'] == point_element3['x'] and wormCoords[HEAD]['y'] == point_element3['y']:
            score_plu += 1
            point_element3 = getRandomLocation()  # го изел третиот елемент, додели нова локација

        # Прв црв движење
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}

        if flag == 'shown':
            # Втор црв движење
            if direction2 == UP:
                newHead2 = {'x': wormCoords2[HEAD2]['x'], 'y': wormCoords2[HEAD2]['y'] - 1}
            elif direction2 == DOWN:
                newHead2 = {'x': wormCoords2[HEAD2]['x'], 'y': wormCoords2[HEAD2]['y'] + 1}
            elif direction2 == LEFT:
                newHead2 = {'x': wormCoords2[HEAD2]['x'] - 1, 'y': wormCoords2[HEAD2]['y']}
            elif direction2 == RIGHT:
                newHead2 = {'x': wormCoords2[HEAD2]['x'] + 1, 'y': wormCoords2[HEAD2]['y']}


        wormCoords.insert(0, newHead)


        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawApple(apple)


        if flag == 'shown':
            wormCoords2.insert(0, newHead2)
            drawWorm(wormCoords2, DARKBLUE, LIGHTBLUE)
            # print(wormCoords2)

        if flag_elements == 'shown':
            drawApple(point_element1, GLAUCOUS)
            drawApple(point_element2, GLAUCOUS)
            drawApple(point_element3, GLAUCOUS)

        # 45 секунди за втор црв функција
        counter, start_ticks_worm, flag = drawSecondWormTime(counter,
                                                             seconds_worm,
                                                             start_ticks_worm,
                                                             flag)
        # 5s on / 5s off
        counter_elements, start_ticks_ele, flag_elements = drawElementsTime(counter_elements,
                                                                            seconds_ele,
                                                                            start_ticks_ele,
                                                                            flag_elements)
        # пресметај резултат: барање 2
        drawScore(len(wormCoords) - 3 - score_sub + score_plu*2)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

# Главна функција за втор црв
def drawSecondWormTime(counter, seconds, start_ticks, flag):
    # HIDDEN: криј го црвот
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
            # ресетирај бројач на 45. значи 45 секунди нема, потоа цело време е тука
            counter = 45
            # најбитно: ресетирај го почетното време на бројачот за game over
            start_ticks = pygame.time.get_ticks()
            # смени знаме на shown за кога ќе излезе да почне да го покажува
            flag = 'shown'
            # врати вредности
            return counter, start_ticks, flag
        else:
            # не е истечен сеуште, започни тајмер (descending) за кога е следното
            display_timer = counter-seconds
            # испиши текст горе десно под score
            text = f'Blue worm in: {str(display_timer)}s'
            yellowSurf = BASICFONT.render(text, True, WHITE)
            yellowRect = yellowSurf.get_rect()
            yellowRect.topleft = (WINDOWWIDTH - 180, 25)
            DISPLAYSURF.blit(yellowSurf, yellowRect)
            # врати вредности
            return counter, start_ticks, flag

    else:
        text = f'Avoid worm!'
        yellowSurf = BASICFONT.render(text, True, DARKBLUE)
        yellowRect = yellowSurf.get_rect()
        yellowRect.topleft = (WINDOWWIDTH - 140, 25)
        DISPLAYSURF.blit(yellowSurf, yellowRect)
        # врати вредности
        return counter, start_ticks, flag


# Главна функција за цртање елементи за плус поени
def drawElementsTime(counter, seconds, start_ticks, flag):

    # HIDDEN: криј го јаболкото
    if flag == 'hidden':
        # 1 проверка: дали тајмерот истече
        if seconds == counter:
            # да, истече
            text = ''
            # испиши текст горе десно под score
            textSurf = BASICFONT.render(text, True, GLAUCOUS)
            textRect = textSurf.get_rect()
            textRect.topleft = (WINDOWWIDTH - 300, 40)
            DISPLAYSURF.blit(textSurf, textRect)
            # ресетирај бројач на 5. значи 5 секунди има 5 нема
            counter = 5
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
            text = f'Elements appear:   {str(display_timer)}s'
            textSurf = BASICFONT.render(text, True, WHITE)
            textRect = textSurf.get_rect()
            textRect.topleft = (WINDOWWIDTH - 220, 40)
            DISPLAYSURF.blit(textSurf, textRect)
            # врати вредности
            return counter, start_ticks, flag

    # SHOWN: покажувај јаболко
    else:
        # 1 проверка: дали тајмерот истече
        if seconds == counter:
            # да, истече
            text = ''
            # испиши текст горе десно под score
            textSurf = BASICFONT.render(text, True, WHITE)
            textRect = textSurf.get_rect()
            textRect.topleft = (WINDOWWIDTH - 300, 40)
            DISPLAYSURF.blit(textSurf, textRect)
            # ресетирај бројач на 5. значи 5 секунди има 5 нема. Тука може да се оди со random.randint(1,10)
            counter = 5
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
            text = f'Elements disappear:{str(display_timer)}s'
            textSurf = BASICFONT.render(text, True, GLAUCOUS)
            textRect = textSurf.get_rect()
            textRect.topleft = (WINDOWWIDTH - 220, 40)
            DISPLAYSURF.blit(textSurf, textRect)
            # врати вредности
            return counter, start_ticks, flag


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

    startRect.midtop = (WINDOWWIDTH / 2, 320)
    quitRect.midtop = (WINDOWWIDTH / 2, 360)

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
            if checkForKeyPress():
                pygame.event.get() # clear event queue
                return

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords, colorOutside=DARKGREEN, colorIniside=GREEN):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, colorOutside, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, colorIniside, wormInnerSegmentRect)


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