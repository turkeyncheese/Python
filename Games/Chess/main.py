import pygame as p
import ChessEngine, ChessAI
import sys
from multiprocessing import Process, Queue

WIDTH = HEIGHT = 512
MOVELOGWIDTH = 128
MOVELOGHEIGHT = HEIGHT
DIMENSION = 8
SQUARESIZE = HEIGHT // DIMENSION
MAXFPS = 15
IMAGES = {}

def loadImages():
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQUARESIZE, SQUARESIZE))

def main():
    p.init()
    screen = p.display.set_mode((WIDTH + MOVELOGWIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    moveLogFont = p.font.SysFont("Arial", 14, False, False)

    gs = ChessEngine.GameState()
    legalMoves = gs.getLegalMoves()

    moveMade = False
    animate = False
    gameOver = False

    loadImages()
    running = True

    squareSelected = ()
    playerClicks = []

    aiThinking = False
    moveUndone = False
    moveFinderProcess = None

    playerOne = True
    playerTwo = False

    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)

        for e in p.event.get():
            if e.type == p.QUIT:
                moveFinderProcess.terminate()
                p.quit()
                sys.exit()

            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()
                    col = location[0] // SQUARESIZE
                    row = location[1] // SQUARESIZE

                    if squareSelected == (row, col) or col >= 8:
                        squareSelected = ()
                        playerClicks = []
                    else:
                        squareSelected = (row, col)
                        playerClicks.append(squareSelected)
                    
                    if len(playerClicks) == 2 and humanTurn:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)

                        for i in range(len(legalMoves)):
                            if move == legalMoves[i]:
                                gs.makeMove(legalMoves[i])
                                moveMade = True
                                animate = True

                                squareSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [squareSelected]
            
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False

                    if aiThinking:
                        moveFinderProcess.terminate()
                        aiThinking = False
                    
                    moveUndone = True
                
                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    legalMoves = gs.getLegalMoves()
                    squareSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False 
                    gameOver = False

                    if aiThinking:
                        moveFinderProcess.terminate()
                        aiThinking = False
                    
                    moveUndone = True
        
        if not gameOver and not humanTurn and not moveUndone:
            if not aiThinking:
                aiThinking = True
                returnQueue = Queue()
                moveFinderProcess = Process(target=ChessAI.findBestMove, args=(gs, legalMoves, returnQueue))
                moveFinderProcess.start()
            
            if not moveFinderProcess.is_alive():
                aiMove = returnQueue.get()

                if aiMove is None:
                    aiMove = ChessAI.findRandomMove(legalMoves)
                
                gs.makeMove(aiMove)
                moveMade = True
                animate = True
                aiThinking = False

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            legalMoves = gs.getLegalMoves()
            moveMade = False
            animate = False
        
        drawGameState(screen, gs, legalMoves, squareSelected)

        if not gameOver:
            drawMoveLog(screen, gs, moveLogFont)

        if gs.checkmate:
            gameOver = True

            if gs.whiteToMove:
                drawEndGameText(screen, "Black wins by checkmate.")
            else:
                drawEndGameText(screen, "White wins by checkmate.")
        
        elif gs.stalemate:
            gameOver = True
            drawEndGameText(screen, "Draw by stalemate")

        clock.tick(MAXFPS)
        p.display.flip()

def drawGameState(screen, gs, legalMoves, squareSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, legalMoves, squareSelected)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]

    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[((row + col) % 2)]
            p.draw.rect(screen, color, p.Rect(col * SQUARESIZE, row * SQUARESIZE, SQUARESIZE, SQUARESIZE))

def highlightSquares(screen, gs, legalMoves, squareSelected):
    if (len(gs.moveLog)) > 0:
        lastMove = gs.moveLog[-1]
        s = p.Surface((SQUARESIZE, SQUARESIZE))
        s.set_alpha(100)
        s.fill(p.Color("green"))
        screen.blit(s, (lastMove.endCol * SQUARESIZE, lastMove.endRow * SQUARESIZE))
    
    if squareSelected != ():
        row, col, = squareSelected

        if gs.board[row][col][0] == ("w" if gs.whiteToMove else "b"):
            s = p.Surface((SQUARESIZE, SQUARESIZE))
            s.set_alpha(100)
            s.fill(p.Color("blue"))
            screen.blit(s, (col * SQUARESIZE, row * SQUARESIZE))
            s.fill(p.Color("yellow"))

            for move in legalMoves:
                if move.startRow == row and move.startCol == col:
                    screen.blit(s, (move.endCol * SQUARESIZE, move.endRow * SQUARESIZE))

def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]

            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(col * SQUARESIZE, row * SQUARESIZE, SQUARESIZE, SQUARESIZE))

def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(WIDTH, 0, MOVELOGWIDTH, MOVELOGHEIGHT)
    p.draw.rect(screen, p.Color("black"), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []

    for i in range(0, len(moveLog), 2):
        moveString = str(i // 2 + 1) + ". " + str(moveLog[i]) + " "

        if i + 1 < len(moveLog):
            moveString += str(moveLog[i + 1]) + "  "
        
        moveTexts.append(moveString)
    
    movesPerRow = 1
    padding = 5
    lineSpacing = 2
    textY = padding

    for i in range(0, len(moveTexts), movesPerRow):
        text = ""

        for j in range(movesPerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i + j]
        
        textObject = font.render(text, True, p.Color("white"))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing

def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    textObject = font.render(text, False, p.Color("gray"))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - textObject.get_width() / 2,
                                                    HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, False, p.Color("black"))
    screen.blit(textObject, textLocation.move(2, 2))

def animateMove(move, screen, board, clock):
    global colors
    dRow = move.endRow - move.startRow
    dCol = move.endCol - move.startCol
    framesPerSquare = 3
    frameCount = (abs(dRow) + abs(dCol)) * framesPerSquare

    for frame in range(frameCount + 1):
        row, col = (move.startRow + dRow * frame / frameCount, move.startCol + dCol * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)

        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQUARESIZE, move.endRow * SQUARESIZE, SQUARESIZE, SQUARESIZE)
        p.draw.rect(screen, color, endSquare)

        if move.pieceCaptured != "--":
            if move.isEnPassantMove:
                enPassantRow = move.endRow + 1 if move.pieceCaptured[0] == "b" else move.endRow - 1
                endSquare = p.Rect(move.endCol * SQUARESIZE, enPassantRow * SQUARESIZE, SQUARESIZE, SQUARESIZE)
                p.draw.rect(screen, color, endSquare)
            
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        
        screen.blit(IMAGES[move.pieceMoved], p.Rect(col * SQUARESIZE, row * SQUARESIZE, SQUARESIZE, SQUARESIZE))
        p.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
