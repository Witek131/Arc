import arcade

# Задаём размер окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Урок: Работа со спрайтами"


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.ASH_GREY)

        # Загружаем изображение спрайта
        self.player_sprite = arcade.Sprite(":resources:/images/miami_synth_parallax/car/car-idle.png", scale=2)
        self.player_sprite.center_x = width // 2
        self.player_sprite.center_y = height // 2
        self.all_sprites = arcade.SpriteList()
        self.all_sprites.append(self.player_sprite)

    def on_draw(self):
        self.clear()
        self.all_sprites.draw()


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()