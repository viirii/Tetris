# Christine Baek
# TETRIS
# Created for Fall 2015 15-112
# Features include pause, restart, hard drop and increasing difficulty

################################################################################

import random
from tkinter import *

def init(data):
    # set board dimensions and margin
    data.gameStart = 0
    data.rows = 15
    data.cols = 10
    data.margin = 20
    # make board
    data.emptyColor = "blue"
    data.board = [([data.emptyColor] * data.cols) for row in range(data.rows)]
    #Seven "standard" pieces (tetrominoes)
    iPiece = [
        [ True,  True,  True,  True]
    ]
    jPiece = [
        [ True, False, False ],
        [ True, True,  True]
    ]
    lPiece = [
        [ False, False, True],
        [ True,  True,  True]
    ]
    oPiece = [
        [ True, True],
        [ True, True]
    ]
    sPiece = [
        [ False, True, True],
        [ True,  True, False ]
    ]
    tPiece = [
        [ False, True, False ],
        [ True,  True, True]
    ]

    zPiece = [
        [ True,  True, False ],
        [ False, True, True]
    ]
    tetrisPieces = [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]
    data.tetrisPieces = tetrisPieces
    tetrisPieceColors = [ "red", "yellow", "magenta", "pink", 
                            "cyan", "green", "orange" ]
    data.tetrisPieceColors = tetrisPieceColors
    # falling piece data
    data.fallingPiece = [[[]]]
    data.fallingPieceColor = "red"
    data.fallingPieceX = 4
    data.fallingPieceY = 0
    # iitial speed
    data.timerDelay = 500
    data.isGameOver = False
    # keep track of score
    data.score = 0
    # keep track of whether game is paused or not
    data.isPaused = False
    data.level = 1

################################################################################
# game functions
################################################################################

# getCellBounds from grid-demo.py
def getCellBounds(row, col, data):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = data.width - 2*data.margin
    gridHeight = data.height - 2*data.margin
    x0 = data.margin + gridWidth * col / data.cols
    x1 = data.margin + gridWidth * (col+1) / data.cols
    y0 = data.margin + gridHeight * row / data.rows
    y1 = data.margin + gridHeight * (row+1) / data.rows
    return (x0, y0, x1, y1)

# randomly choose and position new game piece
def newFallingPiece(data) :
    # randomly choose new piece
    index = random.randint(0,6)
    data.fallingPiece = data.tetrisPieces[index]
    data.fallingPieceColor = data.tetrisPieceColors[index]
    # center the piece depending on the size of the piece
    data.fallingPieceX = ((data.cols//2) - (len(data.fallingPiece[0])//2))
    data.fallingPieceY = 0

# move the falling Piece if allowed
def moveFallingPiece(data, drow, dcol) :
    data.fallingPieceX += dcol
    data.fallingPieceY += drow
    if fallingPieceIsLegal(data) :
        return True
    # if move is ilegal, revert back to original coordinates
    else :
        data.fallingPieceX -= dcol
        data.fallingPieceY -= drow
    return False

# test to see if the desired move of piece is allowed
def fallingPieceIsLegal(data) :    
    # left bounds
    if data.fallingPieceX < 0 : return False
    # right bounds
    elif data.fallingPieceX + len(data.fallingPiece[0]) > data.cols  : 
        return False
    # lower bounds
    elif data.fallingPieceY + len(data.fallingPiece) > data.rows : 
        return False
    # upper bounds
    elif data.fallingPieceY < 0 : return False
    # if any of the piece overlaps with a block already in board, return False
    for row in range(len(data.fallingPiece)) :
        for col in range(len(data.fallingPiece[0])) :
            if data.fallingPiece[row][col] :
                y, x = row+data.fallingPieceY, col+data.fallingPieceX
                if data.board[y][x] != data.emptyColor: return False
    # move is allowed if it passes all the tests above
    else : return True

def rotateFallingPiece(data) :
    rows, cols = len(data.fallingPiece[0]), len(data.fallingPiece)
    # temporarily store the shape of the piece before rotation
    tempPiece = data.fallingPiece
    # temporarily store the original top-left corner of the piece
    tempX, tempY = data.fallingPieceX, data.fallingPieceY
    # initialize the newly rotated piece
    data.fallingPiece = [([False] * cols) for row in range(rows)]    
    # rotate piece
    for col in range(len(tempPiece[0])-1, -1, -1) :
        for row in range(len(tempPiece)) :  # loop through the row backwards
            column = len(tempPiece[0])-1-col
            data.fallingPiece[column][row] = (tempPiece[row][col])
    # center the piece based on its center of weight
    oldCenterX = data.fallingPieceX + len(tempPiece[0])//2
    oldCenterY = data.fallingPieceY + len(tempPiece)//2
    newCenterX = data.fallingPieceX + len(data.fallingPiece[0])//2
    newCenterY = data.fallingPieceY + len(data.fallingPiece)//2
    # if balance is off, move the piece accordingly
    if oldCenterX != newCenterX : data.fallingPieceX += oldCenterX - newCenterX
    if oldCenterY != newCenterY : data.fallingPieceY += oldCenterY - newCenterY
    if fallingPieceIsLegal(data) : return
    # if move is illega, re-instate the original rotation and coordinate
    else : 
        data.fallingPiece = tempPiece
        data.fallingPieceX, data.fallingPieceY = tempX, tempY

# once piece has reached the blocks, insert into the board
def placeFallingPiece(data) :
    for row in range(len(data.fallingPiece)) :
            for col in range(len(data.fallingPiece[0])) :
                if data.fallingPiece[row][col] :                    
                    y, x = data.fallingPieceY+row, data.fallingPieceX+col
                    data.board[y][x] = data.fallingPieceColor

# test to see if the game is over
def isGameOver(data) :
    if data.board[0][4]!=data.emptyColor or data.board[0][5]!=data.emptyColor :
        return True
    return False    

# remove rows full of blocks
def removeFullRow(data) :
    newRow = data.rows
    # if any block in a row is empty, keep the row in the board
    for oldRow in range(len(data.board)-1, -1, -1) :
        if data.emptyColor in data.board[oldRow] :
            newRow -= 1
            for cells in range(len(data.board[0])) :
                data.board[newRow][cells] = data.board[oldRow][cells]
        else : pass
    # Update score
    data.score += (newRow**2)
    # fill in deleted/empty rows with emptyColor
    for row in range(newRow) :
        for col in range(len(data.board[0])) :
            data.board[row][col] = data.emptyColor

# position piece in a hard-drop
def getFinalPosition(data) :
    while True :
        drow = 1
        if not moveFallingPiece(data, drow, 0) : break
        # test each increasing row until the move is illegal
        else : 
            continue
            drow += 1
    placeFallingPiece(data)

################################################################################
# controllers
################################################################################

def mousePressed(event, data):
    pass

def keyPressed(event, data):
    # following keys available only during active play
    if not data.isPaused : 
        if (event.keysym == "Left") :
            moveFallingPiece(data, 0, -1)    
        elif (event.keysym == "Right") :
            moveFallingPiece(data, 0, +1) 
        elif (event.keysym == "Down") :
            moveFallingPiece(data, +1, 0)
        elif (event.keysym == "Up") :
            rotateFallingPiece(data)
        # hard-drop the piece
        elif (event.keysym == "space") :
            getFinalPosition(data)
    # pause/unpause
    if (event.keysym == "p") :
        data.isPaused = not data.isPaused
    # restart the game
    elif (event.keysym == "r") :
        init(data)
    ############################################################################
    # below are options that are turned off by default
    # to turn on, remove the # before elif
    ############################################################################
    # faster piece drop / harder level
    #elif (event.keysym == "f") : data.timerDelay -= 50
    # slower piece drop / easier level
    #elif (event.keysym == "s") : data.timerDelay += 50
    # changes the falling piece
    #elif (event.keysym == "a") :
    #    newFallingPiece(data)
    
def timerFired(data):
    #moveFallingPiece(data, +1, 0)
    # place the falling piece in background board
    data.timerDelay = 500 - (data.level-1)*50
    data.level = data.score//10 + 1
    if data.gameStart == 0 :
        newFallingPiece(data)
        data.gameStart = 1
    if not data.isPaused : 
        if not moveFallingPiece(data,+1,0):
            placeFallingPiece(data)
            if not isGameOver(data) :
                removeFullRow(data)
                newFallingPiece(data)
            else :
                data.isGameOver = True

################################################################################
# Draw Functions
################################################################################

def drawGame(canvas, data):
    # call draw functions depending on whether game is active or not
    if data.isGameOver : drawGameOver(canvas, data)
    else :
        canvas.create_rectangle(0, 0, data.width, data.height, fill="orange")
        drawBoard(canvas, data)
        drawFallingPiece(canvas, data)
        drawScore(canvas, data)
        drawLevel(canvas, data)

def drawBoard(canvas, data):
    # draw grid of cells
    for row in range(data.rows):
        for col in range(data.cols):
            drawCell(canvas, data, row, col)

def drawCell(canvas, data, row, col):
    (x0, y0, x1, y1) = getCellBounds(row, col, data)
    m = 1 # cell outline margin
    canvas.create_rectangle(x0, y0, x1, y1, fill="black")
    canvas.create_rectangle(x0+m, y0+m, x1-m, y1-m, fill=data.board[row][col])

def drawFallingPiece(canvas, data) :
    #newFallingPiece(data)
    for row in range(len(data.fallingPiece)) :
        for col in range(len(data.fallingPiece[0])) :
            if data.fallingPiece[row][col] : 
                drawPiece(canvas, data, row, col)

def drawPiece(canvas, data, row, col) :
    (x0, y0, x1, y1) = getCellBounds(row+data.fallingPieceY, 
        col+data.fallingPieceX, data)
    m = 1
    canvas.create_rectangle(x0, y0, x1, y1, fill="black")
    canvas.create_rectangle(x0+m, y0+m, x1-m, y1-m, fill=data.fallingPieceColor) 

# score indicator
def drawScore(canvas, data) :
    canvas.create_text(data.width-10, data.height-5, 
                        text="SCORE : " + str(data.score), anchor=SE, 
                       fill="red", font="Helvetica 10 bold")

# level indicator
def drawLevel(canvas, data) :
    canvas.create_text(10, data.height-5, 
                        text="LEVEL : " + str(data.level), anchor=SW, 
                       fill="purple", font="Helvetica 10 bold")

# game over screen
def drawGameOver(canvas, data) :
    canvas.create_rectangle(0, 0, data.width, data.height, fill="black")
    canvas.create_text(data.width//2, data.height//2, text="GAME OVER", 
        anchor=S, fill="red", font="Helvetica 26 bold")
    canvas.create_text(data.width//2, data.height//2+30, 
        text = "Press r to Restart", anchor=N, fill = "yellow", 
        font="Helvetica 16")

def redrawAll(canvas, data):
    drawGame(canvas, data)

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 1000 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

# run(300, 300)

####################################
# playTetris() [calls run()]
####################################

def playTetris():
    rows = 15
    cols = 10
    margin = 20 # margin around grid
    cellSize = 20 # width and height of each cell
    width = 2*margin + cols*cellSize
    height = 2*margin + rows*cellSize
    run(width, height)

playTetris()