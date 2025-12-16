import arcade
import random

# Параметры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Клетчатое поле"


class GridGame(arcade.Window):
    def __init__(self, screen_width, screen_height, screen_title, cell_size):
        super().__init__(screen_width, screen_height, screen_title)

        self.cell_size = cell_size
        self.rows = screen_height // cell_size
        self.cols = screen_width // cell_size

        # Создаём пустую сетку нужного размера
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def setup(self):
        # Заполняем сетку случайными значениями
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j] = random.randint(0, 2)

    def on_draw(self):
        # Рисуем сетку
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.cell_size + self.cell_size // 2
                y = row * self.cell_size + self.cell_size // 2

                # Цвет в зависимости от значения в сетке
                if self.grid[row][col] == 1:
                    color = arcade.color.BLUE
                elif self.grid[row][col] == 2:
                    color = arcade.color.RED
                else:
                    color = arcade.color.LIGHT_GRAY
                arcade.draw_rect_filled(arcade.rect.XYWH(x, y,
                                                         self.cell_size - 2,
                                                         self.cell_size - 2),
                                        color)
                # Для красоты рисуем границы, чтобы всё не сливалось
                arcade.draw_rect_outline(arcade.rect.XYWH(x, y,
                                                          self.cell_size - 2,
                                                          self.cell_size - 2),
                                         arcade.color.BLACK, 1)

    def on_mouse_press(self, x, y, button, modifiers):
        # Преобразуем экранные координаты в индексы сетки
        col = int(x // self.cell_size)
        row = int(y // self.cell_size)

        # Проверяем границы
        if 0 <= row < self.rows and 0 <= col < self.cols:
            # Левый клик — «увеличиваем» цвет на единицу циклически
            if button == arcade.MOUSE_BUTTON_LEFT:
                self.grid[row][col] = (self.grid[row][col] + 1) % 3

            # Правый клик — «уменьшаем» по этим же правилам
            elif button == arcade.MOUSE_BUTTON_RIGHT:
                self.grid[row][col] = (self.grid[row][col] - 1) % 3

def main():
    game = GridGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, 40)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()