import pygame as p
import sys

WIDTH = HEIGHT = 384
DIMENSION = 3
SQUARESIZE = WIDTH // DIMENSION

grid = [["" for i in range(DIMENSION)] for j in range(DIMENSION)]

def main():
    p.init()

    p.display.set_caption("Tic Tac Toe")
    screen = p.display.set_mode((WIDTH, HEIGHT))
    screen.fill(p.Color("white"))

    squareSelected = ()
    turn = "X"

    running = True

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()

            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // SQUARESIZE
                row = location[1] // SQUARESIZE

                if squareSelected == (row, col) or col >= DIMENSION:
                    squareSelected = ()
                else:
                    squareSelected = (row, col)
                
                highlightSquare(screen, squareSelected)
            
            elif e.type == p.KEYDOWN:
                if squareSelected != ():
                    if e.key == p.K_x:
                        if isValidMove(grid, turn, "X", squareSelected):
                            grid[squareSelected[0]][squareSelected[1]] = "X"
                            turn = "O"

                    elif e.key == p.K_o:
                        if isValidMove(grid, turn, "O", squareSelected):
                            grid[squareSelected[0]][squareSelected[1]] = "O"
                            turn = "X"
        
        if gameOver(grid):
            print("Game over: " + ("X" if turn == "O" else "O") + " wins")
            break

        drawGameState(screen, squareSelected)
        p.display.flip()
    
    drawGameState(screen, squareSelected)
    p.display.flip()

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()


def drawGameState(screen, squareSelected):
    drawGrid(screen)
    highlightSquare(screen, squareSelected)
    drawPieces(screen)

def drawGrid(screen):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            rect = p.Rect(col * SQUARESIZE, row * SQUARESIZE, SQUARESIZE, SQUARESIZE)
            p.draw.rect(screen, p.Color("white"), rect)
            p.draw.rect(screen, p.Color("black"), rect, 2)

def highlightSquare(screen, squareSelected):
    if squareSelected != ():
        row, col = squareSelected

        s = p.Surface((SQUARESIZE, SQUARESIZE))
        s.set_alpha(100)
        s.fill(p.Color("yellow"))
        screen.blit(s, (col * SQUARESIZE, row * SQUARESIZE))

def drawPieces(screen):
    font = p.font.Font(None, 64)

    for row in range(DIMENSION):
        for col in range(DIMENSION):
            char = font.render(grid[row][col], True, p.Color("black"))
            x = col * SQUARESIZE + SQUARESIZE // 2 - char.get_width() // 2
            y = row * SQUARESIZE + SQUARESIZE // 2 - char.get_height() // 2

            if grid[row][col] != "":
                screen.blit(char, (x, y))

def isValidMove(grid, turn, char, squareSelected):
    if grid[squareSelected[0]][squareSelected[1]] == "":
        if turn == char:
            return True
    
    return False

def gameOver(grid):
    for row in range(0, DIMENSION):
        if (grid[row][0] == grid[row][1] and grid[row][1] == grid[row][2]) and grid[row][0] != "":
            return True
    
    for col in range(0, DIMENSION):
        if (grid[0][col] == grid[1][col] and grid[1][col] == grid[2][col]) and grid[0][col] != "":
            return True
    
    if (grid[0][0] == grid[1][1] and grid[1][1] == grid[2][2]) and grid[0][0] != "":
        return True
    
    if (grid[2][0] == grid[1][1] and grid[1][1] == grid[0][2]) and grid[0][0] != "":
        return True
    
    return False

if __name__ == "__main__":
    main()
