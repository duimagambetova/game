import pygame
import random
import numpy as np
import time

BG_COLORS = {
    0: (250, 250, 250),
    2: (238, 228, 218),
    4: (238, 225, 201),
    8: (243, 178, 122),
    16: (246, 150, 100),
    32: (247, 124, 95),
    64: (247, 95, 59),
    128: (237, 208, 115),
    256: (237, 204, 98),
    512: (237, 201, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}


class Game2048:
    def __init__(self, difficulty=1):
        self.N = 4
        self.cellSize = 100
        self.gap = 5
        self.windowBgColor = (187, 173, 160)
        self.blockSize = self.cellSize + self.gap * 2
        self.difficulty = difficulty

        self.windowWidth = self.blockSize * 4
        self.windowHeight = self.windowWidth
        self.score = 0  # Initialize the score
        self.moves = []  # List to store the moves
        pygame.init()

        # create window
        self.window = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        self.myFont = pygame.font.SysFont("Comic Sans MS", 30)
        pygame.display.set_caption("2048")

        # init board status
        self.boardStatus = np.zeros((self.N, self.N))
        self.addNewNumber()  # add new number to board

        self.difficulty = difficulty  # Set the difficulty level
        self.best_time = float("inf")  # Initialize the best time with infinity

    def addNewNumber(self):
        freePos = list(zip(*np.where(self.boardStatus == 0)))

        if len(freePos) > 0:
            pos = random.choice(freePos)
            if self.difficulty == 1:
                self.boardStatus[pos] = 2  # Generate 2 for difficulty level 1
            elif self.difficulty == 2:
                self.boardStatus[pos] = random.choice([2, 4])  # Generate 2 or 4 for difficulty level 2
            elif self.difficulty == 3:
                self.boardStatus[pos] = random.choice([2, 2, 4])  # Generate 2, 2, or 4 for difficulty level 3
    def drawBoard(self):
        self.window.fill(self.windowBgColor)

        for r in range(self.N):
            rectY = self.blockSize * r + self.gap
            for c in range(self.N):
                rectX = self.blockSize * c + self.gap
                cellValue = int(self.boardStatus[r][c])

                pygame.draw.rect(
                    self.window,
                    BG_COLORS[cellValue],
                    pygame.Rect(rectX, rectY, self.cellSize, self.cellSize)
                )

                if cellValue != 0:
                    textSurface = self.myFont.render(f"{cellValue}", True, (0, 0, 0))
                    textRect = textSurface.get_rect(center=(rectX + self.blockSize / 2, rectY + self.blockSize / 2))
                    self.window.blit(textSurface, textRect)

    def compressNumber(self, data):
        result = [0]
        data = [x for x in data if x != 0]
        for element in data:
            if element == result[len(result) - 1]:
                result[len(result) - 1] *= 2
                result.append(0)
            else:
                result.append(element)

        result = [x for x in result if x != 0]
        return result

    def move(self, dir):
        for idx in range(self.N):
            if dir in "UD":
                data = self.boardStatus[:, idx]
            else:
                data = self.boardStatus[idx, :]

            flip = False
            if dir in "RD":
                flip = True
                data = data[::-1]

            data = self.compressNumber(data)
            data = data + (self.N - len(data)) * [0]

            if flip:
                data = data[::-1]

            if dir in "UD":
                self.boardStatus[:, idx] = data
            else:
                self.boardStatus[idx, :] = data

            self.moves.append(self.boardStatus.copy())  # Save the current board status

    def isGameOver(self):
        boardStatusBackup = self.boardStatus.copy()
        for dir in "UDLR":
            self.move(dir)

            if (self.boardStatus == boardStatusBackup).all() == False:
                self.boardStatus = boardStatusBackup
                return False
        return True

    def play(self):
        running = True
        while running:
            self.drawBoard()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            if running and not self.isGameOver():
                start_time = time.time()  # Measure the start time of the move

                # Perform bot's move
                # In this example, we will make a random move with a slight delay
                randomMove = random.choice(["U", "D", "L", "R"])
                self.move(randomMove)
                self.addNewNumber()
                time.sleep(0.2)  # Delay between moves

                if self.isGameOver():
                    print("Game Over !!")
                    print("Final Score:", self.score)
                    return

                end_time = time.time()  # Measure the end time of the move
                move_time = end_time - start_time

                if move_time < self.best_time:
                    self.best_time = move_time

                print("Move Time:", move_time)
                print("Best Time:", self.best_time)


if __name__ == "__main__":
    game = Game2048(difficulty=2)
    game.play()

