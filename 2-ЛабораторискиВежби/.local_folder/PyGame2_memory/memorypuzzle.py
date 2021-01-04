"""

 Created on 06-Nov-20
 @author: Kiril Zelenkovski

Memory puzzle:

МКД:
Во оваа игра одреден број икони (форми) се покриени
со бели коцки. Има по две од секоја форма.
Играч треба да клика 2 полиња бели со цел да добие
совпаѓање на две. Со клик се гледа што има позади
таа бела коцка. Ако две форми се совпаѓаат од откриените
коцки тогаш тие остануваат, не се сокриваат. Играчот
ја комплетирал таблата (завршил со играта) доколку сите
коцки бели се ослободени, односно нема веќе сокриени форми.
На почетоци од игра брзински се откриени некои форми како
вид помош за играчот.

ENG:
In the Memory Puzzle game, several icons
are covered up by white boxes. There are
two of each icon. The player can click on
two boxes to see what icon is behind
them. If the icons match, then those boxes
remain uncovered. The player wins when
all the boxes on the board are uncovered.
To give the player a hint, the boxes are
quickly uncovered once at the beginning of
the game.

"""
from pygame.locals import *
import pygame
import random
import sys

# frames per second, the general speed of the program
FPS = 30
# size of window's width in pixels
WINDOW_WIDTH = 640
# size of windows' height in pixels
WINDOW_HEIGHT = 480
# speed boxes' sliding reveals and covers
REVEAL_SPEED = 8
# size of box height & width in pixels
BOX_SIZE = 40
# size of gap between boxes in pixels
GAP_SIZE = 10
# number of columns of icons
BOARD_WIDTH = 10
# number of rows of icons
BOARD_HEIGHT = 7

'''
assert 1: 
This assert statement with an expression basically says, ―The
programmer asserts that this expression must be True,
otherwise crash the program
'''
assert (BOARD_WIDTH * BOARD_HEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
# Divide with 2: to get one margin instead of two
X_MARGIN = int((WINDOW_WIDTH - (BOARD_WIDTH * (BOX_SIZE + GAP_SIZE))) / 2)
Y_MARGIN = int((WINDOW_HEIGHT - (BOARD_HEIGHT * (BOX_SIZE + GAP_SIZE))) / 2)

# RGB colors
GRAY = (100, 100, 100)
NAVY_BLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

BG_COLOR = NAVY_BLUE
LIGHT_BG_COLOR = GRAY
BOX_COLOR = WHITE
HIGHLIGHT_COLOR = BLUE

# all shapes
DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

# tuple of colors
ALL_COLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
# tuple of shapes
ALL_SHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)

'''
assert 2:
This assertion statement makes sure that there
are enough color/shape combinations for
the size of the board we have.  
'''
assert len(ALL_COLORS) * len(ALL_SHAPES) * 2 >= BOARD_WIDTH * BOARD_HEIGHT, \
    "Board is too big for the number of shapes/colors defined."


def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # used to store x coordinate of mouse event
    mousex = 0
    # used to store y coordinate of mouse event
    mousey = 0
    # display caption
    pygame.display.set_caption('Memory Puzzle game')

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    # stores the (x, y) of the first box clicked.
    firstSelection = None

    DISPLAYSURF.fill(BG_COLOR)
    startGameAnimation(mainBoard)

    while True:  # main game loop
        mouseClicked = False

        DISPLAYSURF.fill(BG_COLOR)  # drawing the window
        drawBoard(mainBoard, revealedBoxes)

        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx is not None and boxy is not None:
            # The mouse is currently over a box.
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx, boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                revealedBoxes[boxx][boxy] = True  # set the box as "revealed"
                if firstSelection is None:  # the current box was the first box clicked
                    firstSelection = (boxx, boxy)
                else:  # the current box was the second box clicked
                    # Check if there is a match between the two icons.
                    icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                    icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)

                    if icon1shape != icon2shape or icon1color != icon2color:
                        # Icons don't match. Re-cover up both selections.
                        pygame.time.wait(1000)  # 1000 milliseconds = 1 sec
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False
                    elif hasWon(revealedBoxes):  # check if all pairs found
                        gameWonAnimation(mainBoard)
                        pygame.time.wait(2000)

                        # Reset the board
                        mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxesData(False)

                        # Show the fully unrevealed board for a second.
                        drawBoard(mainBoard, revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        # Replay the start game animation.
                        startGameAnimation(mainBoard)
                    firstSelection = None  # reset firstSelection variable

        # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARD_WIDTH):
        revealedBoxes.append([val] * BOARD_HEIGHT)
    return revealedBoxes


def getRandomizedBoard():
    # Get a list of every possible shape in every possible color.
    icons = []
    for color in ALL_COLORS:
        for shape in ALL_SHAPES:
            icons.append((shape, color))

    random.shuffle(icons)  # randomize the order of the icons list
    numIconsUsed = int(BOARD_WIDTH * BOARD_HEIGHT / 2)  # calculate how many icons are needed
    icons = icons[:numIconsUsed] * 2  # make two of each
    random.shuffle(icons)

    # Create the board data structure, with randomly placed icons.
    board = []
    for x in range(BOARD_WIDTH):
        column = []
        for y in range(BOARD_HEIGHT):
            column.append(icons[0])
            del icons[0]  # remove the icons as we assign them
        board.append(column)
    return board


def splitIntoGroupsOf(groupSize, theList):
    # splits a list into a list of lists, where the inner lists have at
    # most groupSize number of items.
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result


def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOX_SIZE + GAP_SIZE) + X_MARGIN
    top = boxy * (BOX_SIZE + GAP_SIZE) + Y_MARGIN
    return (left, top)


def getBoxAtPixel(x, y):
    for boxx in range(BOARD_WIDTH):
        for boxy in range(BOARD_HEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOX_SIZE, BOX_SIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


def drawIcon(shape, color, boxx, boxy):
    quarter = int(BOX_SIZE * 0.25)  # syntactic sugar
    half = int(BOX_SIZE * 0.5)  # syntactic sugar

    left, top = leftTopCoordsOfBox(boxx, boxy)  # get pixel coords from board coords
    # Draw the shapes
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BG_COLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOX_SIZE - half, BOX_SIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, (
            (left + half, top), (left + BOX_SIZE - 1, top + half), (left + half, top + BOX_SIZE - 1),
            (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOX_SIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOX_SIZE - 1), (left + BOX_SIZE - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOX_SIZE, half))


def getShapeAndColor(board, boxx, boxy):
    # shape value for x, y spot is stored in board[x][y][0]
    # color value for x, y spot is stored in board[x][y][1]
    return board[boxx][boxy][0], board[boxx][boxy][1]


def drawBoxCovers(board, boxes, coverage):
    # Draws boxes being covered/revealed. "boxes" is a list
    # of two-item lists, which have the x & y spot of the box.
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BG_COLOR, (left, top, BOX_SIZE, BOX_SIZE))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0:  # only draw the cover if there is an coverage
            pygame.draw.rect(DISPLAYSURF, BOX_COLOR, (left, top, coverage, BOX_SIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def revealBoxesAnimation(board, boxesToReveal):
    # Do the "box reveal" animation.
    for coverage in range(BOX_SIZE, (-REVEAL_SPEED) - 1, -REVEAL_SPEED):
        drawBoxCovers(board, boxesToReveal, coverage)


def coverBoxesAnimation(board, boxesToCover):
    # Do the "box cover" animation.
    for coverage in range(0, BOX_SIZE + REVEAL_SPEED, REVEAL_SPEED):
        drawBoxCovers(board, boxesToCover, coverage)


def drawBoard(board, revealed):
    # Draws all of the boxes in their covered or revealed state.
    for boxx in range(BOARD_WIDTH):
        for boxy in range(BOARD_HEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                # Draw a covered box.
                pygame.draw.rect(DISPLAYSURF, BOX_COLOR, (left, top, BOX_SIZE, BOX_SIZE))
            else:
                # Draw the (revealed) icon.
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)


def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHT_COLOR, (left - 5, top - 5, BOX_SIZE + 10, BOX_SIZE + 10), 4)


def startGameAnimation(board):
    # Randomly reveal the boxes 8 at a time.
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            boxes.append((x, y))
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8, boxes)

    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)


def gameWonAnimation(board):
    # flash the background color when the player has won
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = LIGHT_BG_COLOR
    color2 = BG_COLOR

    for i in range(13):
        color1, color2 = color2, color1  # swap colors
        DISPLAYSURF.fill(color1)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)


def hasWon(revealedBoxes):
    # Returns True if all the boxes have been revealed, otherwise False
    for i in revealedBoxes:
        if False in i:
            return False  # return False if any boxes are covered.
    return True


if __name__ == '__main__':
    main()
