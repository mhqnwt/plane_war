import random
import sys
from enum import Enum

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
        self.once_over = False

    def init_game(self):
        self.hero = Hero(self)
        self.enemy_list = []
        self.once_over = False

    def hero_collided(self):
        for e in self.enemy_list:
            if e.status != Status.OK:
                continue
            result = e.hero_collided(self.hero)
            print(result)
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
            if e.status == Status.OK:
                e.move()
            e.draw()

    def start(self):
        while True:
            if self.once_over:
                self.init_game()
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
            self.enemy_list = list(filter(lambda e: e.status != Status.Disappear, self.enemy_list))

            # 画英雄和子弹 - draw hero and bullets
            self.draw_hero()
            self.hero.move_draw_bullets()

            self.bullet_collided()
            crashed = self.hero_collided()
            if crashed:
                print("游戏结束")
                self.once_over = True
                self.hero.status = Status.Blow
                while self.hero.status == Status.Blow:
                    self.hero.draw()
                    pygame.display.update()
                print("游戏结束2")

            pygame.display.update()


class Status(Enum):
    OK = 1
    Blow = -1
    Disappear = 0


def get_blow_image_path(base, num, suffix):
    arr = []
    for i in range(num):
        arr.append("{0}{1}.{2}".format(base, i + 1, suffix))
    return arr


class GameItem:
    def __init__(self, game_obj: Game, pos: Position, img_path, blow_img_paths, speed=10, fall=True):
        self.game, self.pos, self.img_path, self.speed, self.fall = game_obj, pos, img_path, speed, fall
        self.image = pygame.image.load(img_path).convert_alpha()
        self.status = Status.OK
        self.blow_index = 0
        self.blow_images = []
        for path in blow_img_paths:
            self.blow_images.append(pygame.image.load(path).convert_alpha())

    def draw(self):
        if self.status == Status.OK:
            self.game.screen.blit(self.image, (self.pos.x, self.pos.y))
        elif self.status == Status.Blow:
            self.game.screen.blit(self.blow_images[self.blow_index], (self.pos.x, self.pos.y))
            self.blow_index += 1
            if self.blow_index > len(self.blow_images) - 1:
                self.status = Status.Disappear

    def move(self):
        tmp = 1
        if not self.fall:
            tmp = -1
        self.pos.y += tmp * self.speed
        w, h = pygame.display.get_surface().get_size()
        if self.fall and self.pos.y > h:
            self.status = Status.Disappear
        if not self.fall and self.pos.y < 0:
            self.status = Status.Disappear

    def get_collide_rect(self) -> Rect:
        return Rect(self.pos.x, self.pos.y, self.image.get_width(), self.image.get_height())


class Enemy(GameItem):
    def __init__(self, game_obj: Game, speed=8):
        w, h = pygame.display.get_surface().get_size()
        pos = Position(random.randint(10, w - 10), -1 * random.randint(10, h - 10))
        super(Enemy, self).__init__(game_obj, pos, "src/enemy1.png", get_blow_image_path("src/enemy1_down", 4, "png"), speed)

    def hero_collided(self, hero):
        tmp = Rect.collide(hero.get_collide_rect(), self.get_collide_rect())
        return tmp


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
        self.status = Status.OK
        self.bullet_list = []
        self.blow_images = []
        tmp = get_blow_image_path("src/me_destroy_", 4, "png")
        self.blow_index = 0
        for path in tmp:
            self.blow_images.append(pygame.image.load(path).convert_alpha())

    def draw(self):
        if self.status == Status.OK:
            self.game.screen.blit(self.hero, (self.pos.x, self.pos.y))
        elif self.status == Status.Blow:
            self.game.screen.blit(self.blow_images[self.blow_index], (self.pos.x, self.pos.y))
            self.blow_index += 1
            if self.blow_index > len(self.blow_images) - 1:
                self.status = Status.Disappear

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
        self.bullet_list = list(filter(lambda e: e.status == Status.OK, self.bullet_list))

    def enemy_collided(self, enemy_list):
        for bul in self.bullet_list:
            for enemy in enemy_list:
                tmp = Rect.collide(bul.get_collide_rect(), enemy.get_collide_rect())
                if tmp:
                    bul.status = Status.Disappear
                    enemy.status = Status.Blow
                    # TODO: enemy destroy with animation
                    print("a enemy crashed")
                    return True
        return False

    def get_collide_rect(self) -> Rect:
        return Rect(self.pos.x, self.pos.y, self.hero.get_width(), self.hero.get_height())


class Bullet(GameItem):
    def __init__(self, game_obj: Game, hero: Hero, speed=20):
        pos = Position(hero.pos.x + int(hero.hero.get_width() / 2), hero.pos.y)
        super().__init__(game_obj, pos, "src/bullet.png", [], speed, False)


game = Game(400, 600)
game.start()
