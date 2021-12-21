import pygame
import sys
import run_game
import random
from run_game import Board
from run_game import Field

WIDTH = 500
HEIGHT = 500
CAPTION = "Pyttleship"
GRID_SIZE = 50

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(CAPTION)


class Game:
    def __init__(self):
        self.game = run_game.Game()
        self.game.init(True)
        self.running = True
        self.players = self.game.players
        self.active_player = self.game.active_player

    def process_exit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def draw(self, board):
        for y, row in enumerate(board.field):
            for x, field in enumerate(row):
                color = "White"
                if field.is_ship_func():
                    color = "Red"
                x_param = x * GRID_SIZE
                y_param = y * GRID_SIZE
                rect = pygame.Rect(x_param, y_param, x_param + GRID_SIZE, y_param + GRID_SIZE)
                pygame.draw.rect(window, color, rect)
        pygame.display.flip()

    def loop(self):
        while self.running:
            self.draw(self.active_player.board)
            self.process_exit()


def main():
    game = Game()
    game.loop()


if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit(1)
