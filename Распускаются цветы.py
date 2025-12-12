import arcade
import random

# Константы
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
SCREEN_TITLE = "Цветущие лилии"
FLOWER_COUNT = 10
ANIMATION_SPEED = 0.2  # скорость анимации в секундах между кадрами


class Flower(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.textures = []
        for i in range(9):
            print(i)
            self.textures.append(arcade.load_texture(f"images/flowers/flower{i}.png"))
        # 1. Загрузите все 9 текстур анимации в список self.textures.
        # 2. Установите начальную текстуру (бутон).
        # 3. Задайте позицию и масштаб спрайта.
        ...
        self.textur = self.textures[0]
        self.center_x = x
        self.center_y = y
        self.scale = 0.2
        self.animation_frame = 0
        self.is_blooming = False
        self.animation_timer = 0

    def update(self, delta_time: float = 1 / 60):
        # Если is_blooming равно True, увеличивайте animation_timer.
        if self.is_blooming:
            self.animation_timer += delta_time
            # Когда таймер превысит ANIMATION_SPEED:
            if self.animation_timer >ANIMATION_SPEED:
                self.animation_timer = 0
                self.animation_frame +=1
                if self.animation_frame >= len(self.textures):
                    self.is_blooming = False
                    self.animation_frame = len(self.textures)
                else:
                    print(self.animation_frame)
                    self.texture = self.textures[self.animation_frame-1]

        # - Сбросьте таймер, увеличьте кадр анимации (animation_frame).
        # - Смените текущую текстуру спрайта на новую из списка.
        # - Если анимация дошла до конца, установите is_blooming в False.
        ...

    def start_blooming(self):  # Изменение параметра цветения
        if not self.is_blooming and self.animation_frame < len(self.textures) -1:
            self.is_blooming = True
        # Установите флаг is_blooming в True, чтобы запустить анимацию.
        ...


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.texture = arcade.load_texture('images/meadow.png')
        self.flower_list = None
        # Загрузите фоновую текстуру 'images/meadow.png'.
        ...

    def setup(self):
        self.flower_list = arcade.SpriteList()
        for i in range(FLOWER_COUNT):
            flower = Flower(
                x=random.randint(50, SCREEN_WIDTH - 50),
                y=random.randint(50, SCREEN_HEIGHT - 50)
            )
            self.flower_list.append(flower)
        # Создайте FLOWER_COUNT экземпляров класса Flower в случайных
        # позициях и добавьте их в self.flower_list.
        ...

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(self.width//2, self.height//2, self.width, self.height))
        self.flower_list.draw()
        # Отрисуйте фон и список цветов self.flower_list.
        ...

    def on_update(self, delta_time):
        self.flower_list.update(delta_time)
        # Вызовите метод .update() у всего списка спрайтов, передав delta_time.
        # Это автоматически вызовет метод update() у каждого цветка.
        ...

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            clicet_flor = arcade.get_sprites_at_point((x, y), self.flower_list)
            for i in clicet_flor:
                i.start_blooming()
        # Используйте arcade.get_sprites_at_point, чтобы найти нажатые цветки.
        # Для каждого из них вызовите метод start_blooming().
        ...


def setup_game(width=1000, height=500, title="Цветущие лилии"):
    game = MyGame(width, height, title)
    game.setup()
    return game


# Блок для вашего локального тестирования (необязателен для сдачи)
def main():
    setup_game()
    arcade.run()


if __name__ == "__main__":
    main()