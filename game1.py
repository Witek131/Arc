import arcade
import random

# Задаём размеры окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Использование списка спрайтов и кликов мыши"


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.ASH_GREY)

        # Создаём список спрайтов для монет
        self.coin_list = arcade.SpriteList()

    def setup(self):
        """Настройка игры, создание монет"""
        for _ in range(10):  # Создаём 10 монет
            coin = arcade.Sprite("images/items/img.jpg", scale=0.5)
            coin.center_x = random.randint(0, SCREEN_WIDTH)
            coin.center_y = random.randint(0, SCREEN_HEIGHT)
            self.coin_list.append(coin)

    def on_draw(self):
        """Отрисовка всех спрайтов"""
        self.clear()
        self.coin_list.draw()  # Отрисовываем все монеты

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка клика мышью"""
        coins_hit_list = arcade.get_sprites_at_point((x, y), self.coin_list) # В какие монеты тыкнул игрок.

        # Удаляем монеты, по которым кликнули
        for coin in coins_hit_list:
            coin.remove_from_sprite_lists()

        if not self.coin_list:
            self.setup()  # Если все монеты собраны, создаём новые //злодейский смех//


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()  # Запускаем начальную настройку игры
    arcade.run()


if __name__ == "__main__":
    main()