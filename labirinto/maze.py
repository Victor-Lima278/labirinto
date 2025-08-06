import pygame
import numpy as np
import csv
import random
import threading
from typing import Tuple

class Maze:

    WALL = 0
    HALL = 1
    PLAYER = 2
    PRIZE = 3

    def __init__(self):
        self.M = None
        pygame.init()

    def load_from_csv(self, file_path: str):
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            self.M = np.array([list(map(int, row)) for row in reader])

    def init_player(self):
        while True:
            posx = random.randint(2, 39)
            posy = random.randint(2, 39)
            if self.M[posx, posy] == Maze.HALL:
                self.init_pos_player = (posx, posy)
                break

        while True:
            posx = random.randint(2, 39)
            posy = random.randint(2, 39)
            if self.M[posx, posy] == Maze.HALL:
                self.M[posx, posy] = Maze.PRIZE
                break

    def find_prize(self, pos: Tuple[int, int]) -> bool:
        return self.M[pos[0], pos[1]] == Maze.PRIZE

    def is_free(self, pos: Tuple[int, int]) -> bool:
        rows, cols = self.M.shape
        x, y = pos
        if 0 <= x < rows and 0 <= y < cols:
            return self.M[x, y] in [Maze.HALL, Maze.PRIZE]
        return False

    def mov_player(self, pos: Tuple[int, int]) -> None:
        if self.M[pos[0], pos[1]] == Maze.HALL:
            self.M[pos[0], pos[1]] = Maze.PLAYER

    def get_init_pos_player(self) -> Tuple[int, int]:
        return self.init_pos_player

    def run(self):
        th = threading.Thread(target=self._display)
        th.daemon = True
        th.start()

    def _display(self, cell_size=15):
        rows, cols = self.M.shape
        width, height = cols * cell_size, rows * cell_size
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Labirinto")

        # Cores
        BLACK = (0, 0, 0)
        GRAY = (192, 192, 192)
        BLUE = (0, 0, 255)
        GOLD = (255, 215, 0)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

            screen.fill(BLACK)

            for y in range(rows):
                for x in range(cols):
                    val = self.M[y, x]
                    if val == Maze.WALL:
                        color = BLACK
                    elif val == Maze.HALL:
                        color = GRAY
                    elif val == Maze.PLAYER:
                        color = BLUE
                    elif val == Maze.PRIZE:
                        color = GOLD

                    pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))

            pygame.display.flip()
