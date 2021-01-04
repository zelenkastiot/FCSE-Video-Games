"""

 Created on 15-Nov-20
 @author: Kiril Zelenkovski

"""

import pygame
import random
import sys
from pygame.locals import *

############################################################################################################### Барање 1
BOARDWIDTH = 4  # number of columns in the board is changed to 4
BOARDHEIGHT = 3  # number of rows in the board is changed to 3
########################################################################################################################

TILESIZE = 90
WINDOWWIDTH = 800  # add new width to fit 8x8 board
WINDOWHEIGHT = 700  # add new height to fit 8x8 board
FPS = 30
BLANK = None

#                 R    G    B
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BRIGHTBLUE = (0, 50, 255)
DARKTURQUOISE = (3, 54, 73)
GREEN = (0, 204, 0)
YELLOW = pygame.Color('yellow')  # add color yellow
BLUE = pygame.Color('blue')  # add color blue

BGCOLOR = DARKTURQUOISE
TILECOLOR = YELLOW  # change tile color
TEXTCOLOR = BLACK  # also changed the text color to black, for better readability
BORDERCOLOR = BLUE  # change background color
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT, my_moves


    pygame.init()   
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Slide Puzzle')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    # Store the option buttons and their rectangles in OPTIONS.
    RESET_SURF, RESET_RECT = makeText('Reset', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 120)
    NEW_SURF, NEW_RECT = makeText('New Game', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
    SOLVE_SURF, SOLVE_RECT = makeText('Solve', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)

    global HELP_SURF, HELP_RECT, COMBINE_SURF, COMBINE_RECT, PLAYER_SURF, PLAYER_RECT
    HELP_SURF, HELP_RECT = makeText('HELP', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 30)

    mainBoard, solutionSeq = generateNewPuzzle(random.randint(1, 100))
    SOLVEDBOARD = getStartingBoard()  # a solved board is the same as the board in a start state.
    allMoves = []  # list of moves made from the solved configuration
    my_moves = 0

    ################################################################################################ БАРАЊЕ 3. ВЕРЗИЈА 2

    while True:  # main game loop
        slideTo = None  # the direction, if any, a tile should slide
        msg = 'Click tile or press arrow keys to slide.'  # contains the message to show in the upper left corner.
        text_lists = []
        if mainBoard == SOLVEDBOARD:
            msg = 'Solved!'
            # Додади листа од текстови за копчиња
            text_com = f'Combined moves: {my_moves + len(solutionSeq)}'  # текст за чекори од компјутер
            text_player = f'Player moves: {my_moves}'  # текст за чекори од играч
            text_lists.append(text_com)
            text_lists.append(text_player)

        drawBoard(mainBoard, msg, text_lists)

    ####################################################################################################################

        checkForQuit()
        for event in pygame.event.get():  # event handling loop
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])

                if (spotx, spoty) == (None, None):
                    # check if the user clicked on an option button
                    if RESET_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, allMoves)  # clicked on Reset button
                        allMoves = []
                    elif NEW_RECT.collidepoint(event.pos):
                        mainBoard, solutionSeq = generateNewPuzzle(random.randint(1, 100))  # clicked on New Game button
                        allMoves = []
                    elif SOLVE_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, solutionSeq + allMoves)  # clicked on Solve button
                        allMoves = []
                    elif HELP_RECT.collidepoint(event.pos):  ###################################################### HELP
                        help_timer(mainBoard, msg)  # Повикуваме главна функција за помош
                else:
                    # check if the clicked tile was next to the blank spot

                    blankxpos, blankypos = getBlankPosition(mainBoard)
                    if spotx == blankxpos + 1 and spoty == blankypos:
                        slideTo = LEFT
                    elif spotx == blankxpos - 1 and spoty == blankypos:
                        slideTo = RIGHT
                    elif spotx == blankxpos and spoty == blankypos + 1:
                        slideTo = UP
                    elif spotx == blankxpos and spoty == blankypos - 1:
                        slideTo = DOWN

            elif event.type == KEYUP:
                # check if the user pressed a key to slide a tile
                if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT):
                    slideTo = LEFT
                elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):
                    slideTo = RIGHT
                elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):
                    slideTo = UP
                elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWN):
                    slideTo = DOWN

        if slideTo:
            slideAnimation(mainBoard, slideTo, 'Click tile or press arrow keys to slide.', 8)  # show slide on screen
            makeMove(mainBoard, slideTo)
            allMoves.append(slideTo)  # record the slide
            my_moves = len(allMoves)  # чувај си чекорите до тогаш за да не ги изгубиш

#################################################################################################### БАРАЊЕ 3. ВЕРЗИЈА 1
        # text_com = f'Combined moves: {len(allMoves) + len(solutionSeq)}'   # текст за сите чекори
        # COMBINE_SURF, COMBINE_RECT = makeText(text_com, TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 800, WINDOWHEIGHT - 90)
        #
        # text_player = f'Player moves: {len(allMoves)}'  # текст за чекори од играч
        # PLAYER_SURF, PLAYER_RECT = makeText(text_player, TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 800, WINDOWHEIGHT - 60)
        #
        # DISPLAYSURF.blit(COMBINE_SURF, COMBINE_RECT)
        # DISPLAYSURF.blit(PLAYER_SURF, PLAYER_RECT)
#######################################################################################################################

        pygame.display.update()
        pygame.time.Clock().tick(1)

def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT):  # get all the QUIT events
        terminate()  # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP):  # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate()  # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event)  # put the other KEYUP event objects back


def getStartingBoard():
    # Return a board data structure with tiles in the solved state.
    # For example, if BOARDWIDTH and BOARDHEIGHT are both 3, this function
    # returns [[1, 4, 7], [2, 5, 8], [3, 6, BLANK]]
    counter = 1
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(counter)
            counter += BOARDWIDTH
        board.append(column)
        counter -= BOARDWIDTH * (BOARDHEIGHT - 1) + BOARDWIDTH - 1

    board[BOARDWIDTH - 1][BOARDHEIGHT - 1] = BLANK
    return board


def getBlankPosition(board):
    # Return the x and y of board coordinates of the blank space.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == BLANK:
                return (x, y)


def makeMove(board, move):
    # This function does not check if the move is valid.
    blankx, blanky = getBlankPosition(board)

    if move == UP:
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]


def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0]) - 1) or \
           (move == DOWN and blanky != 0) or \
           (move == LEFT and blankx != len(board) - 1) or \
           (move == RIGHT and blankx != 0)


def getRandomMove(board, lastMove=None):
    # start with a full list of all four moves
    validMoves = [UP, DOWN, LEFT, RIGHT]

    # remove moves from the list as they are disqualified
    if lastMove == UP or not isValidMove(board, DOWN):
        validMoves.remove(DOWN)
    if lastMove == DOWN or not isValidMove(board, UP):
        validMoves.remove(UP)
    if lastMove == LEFT or not isValidMove(board, RIGHT):
        validMoves.remove(RIGHT)
    if lastMove == RIGHT or not isValidMove(board, LEFT):
        validMoves.remove(LEFT)

    # return a random move from the list of remaining moves
    return random.choice(validMoves)


def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)


def getSpotClicked(board, x, y):
    # from the x & y pixel coordinates, get the x & y board coordinates
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)


def drawTile(tilex, tiley, number, adjx=0, adjy=0):
    # draw a tile at board coordinates tilex and tiley, optionally a few
    # pixels over (determined by adjx and adjy)
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect)


def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)


def drawBoard(board, message, texts=[]):
    DISPLAYSURF.fill(BGCOLOR)
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)

        # Ако е пораката SOLVED испиши ги чекорите потребни и од играчот и од компјутерот
        if message == 'Solved!':
            text_com = texts[0]
            COMBINE_SURF, COMBINE_RECT = makeText(text_com, TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 800, WINDOWHEIGHT - 90)

            text_player = texts[1]
            PLAYER_SURF, PLAYER_RECT = makeText(text_player, TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 800, WINDOWHEIGHT - 60)

            DISPLAYSURF.blit(COMBINE_SURF, COMBINE_RECT)
            DISPLAYSURF.blit(PLAYER_SURF, PLAYER_RECT)
            pygame.display.update()

    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])

    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)

    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)
    # Цртај HELP копче
    DISPLAYSURF.blit(HELP_SURF, HELP_RECT)


def slideAnimation(board, direction, message, animationSpeed):
    # Note: This function does not check if the move is valid.

    blankx, blanky = getBlankPosition(board)
    if direction == UP:
        movex = blankx
        movey = blanky + 1
    elif direction == DOWN:
        movex = blankx
        movey = blanky - 1
    elif direction == LEFT:
        movex = blankx + 1
        movey = blanky
    elif direction == RIGHT:
        movex = blankx - 1
        movey = blanky

    # prepare the base surface
    drawBoard(board, message)
    baseSurf = DISPLAYSURF.copy()
    # draw a blank space over the moving tile on the baseSurf Surface.
    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))

    for i in range(0, TILESIZE, animationSpeed):
        # animate the tile sliding over
        checkForQuit()
        DISPLAYSURF.blit(baseSurf, (0, 0))
        if direction == UP:
            drawTile(movex, movey, board[movex][movey], 0, -i)
        if direction == DOWN:
            drawTile(movex, movey, board[movex][movey], 0, i)
        if direction == LEFT:
            drawTile(movex, movey, board[movex][movey], -i, 0)
        if direction == RIGHT:
            drawTile(movex, movey, board[movex][movey], i, 0)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generateNewPuzzle(numSlides):
    # From a starting configuration, make numSlides number of moves (and
    # animate these moves).
    sequence = []
    board = getStartingBoard()
    drawBoard(board, '')
    pygame.display.update()
    pygame.time.wait(500)  # pause 500 milliseconds for effect
    lastMove = None
    for i in range(numSlides):
        move = getRandomMove(board, lastMove)
        # Change from TILESIZE/3 to TILESIZE/3, same as speed when solving #L331
        slideAnimation(board, move, 'Generating new puzzle...', animationSpeed=int(TILESIZE / 2))
        makeMove(board, move)
        sequence.append(move)
        lastMove = move
    return (board, sequence)


def resetAnimation(board, allMoves):
    # make all of the moves in allMoves in reverse.
    revAllMoves = allMoves[:]  # gets a copy of the list
    revAllMoves.reverse()

    for move in revAllMoves:
        if move == UP:
            oppositeMove = DOWN
        elif move == DOWN:
            oppositeMove = UP
        elif move == RIGHT:
            oppositeMove = LEFT
        elif move == LEFT:
            oppositeMove = RIGHT
        slideAnimation(board, oppositeMove, '', animationSpeed=int(TILESIZE / 2))
        makeMove(board, oppositeMove)

######################################################################################################## БАРАЊЕ 2

# Функија 1: Цртање на tiles црвени, може да се модифицира е обичната со цел да ставаме боја како аргумент исто така
def drawHelpTile(tilex, tiley, number, adjx=0, adjy=0):
    left, top = getLeftTopOfTile(tilex, tiley)
    # Променуваме бојата да биде "red" од главната функција сите други редови се исти од обичната drawTile()
    pygame.draw.rect(DISPLAYSURF, pygame.Color('red'), (left + adjx, top + adjy, TILESIZE, TILESIZE))
    textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect)


# Функија 2: Главна функција за помош
def help_timer(myBoard, msg):
    # 1 Чекор: Дефинирај ги сите помошни променливи
    counter = 5  # Бројач за секунди (иницијално 5)
    text = "Help time: " + str(counter).rjust(3) if counter > 0 else 'Time up!'
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font = pygame.font.SysFont('Consolas', 30)  # Фонт кој сакаме да се рендерира
    before_draw = myBoard  # Зачувај ја првата сотојба пред цртање за секој случај (force of habit не е нужно)

    # Главен циклус за бројач
    while True:
        drawBoard(myBoard, msg)
        # 2 Чекор: Земи кординати на празно поле
        pos_x, pos_y = getBlankPosition(myBoard)
        # 3: Бој ги сите полиња кој се достапни; Во најдобар случај можни се 4 полиња, во најлош 3
        if (isValidMove(myBoard, RIGHT) and pos_x != (len(myBoard) - 1)) \
                or pos_x == 0:  # Поле ДЕСНО од нас
            drawHelpTile(pos_x + 1, pos_y, myBoard[pos_x + 1][pos_y])

        if (isValidMove(myBoard, LEFT) and pos_x != 0) \
                or pos_x == (len(myBoard) - 1):  # Поле ЛЕВО од нас
            drawHelpTile(pos_x - 1, pos_y, myBoard[pos_x - 1][pos_y])

        if isValidMove(myBoard, UP):  # Поле НАД од нас
            drawHelpTile(pos_x, pos_y + 1, myBoard[pos_x][pos_y + 1])

        if isValidMove(myBoard, DOWN):  # Поле ДОЛУ од нас
            drawHelpTile(pos_x, pos_y - 1, myBoard[pos_x][pos_y - 1])

        # 4 Чекор: Креирај timer (да брои до кога ќе стои помоштач); 5 секунди
        for e in pygame.event.get():
            if e.type == pygame.USEREVENT:
                counter -= 1  # Намали го бројачот
                text = "Move one of the red squares. Help time: " + str(counter).rjust(3) \
                    if counter > 0 else 'Time up!'  # Ако дојде 0=Time up!
            if text == 'Time up!':  # Доколку си на 0-та секунда изгаси го циклусот врати се назад во главниот циклус
                DISPLAYSURF.blit(font.render(text, True, (255, 255, 255)),
                                 (32, 48))  # Кординати за испишување x:32, y:48
                pygame.display.flip()
                pygame.time.Clock().tick(3)  # Повикај часовнк за секоја секунда
                break
        else:
            DISPLAYSURF.blit(font.render(text, True, (255, 255, 255)), (32, 48))  # Кординати за испишување x:32, y:48
            pygame.display.flip()
            pygame.time.Clock().tick(60)  # Повикај часовнк за секоја секунда
            continue
        break
    # Цртај ја таблата секој пат со цел да стојат сите квадратчиња
    drawBoard(before_draw, msg)

########################################################################################################################

if __name__ == '__main__':
    main()
