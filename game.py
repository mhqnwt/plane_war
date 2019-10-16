import sys

import pygame

pygame.init()


class Position:
    def __init__(self, x, y):
        self.x, self.y = x, y


class Game:
    def __init__(self, window_h, window_w):
        self.screen = pygame.display.set_mode(size=(window_h, window_w))
        self.bg = pygame.image.load("src/background.png")
        self.hero = Hero()

    def draw_bg(self):
        self.screen.blit(self.bg, (0, 0))

    def draw_hero(self):
        self.screen.blit(self.hero, self.get_hero_pos())

    def get_hero_pos(self):
        return (0, 0)

    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.draw_bg()
            self.draw_hero()

            pygame.display.update()


class Hero:
    def __init__(self, game_obj: Game, pos: Position, speed=20):
        """
        一个飞机对象
        :param game_obj:
        :param pos:
        :param speed:
        """

        self.game = game_obj
        self.pos = pos.x
        self.speed = speed
        self.hero = pygame.image.load("src/plan1.png")

    def draw_hero(self):
        self.game.screen.blit(self.hero, self.pos)

    def hero_move(self, up=0, down=0, left=0, right=0):
        self.pos.y = self.pos.y - up + down
        self.pos.x = self.pos.x - left + right


game = Game(400, 600)
game.start()
