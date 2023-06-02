import pygame as p
import sys
from random import sample

WIDTH = HEIGHT = 576
DIMENSION = 9
DIFFICULTY = 50 # percent of squares empty
SQUARESIZE = HEIGHT // DIMENSION

def main():
    global grid

    p.init()
    p.display.set_caption("Sudoku")

    screen = p.display.set_mode((WIDTH, HEIGHT))
    screen.fill(p.Color("white"))

    grid = genBoard()

    squareSelected = ()
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

            elif e.type == p.KEYDOWN and squareSelected != ():
                if e.key == p.K_0 or e.key == p.K_KP0:
                    grid[squareSelected[0]][squareSelected[1]] = 0
                elif e.key == p.K_1 or e.key == p.K_KP1:
                    grid[squareSelected[0]][squareSelected[1]] = 1
                elif e.key == p.K_2 or e.key == p.K_KP2:
                    grid[squareSelected[0]][squareSelected[1]] = 2
                elif e.key == p.K_3 or e.key == p.K_KP3:
                    grid[squareSelected[0]][squareSelected[1]] = 3
                elif e.key == p.K_4 or e.key == p.K_KP4:
                    grid[squareSelected[0]][squareSelected[1]] = 4
                elif e.key == p.K_5 or e.key == p.K_KP5:
                    grid[squareSelected[0]][squareSelected[1]] = 5
                elif e.key == p.K_6 or e.key == p.K_KP6:
                    grid[squareSelected[0]][squareSelected[1]] = 6
                elif e.key == p.K_7 or e.key == p.K_KP7:
                    grid[squareSelected[0]][squareSelected[1]] = 7
                elif e.key == p.K_8 or e.key == p.K_KP8:
                    grid[squareSelected[0]][squareSelected[1]] = 8
                elif e.key == p.K_9 or e.key == p.K_KP9:
                    grid[squareSelected[0]][squareSelected[1]] = 9
            
            elif e.type == p.KEYDOWN:
                if e.key == p.K_r:
                    grid = genBoard()

                    drawGameState(screen, squareSelected)
                    p.display.flip()

            if isBoardSolved(grid):
                print("You win.")
                running = False

        drawGameState(screen, squareSelected)
        p.display.flip()

    drawGameState(screen, squareSelected)
    p.display.flip()

def drawGameState(screen, squareSelected):
    drawGrid(screen)
    highlightSquare(screen, squareSelected)
    drawNumbers(screen)

def drawGrid(screen):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            rect = p.Rect(col * SQUARESIZE, row * SQUARESIZE, SQUARESIZE, SQUARESIZE)
            p.draw.rect(screen, p.Color("white"), rect)
            p.draw.rect(screen, p.Color("gray"), rect, 1)

            if col % 3 == 0 and col != 0:
                p.draw.line(screen, p.Color("black"), (col * SQUARESIZE, 0), (col * SQUARESIZE, HEIGHT), 2)
            
            if row % 3 == 0 and row != 0:
                p.draw.line(screen, p.Color("black"), (0, row * SQUARESIZE), (WIDTH, row * SQUARESIZE), 2)

def highlightSquare(screen, squareSelected):
    if squareSelected != ():
        row, col = squareSelected

        s = p.Surface((SQUARESIZE, SQUARESIZE))
        s.set_alpha(100)
        s.fill(p.Color("yellow"))
        screen.blit(s, (col * SQUARESIZE, row * SQUARESIZE))

def drawNumbers(screen):
    font = p.font.Font(None, 40)

    for row in range(DIMENSION):
        for col in range(DIMENSION):
            number = font.render(str(grid[row][col]), True, p.Color("black"))
            x = col * SQUARESIZE + SQUARESIZE // 2 - number.get_width() // 2
            y = row * SQUARESIZE + SQUARESIZE // 2 - number.get_height() // 2

            if grid[row][col] != 0:
                screen.blit(number, (x, y))

def isBoardSolved(board):
    dim = len(board)

    for row in range(dim):
        values = set(board[row])

        if len(values) != dim or 0 in values:
            return False

    for col in range(dim):
        values = set(board[row][col] for row in range(dim))

        if len(values) != dim or 0 in values:
            return False

    for startRow in range(0, dim, 3):
        for startCol in range(0, dim, 3):
            values = set()

            for row in range(startRow, startRow + 3):
                for col in range(startCol, startCol + 3):
                    values.add(board[row][col])

            if len(values) != dim or 0 in values:
                return False

    return True

def genBoard():
    base = 3
    side = base * base

    def pattern(row, col): 
        return (base * (row % base) + row // base + col) % side

    def shuffle(s): 
        return sample(s,len(s))

    rBase = range(base) 
    rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase) ] 
    cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase) ]
    nums = shuffle(range(1, base * base + 1))

    board = [[nums[pattern(r, c)] for c in cols] for r in rows]
    
    for line in board:
        print(line)

    squares = side * side
    empties = int((DIFFICULTY / 100) * squares)

    for p in sample(range(squares), empties):
        board[p // side][p % side] = 0

    return board

if __name__ == "__main__":
    main()
