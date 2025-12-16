import arcade
import random

from pyglet.graphics import Batch

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Red Hat collects berries"

GIRL_SCALE = 0.5
GIRL_SPEED = 50

BUSH_COUNT = 15
BUSH_SCALE = 0.4
BERRY_SCALE = 0.2

class Girl(arcade.Sprite):
    def __init__(self):
        super().__init__('images/images/girl.png', GIRL_SCALE)
        self.center_x = self.width // 2
        self.center_y = self.height // 2
        self.change_x = 0
        self.change_y = 0
        self.speed = GIRL_SPEED

    def update(self, delta_time):
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time
        if self.left < 0:
            self.left = 0
        if self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH
        if self.bottom < 0:
            self.bottom = 0
        if self.top > SCREEN_HEIGHT:
            self.top = SCREEN_HEIGHT


class Bush(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.texture = arcade.load_texture('images/images/bush.png')
        self.scale = BUSH_SCALE
        self.center_x = x
        self.center_y = y



class Berry(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.texture = arcade.load_texture('images/images/berry.png')
        self.scale = 0.2
        self.center_x = x
        self.center_y = y + 20


class BerryGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.background = arcade.load_texture('images/images/meadow.png')

    def setup(self):
        # Создание объектов
        self.girl = Girl()
        self.girl_list = arcade.SpriteList()
        self.girl_list.append(self.girl)
        self.bushes = arcade.SpriteList()  # Список спрайтов
        self.berries = arcade.SpriteList()  # Список спрайтов
        self.batch = Batch()
        self.score = 0
        for i in range(BUSH_COUNT):
            x = random.randint(20, SCREEN_WIDTH - 20)
            y = random.randint(20, SCREEN_HEIGHT - 20)
            b = Bush(x, y)
            be = Berry(x, y)
            self.bushes.append(b)
            self.berries.append(be)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.XYWH(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT))
        self.bushes.draw()
        self.berries.draw()
        self.girl_list.draw()

    def on_update(self, delta_time):
        self.girl.update(delta_time)
        coins_hit_list = arcade.check_for_collision_with_list(self.girl, self.berries)
        print(coins_hit_list)
        for coin in coins_hit_list:
            coin.remove_from_sprite_lists()

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP:
            self.girl.change_y = self.girl.speed
        elif key == arcade.key.DOWN:
            self.girl.change_y = -self.girl.speed
        elif key == arcade.key.LEFT:
            self.girl.change_x = -self.girl.speed
        elif key == arcade.key.RIGHT:
            self.girl.change_x = self.girl.speed
        # Управление Красной Шапочкой
        ...

    def on_key_release(self, key, modifiers):
        # Остановка при отпускании клавиш
        ...


def setup_game(width=800, height=600, title="Red Hat collects berries"):
    game = BerryGame(width, height, title)
    game.setup()
    return game


def main():
    setup_game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
