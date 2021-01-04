"""

 Created on 24-Dec-20
 @author: Kiril Zelenkovski

"""

import random, sys, time, pygame
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 800  # смени ширина
WINDOWHEIGHT = 500 # смени висина
FLASHSPEED = 500  # in milliseconds
FLASHDELAY = 200  # in milliseconds
BUTTONSIZE = 100
BUTTONGAPSIZE = 20
TIMEOUT = 5 # seconds before game over if no button is pushed.

#                R    G    B
WHITE        = (255, 255, 255)
BLACK        = (  0,   0,   0)
BRIGHTRED    = (200,   0,   0)  # 1ва боја: RED1
RED          = (100,   0,   0)  # 1ва посветла боја: RED2
BRIGHTGREEN  = (  0, 200,   0)  # 2ра боја: GREEN1
GREEN        = (  0, 100,   0)  # 2ра посветла боја: GREEN2
BRIGHTBLUE   = (  0,   0, 200)  # 3та боја: BLUE1
BLUE         = (  0,   0, 100)  # 3та посветла боја: BLUE2
BRIGHTYELLOW = (200, 200,   0)  # 4та боја: YELLOW1
YELLOW       = (100, 100,   0)  # 4та посветла боја: YELLOW2
BRIGHTPURPLE = ( 75,   0, 130)  # 5та боја: PURPLE1
PURPLE       = (186,  85, 211)  # 5та посветла боја: PURPLE2
BRIGHTORANGE = (255, 140,  0)   # 6та боја: ORANGE1
ORANGE       = (255, 165,  0)   # 6та посветла боја: ORANGE2
DARKGRAY     = ( 40,  40,  40)
bgColor = BLACK

XMARGIN = int((WINDOWWIDTH - (1 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)
# 1 ниво
YELLOWRECT = pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
REDRECT    = pygame.Rect(XMARGIN, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
# 2 ниво
BLUERECT   = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE)
GREENRECT  = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
# 3 ниво
ORANGERECT  = pygame.Rect(XMARGIN + BUTTONSIZE*2 + BUTTONGAPSIZE*2, YMARGIN, BUTTONSIZE, BUTTONSIZE)
PURPLERECT   = pygame.Rect(XMARGIN + BUTTONSIZE*2 + BUTTONGAPSIZE*2, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BEEP1, BEEP2, BEEP3, BEEP4, BEEP5, BEEP6
    global TIMEOUT, XMARGIN, level, color_list
    global YELLOWRECT, REDRECT, BLUERECT, GREENRECT, ORANGERECT, PURPLERECT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Simulate')

    BASICFONT = pygame.font.Font('freesansbold.ttf', 16)
    infoSurf = BASICFONT.render('Match the pattern by clicking on the button or using the first symbol of the color Y, R, B, G, O, P keys.', 1, DARKGRAY)
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (10, WINDOWHEIGHT - 25)

    # load the sound files
    BEEP1 = pygame.mixer.Sound('beep1.ogg')
    BEEP2 = pygame.mixer.Sound('beep2.ogg')
    BEEP3 = pygame.mixer.Sound('beep3.ogg')
    BEEP4 = pygame.mixer.Sound('beep4.ogg')
    BEEP5 = pygame.mixer.Sound('beep1.ogg')  # нов звук за копче (исиот со 1)
    BEEP6 = pygame.mixer.Sound('beep2.ogg')  # нов звук за копче (исиот со 2)

    # Initialize some variables for a new game
    pattern = [] # stores the pattern of colors
    currentStep = 0 # the color the player must push next
    lastClickTime = 0 # timestamp of the player's last button push
    score = 0
    # when False, the pattern is playing. when True, waiting for the player to click a colored button:
    waitingForInput = False
    # step counter
    counter = 1
    # листа за бои
    color_list = [YELLOW, RED]
    # бројач за нивоа
    level = 0
    while True: # main game loop
        clickedButton = None # button that was clicked (set to YELLOW, RED, GREEN, or BLUE)
        DISPLAYSURF.fill(bgColor)
        drawButtons(level)

        scoreSurf = BASICFONT.render('Score: ' + str(score), 1, WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH - 100, 10)
        DISPLAYSURF.blit(scoreSurf, scoreRect)

        levelSurf = BASICFONT.render('Level: ' + str(level), 1, WHITE)
        levelRect = scoreSurf.get_rect()
        levelRect.topleft = (WINDOWWIDTH - 98, 25)
        DISPLAYSURF.blit(levelSurf, levelRect)

        DISPLAYSURF.blit(infoSurf, infoRect)

        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                clickedButton = getButtonClicked(mousex, mousey, level)
            elif event.type == KEYDOWN:
                if event.key == K_y:
                    clickedButton = YELLOW
                elif event.key == K_r:
                    clickedButton = RED
                elif event.key == K_b:
                    clickedButton = BLUE
                elif event.key == K_g:
                    clickedButton = GREEN
                elif event.key == K_o:
                    clickedButton = ORANGE
                elif event.key == K_p:
                    clickedButton = PURPLE



        if not waitingForInput:
            # play the pattern
            pygame.display.update()
            pygame.time.wait(1000)

            ################################################################################################### Барање 1
            pattern = []
            for c in range(0, counter):
                pattern.append(random.choice(tuple(color_list)))
            ############################################################################################################

            # Коментирано доколку сакаме да го следиме редоследот
            # pattern.append(random.choice(tuple(color_list)))
            for button in pattern:
                flashButtonAnimation(button)
                pygame.time.wait(FLASHDELAY)
            waitingForInput = True
        else:
            # wait for the player to enter buttons
            if clickedButton and clickedButton == pattern[currentStep]:
                # pushed the correct button
                flashButtonAnimation(clickedButton)
                currentStep += 1
                lastClickTime = time.time()

                if currentStep == len(pattern):
                    # pushed the last button in the pattern
                    changeBackgroundAnimation()
                    score += 1
                    waitingForInput = False
                    currentStep = 0 # reset back to first step
                    counter += 1

                ############################################################################################### Барање 2
                # if len(pattern) % 10 == 0 and TIMEOUT > 2:
                #     TIMEOUT -= 1
                ########################################################################################################

                ############################################################################################### Барање 3
                # if 11 <= score <= 20:
                if 3 <= score <= 5:
                    level = 1
                    XMARGIN = int((WINDOWWIDTH - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)  # 1+1 = 2
                    color_list.append(GREEN)
                    color_list.append(BLUE)
                    YELLOWRECT = pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
                    REDRECT = pygame.Rect(XMARGIN, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
                    BLUERECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE)
                    GREENRECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE,
                                            BUTTONSIZE, BUTTONSIZE)

                # elif 21 <= score <= 30:
                elif 6 <= score <= 8:
                    level = 2
                    XMARGIN = int((WINDOWWIDTH - (3 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)  # 2+1 = 3
                    color_list.append(ORANGE)
                    color_list.append(PURPLE)
                    YELLOWRECT = pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
                    REDRECT = pygame.Rect(XMARGIN, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
                    BLUERECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE)
                    GREENRECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE,
                                            BUTTONSIZE, BUTTONSIZE)
                    ORANGERECT = pygame.Rect(XMARGIN + BUTTONSIZE * 2 + BUTTONGAPSIZE * 2, YMARGIN, BUTTONSIZE,
                                             BUTTONSIZE)
                    PURPLERECT = pygame.Rect(XMARGIN + BUTTONSIZE * 2 + BUTTONGAPSIZE * 2,
                                             YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)

                ########################################################################################################

            elif (clickedButton and clickedButton != pattern[currentStep]) or (currentStep != 0 and time.time() - TIMEOUT > lastClickTime):
                # pushed the incorrect button, or has timed out
                gameOverAnimation()
                # reset the variables for a new game:
                pattern = []
                currentStep = 0
                waitingForInput = False
                score = 0
                # ресетирај бројач
                counter = 1
                # ресетирај ниво
                level = 0
                # ресетирај листа од бои
                color_list = [YELLOW, RED]
                # врати се на првобитната маргина
                XMARGIN = int((WINDOWWIDTH - (1 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)
                # пресметај ги од ново правоагонлиците за жолто и црвено бидејќи маргината ја смени
                YELLOWRECT = pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
                REDRECT = pygame.Rect(XMARGIN, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
                pygame.time.wait(1000)
                changeBackgroundAnimation()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back


def flashButtonAnimation(color, animationSpeed=50):
    if color == YELLOW:
        sound = BEEP1
        flashColor = BRIGHTYELLOW
        rectangle = YELLOWRECT
    elif color == RED:
        sound = BEEP2
        flashColor = BRIGHTRED
        rectangle = REDRECT
    elif color == BLUE:
        sound = BEEP3
        flashColor = BRIGHTBLUE
        rectangle = BLUERECT
    elif color == GREEN:
        sound = BEEP4
        flashColor = BRIGHTGREEN
        rectangle = GREENRECT
    elif color == ORANGE:
        sound = BEEP5
        flashColor = BRIGHTORANGE
        rectangle = ORANGERECT
    elif color == PURPLE:
        sound = BEEP6
        flashColor = BRIGHTPURPLE
        rectangle = PURPLERECT

    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface((BUTTONSIZE, BUTTONSIZE))
    flashSurf = flashSurf.convert_alpha()
    r, g, b = flashColor
    sound.play()
    for start, end, step in ((0, 255, 1), (255, 0, -1)): # animation loop
        for alpha in range(start, end, animationSpeed * step):
            checkForQuit()
            DISPLAYSURF.blit(origSurf, (0, 0))
            flashSurf.fill((r, g, b, alpha))
            DISPLAYSURF.blit(flashSurf, rectangle.topleft)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
    DISPLAYSURF.blit(origSurf, (0, 0))


def drawButtons(level):
    if level == 0:
        pygame.draw.rect(DISPLAYSURF, YELLOW, YELLOWRECT)
        pygame.draw.rect(DISPLAYSURF, RED,    REDRECT)
    elif level == 1:
        pygame.draw.rect(DISPLAYSURF, YELLOW, YELLOWRECT)
        pygame.draw.rect(DISPLAYSURF, RED, REDRECT)
        pygame.draw.rect(DISPLAYSURF, BLUE,   BLUERECT)
        pygame.draw.rect(DISPLAYSURF, GREEN,  GREENRECT)
    elif level > 1:
        pygame.draw.rect(DISPLAYSURF, YELLOW, YELLOWRECT)
        pygame.draw.rect(DISPLAYSURF, RED, REDRECT)
        pygame.draw.rect(DISPLAYSURF, BLUE, BLUERECT)
        pygame.draw.rect(DISPLAYSURF, GREEN, GREENRECT)
        pygame.draw.rect(DISPLAYSURF, ORANGE, ORANGERECT)
        pygame.draw.rect(DISPLAYSURF, PURPLE, PURPLERECT)



def changeBackgroundAnimation(animationSpeed=40):
    global bgColor
    newBgColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    newBgSurf = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
    newBgSurf = newBgSurf.convert_alpha()
    r, g, b = newBgColor
    for alpha in range(0, 255, animationSpeed): # animation loop
        checkForQuit()
        DISPLAYSURF.fill(bgColor)

        newBgSurf.fill((r, g, b, alpha))
        DISPLAYSURF.blit(newBgSurf, (0, 0))

        drawButtons(level) # redraw the buttons on top of the tint

        pygame.display.update()
        FPSCLOCK.tick(FPS)
    bgColor = newBgColor


def gameOverAnimation(color=WHITE, animationSpeed=50):
    # play all beeps at once, then flash the background
    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface(DISPLAYSURF.get_size())
    flashSurf = flashSurf.convert_alpha()
    BEEP1.play() # play all four beeps at the same time, roughly.
    BEEP2.play()
    BEEP3.play()
    BEEP4.play()
    level = 0
    r, g, b = color
    for i in range(3): # do the flash 3 times
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            # The first iteration in this loop sets the following for loop
            # to go from 0 to 255, the second from 255 to 0.
            for alpha in range(start, end, animationSpeed * step): # animation loop
                # alpha means transparency. 255 is opaque, 0 is invisible
                checkForQuit()
                flashSurf.fill((r, g, b, alpha))
                DISPLAYSURF.blit(origSurf, (0, 0))
                DISPLAYSURF.blit(flashSurf, (0, 0))
                drawButtons(level)
                pygame.display.update()
                FPSCLOCK.tick(FPS)



def getButtonClicked(x, y, level):
    if level == 0:
        if YELLOWRECT.collidepoint( (x, y) ):
            return YELLOW
        elif REDRECT.collidepoint( (x, y) ):
            return RED

    elif level == 1:
        if YELLOWRECT.collidepoint( (x, y) ):
            return YELLOW
        elif REDRECT.collidepoint( (x, y) ):
            return RED
        elif BLUERECT.collidepoint( (x, y) ):
            return BLUE
        elif GREENRECT.collidepoint( (x, y) ):
            return GREEN

    elif level > 1:
        if YELLOWRECT.collidepoint( (x, y) ):
            return YELLOW
        elif REDRECT.collidepoint( (x, y) ):
            return RED
        elif BLUERECT.collidepoint( (x, y) ):
            return BLUE
        elif GREENRECT.collidepoint( (x, y) ):
            return GREEN
        elif ORANGERECT.collidepoint((x, y)):
            return ORANGE
        elif PURPLERECT.collidepoint((x, y)):
            return PURPLE

    return None


if __name__ == '__main__':
    main()
