import arcade

# Константы
SCREEN_WIDTH = 820
SCREEN_HEIGHT = 620
SCREEN_TITLE = "Balls"
CELL_SIZE = 40
INDENT = 10  # Отступ от края окна

# Цвета шариков (по кругу)
COLORS = [
    arcade.color.RED,
    arcade.color.GREEN,
    arcade.color.BLUE,
    arcade.color.YELLOW,
    arcade.color.VIOLET
]


class GridGame(arcade.Window):
    def __init__(self, screen_width, screen_height, screen_title):
        super().__init__(screen_width, screen_height, screen_title)

        self.rows = (screen_height - 2 * INDENT) // CELL_SIZE
        self.cols = (screen_width - 2 * INDENT) // CELL_SIZE

        self.radius = CELL_SIZE - 2

    def setup(self):
        # Создаём пустую сетку нужного размера
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def on_draw(self):
        self.clear()
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * CELL_SIZE + INDENT
                y = row * CELL_SIZE + INDENT
                arcade.draw_lbwh_rectangle_outline(x, y, CELL_SIZE, CELL_SIZE, arcade.color.GRAY, 1)

        for row in range(self.rows):
            for col in range(self.cols):
                x = row * CELL_SIZE + INDENT + CELL_SIZE // 2
                y = col * CELL_SIZE + INDENT + CELL_SIZE // 2
                if self.grid[row][col] != 0:
                    arcade.draw_ellipse_filled(x, y, self.radius, self.radius, COLORS[self.grid[row][col]-1])

    def on_mouse_press(self, x, y, button, modifiers):
        row = (int(x) - INDENT)// CELL_SIZE
        col = (int(y) -INDENT)// CELL_SIZE
        print(self.grid[row][col])
        self.grid[row][col] %= len(COLORS)
        self.grid[row][col] += 1

        """Обработка клика мыши"""
        ...


def setup_game(width=820, height=620, title="Balls"):
    game = GridGame(width, height, title)
    game.setup()
    return game


def main():
    setup_game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
