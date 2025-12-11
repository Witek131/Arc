import arcade

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
TITLE = "Texture"


class MyGame(arcade.Window):
    def __init__(self, width, height, title, filename):
        super().__init__(width, height, title)
        self.w = width
        self.h = height
        self.texture = arcade.load_texture(f"images/backgrounds/{filename}")  # Мы все картинки храним в images, помните?

    def setup(self):
        

        # Отрисовываем изображение во весь экран

        # Загрузите текстуру из файла, используя полный путь
        # Сохраните загруженную текстуру в атрибут класса.
        ...

    def on_draw(self):
        self.clear()

        # Отрисовываем изображение во весь экран
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(self.w // 2, self.h // 2, self.w, self.h))
        ...


def setup_game(width=800, height=600, title="Texture", filename='fon2.png'):
    game = MyGame(width, height, title, filename)
    game.setup()
    return game


# Блок для вашего локального тестирования (необязателен для сдачи)
def main():
    setup_game()
    arcade.run()


if __name__ == "__main__":
    main()