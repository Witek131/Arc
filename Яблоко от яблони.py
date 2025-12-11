import arcade
import random

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800
TITLE = "Apple Tree"


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.texture = arcade.load_texture('images/tree.png')  # Мы все картинки храним в images, помните?
        # Загрузите фоновую текстуру 'images/tree.png'
        self.apple_list = arcade.SpriteList()
        self.apple_hit_list = arcade.SpriteList()

    def setup(self):
        """Настройка игры"""
        for i in range(10):
            apple = arcade.Sprite('images/apple.png', scale=1)
            apple.center_x  =random.randint(100, self.width - 100)
            apple.center_y = random.randint(100, self.height - 100)
            apple.speed  = 50
            self.apple_list.append(apple)


        # В цикле создайте 10 спрайтов яблок ('images/apple.png').
        # Для каждого задайте случайные координаты в пределах кроны дерева
        # и добавьте его в self.apple_list.
        ...

    def on_draw(self):
        self.clear()
        # Сначала нарисуйте фоновую текстуру.
        # Затем отрисуйте оба списка спрайтов с помощью метода .draw().
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(self.width // 2, self.height // 2, self.width, self.height))
        self.apple_list.draw()
        self.apple_hit_list.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        clikk = arcade.get_sprites_at_point((x, y), self.apple_list)
        for coin in clikk:
            if coin not in self.apple_hit_list:
                self.apple_hit_list.append(coin)
                self.apple_list.remove(coin)
        """Обработка клика мышью"""
        # Используйте arcade.get_sprites_at_point для определения,
        # по какому яблоку из self.apple_list был сделан клик.
        # Переместите "кликнутые" яблоки из self.apple_list в self.apple_hit_list.
        ...

    def on_update(self, delta_time: float):
        for i in self.apple_hit_list:
            i.center_y -= i.speed * delta_time
            if i.center_y < 25:
                i.center_y = 25

        """Обновление состояния игры"""
        # В цикле пройдитесь по списку падающих яблок (self.apple_hit_list).
        # Для каждого яблока уменьшите его center_y, используя скорость и delta_time.
        # Проверьте, не достигло ли яблоко низа окна, и остановите его.
        ...


def setup_game(width=1000, height=800, title="Apple Tree"):
    game = MyGame(width, height, title)
    game.setup()
    return game


# Блок для вашего локального тестирования (необязателен для сдачи)
def main():
    setup_game()
    arcade.run()


if __name__ == "__main__":
    main()