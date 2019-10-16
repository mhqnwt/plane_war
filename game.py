import sys

import pygame

pygame.init()


class Position:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):
        return "({x}, {y})".format(x=self.x, y=self.y)


class Game:
    def __init__(self, window_w, window_h):
        self.screen = pygame.display.set_mode(size=(window_w, window_h))
        self.bg = pygame.image.load("src/background.png")
        self.hero = Hero(self)

    def draw_bg(self):
        self.screen.blit(self.bg, (0, 0))

    def draw_hero(self):
        self.hero.draw()

    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            key = pygame.key.get_pressed()
            self.draw_bg()
            self.draw_hero()
            self.hero.move(key)

            pygame.display.update()


class Hero:
    def __init__(self, game_obj: Game, speed=20):
        """
        一个飞机对象
        :param game_obj:
        :param speed:
        """
        self.game = game_obj
        w, h = pygame.display.get_surface().get_size()
        self.hero = pygame.image.load("src/plan1.png")
        self.pos = Position((w - self.hero.get_width()) / 2, h - self.hero.get_height())
        self.speed = speed

    def draw(self):
        self.game.screen.blit(self.hero, (self.pos.x, self.pos.y))

    def move(self, key):
        x, y = 0, 0
        if key[pygame.K_w]:
            y -= 1
        if key[pygame.K_s]:
            y += 1
        if key[pygame.K_a]:
            x -= 1
        if key[pygame.K_d]:
            x += 1
        self.pos.y = self.pos.y + y * self.speed
        self.pos.x = self.pos.x + x * self.speed


game = Game(400, 600)
game.start()
