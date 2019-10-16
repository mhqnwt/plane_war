import random
import sys

import pygame

pygame.init()


class Position:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):
        return "({x}, {y})".format(x=self.x, y=self.y)


class Rect:
    def __init__(self, x, y, w, h):
        self.left, self.top, self.right, self.bottom = x, y + h, x + w, y

    @staticmethod
    def collide(r1, r2):
        return not (((r1.right < r2.left) or (r1.bottom > r2.top)) or (
                (r2.right < r1.left) or (r2.bottom > r1.top)))


class Game:
    def __init__(self, window_w, window_h, max_enemy_num=10):
        self.screen = pygame.display.set_mode(size=(window_w, window_h))
        self.bg = pygame.image.load("src/background.png")
        self.hero = Hero(self)
        self.enemy_list = []
        self.max_enemy_num = max_enemy_num

    def hero_collided(self):
        for e in self.enemy_list:
            result = e.hero_collided(self.hero)
            if result:
                return True
        return False

    def bullet_collided(self):
        self.hero.enemy_collided(self.enemy_list)

    def draw_bg(self):
        self.screen.blit(self.bg, (0, 0))

    def draw_hero(self):
        self.hero.draw()

    def move_draw_enemies(self):
        for e in self.enemy_list:
            e.move()
            e.draw()

    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    return
            key = pygame.key.get_pressed()
            # 英雄响应键盘事件 - keyboard event for hero
            # w, s, a, d = up, down, left, right
            self.hero.move(key)
            if key[pygame.K_j]:
                self.hero.shoot()

            # 画背景 - draw background
            self.draw_bg()
            # 画敌人 - gen and draw enemy
            e_more = self.max_enemy_num - len(self.enemy_list)
            if e_more > 0:
                for i in range(e_more):
                    e = Enemy(self)
                    self.enemy_list.append(e)

            self.move_draw_enemies()
            self.enemy_list = list(filter(lambda e: e.status, self.enemy_list))

            # 画英雄和子弹 - draw hero and bullets
            self.draw_hero()
            self.hero.move_draw_bullets()

            self.bullet_collided()

            pygame.display.update()


class Enemy:
    def __init__(self, game_obj: Game, speed=8):
        self.game = game_obj
        self.speed = speed
        w, h = pygame.display.get_surface().get_size()
        self.pos = Position(random.randint(10, w - 10), -1 * random.randint(10, h - 10))
        self.enemy = pygame.image.load("src/enemy1.png")
        self.status = True

    def draw(self):
        self.game.screen.blit(self.enemy, (self.pos.x, self.pos.y))

    def move(self):
        self.pos.y += self.speed
        w, h = pygame.display.get_surface().get_size()
        if self.pos.y > h:
            self.status = False

    def get_rect(self) -> Rect:
        return Rect(self.pos.x, self.pos.y, self.enemy.get_width(), self.enemy.get_height())

    def hero_collided(self, hero):
        tmp = Rect.collide(hero.get_rect(), self.get_rect())
        if not tmp:
            return True
        else:
            return False


class Hero:
    def __init__(self, game_obj: Game, speed=10):
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
        self.bullet_list = []

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

    def shoot(self):
        bullet = Bullet(game, self)
        self.bullet_list.append(bullet)

    def move_draw_bullets(self):
        for bul in self.bullet_list:
            bul.move()
            bul.draw()
        self.bullet_list = list(filter(lambda e: e.status, self.bullet_list))

    def enemy_collided(self, enemy_list):
        for bul in self.bullet_list:
            for enemy in enemy_list:
                tmp = Rect.collide(bul.get_rect(), enemy.get_rect())
                if tmp:
                    bul.status = False
                    enemy.status = False
                    # TODO: enemy destroy with animation
                    print("a enemy crashed")
                    return True
        return False

    def get_rect(self) -> Rect:
        return Rect(self.pos.x, self.pos.y, self.hero.get_width(), self.hero.get_height())


class Bullet:
    def __init__(self, game_obj: Game, hero: Hero, speed=20):
        self.pos = Position(hero.pos.x + int(hero.hero.get_width() / 2), hero.pos.y)
        self.bullet = pygame.image.load("src/bullet.png")
        self.speed = speed
        self.game = game_obj
        self.status = True

    def draw(self):
        self.game.screen.blit(self.bullet, (self.pos.x, self.pos.y))

    def move(self):
        self.pos.y -= self.speed
        if self.pos.y < 0:
            self.status = False

    def get_rect(self) -> Rect:
        return Rect(self.pos.x, self.pos.y, self.bullet.get_width(), self.bullet.get_height())


game = Game(400, 600)
game.start()
