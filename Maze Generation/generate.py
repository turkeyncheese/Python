import random
import numpy as np

def getMaze(size):
    maze = np.ones((size, size), dtype=int)
    maze = generateMaze(size)

    entranceCandidates = exitCandidates = []

    for i in range(1, size - 1, 2):
        if maze[1, i] == 0:
            entranceCandidates.append(i)

    if entranceCandidates:
        entrance = random.choice(entranceCandidates)
        maze[0, entrance] = 0

    for i in range(1, size - 1, 2):
        if maze[size - 2, i] == 0:
            exitCandidates.append(i)

    if exitCandidates:
        exit = random.choice(exitCandidates)
        maze[size - 1, exit] = 0

    return maze, entrance, exit

def generateMaze(size):
    maze = np.ones((size, size), dtype=int)

    stack = [(1, 1)]
    maze[1, 1] = 0

    while stack:
        x, y = stack[-1]

        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
        random.shuffle(directions)

        found = False

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < size and 0 <= ny < size and maze[ny, nx] == 1:
                maze[ny - dy // 2, nx - dx // 2] = 0
                maze[ny, nx] = 0
                stack.append((nx, ny))
                found = True
                break

        if not found:
            stack.pop()

    return maze