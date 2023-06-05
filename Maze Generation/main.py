import pygame as p
import sys
import numpy as np
from collections import deque
import generate

WIDTH = HEIGHT = 768
DIMENSION = 81 # only odd number dimensions
SQUARESIZE = WIDTH // DIMENSION

maze, entrance, exit = generate.getMaze(DIMENSION)
entrance = (0, entrance)
exit = (DIMENSION, exit)

visitedPositions = []

def main():
    p.init()
    p.display.set_caption("Maze Generation")

    screen = p.display.set_mode((SQUARESIZE * DIMENSION, SQUARESIZE * DIMENSION))
    screen.fill(p.Color("white"))

    drawMaze(screen)
    p.display.flip()

    running = True
    solvedPath = []

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()
        
        if not solvedPath:
            solvedPath = solveMaze(maze, entrance, exit, screen)
            solvedPath = [entrance] + solvedPath

        drawMaze(screen)
        drawPath(screen, solvedPath)
        p.display.flip()

def drawMaze(screen):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            cell = maze[row][col]
            rect = p.Rect((col) * SQUARESIZE, (row) * SQUARESIZE, SQUARESIZE, SQUARESIZE)

            if cell == 0:
                p.draw.rect(screen, p.Color("white"), rect)
            elif cell == 1:
                p.draw.rect(screen, p.Color("black"), rect)

def drawPath(screen, path):
    for position in path:
        row, col = position
        rect = p.Rect((col) * SQUARESIZE, (row) * SQUARESIZE, SQUARESIZE, SQUARESIZE)
        p.draw.rect(screen, p.Color("red"), rect)

def solveMaze(maze, entrance, exit, screen):
    queue = deque([(entrance, [])])
    visited = set()
    solvedPath = []

    while queue:
        current, path = queue.popleft()

        if current[0] + 1 == exit[0] and current[1] == exit[1]:
            solvedPath = path + [current]
            return solvedPath

        visited.add(current)
        
        # Draw all visited positions
        # Turning this segment off improves speed
        visitedPositions = list(visited)
        drawVisitedPositions(screen, visitedPositions)
        p.display.flip()

        row, col = current
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            nextRow = row + dr
            nextCol = col + dc
            nextPos = (nextRow, nextCol)

            if (
                0 <= nextRow < maze.shape[0]
                and 0 <= nextCol < maze.shape[1]
                and maze[nextRow, nextCol] == 0
                and nextPos not in visited
            ):
                queue.append((nextPos, path + [nextPos]))
                visited.add(nextPos)

    return solvedPath

def drawVisitedPositions(screen, visitedPositions):
    for position in visitedPositions:
        row, col = position
        rect = p.Rect(col * SQUARESIZE, row * SQUARESIZE, SQUARESIZE, SQUARESIZE)
        p.draw.rect(screen, (128, 128, 128), rect)

if __name__ == "__main__":
    main()
