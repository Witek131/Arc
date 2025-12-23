import arcade

SPEED = 4
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
SCREEN_TITLE = "Leonardo Game"


class GridGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.cell_size = 64
        self.all_sprites = arcade.SpriteList()
        self.wall_sprites = arcade.SpriteList()
        # Загружаем текстуры из встроенных ресурсов
        self.stone_texture = arcade.load_texture(":resources:images/tiles/stoneCenter.png")
        self.sand_texture = arcade.load_texture(":resources:images/tiles/sandCenter.png")
        self.player_texture = arcade.load_texture(":resources:images/enemies/slimeBlue.png")

    def setup(self):
        self.grid = [[0 for _ in range(15)] for _ in range(10)]
        for row in range(10):
            for col in range(15):
                if not row * col or row == 9 or col == 14:
                    self.grid[row][col] = 1
                x = col * self.cell_size + self.cell_size // 2
                y = row * self.cell_size + self.cell_size // 2

                # Рисуем основу клетки
                if self.grid[row][col] == 0:
                    sand_sprite = arcade.Sprite(self.sand_texture, scale=0.5)
                    sand_sprite.position = (x, y)
                    self.grid[row][col] = [sand_sprite]
                    self.all_sprites.append(sand_sprite)
                else:
                    stone_sprite = arcade.Sprite(self.stone_texture, scale=0.5)
                    self.grid[row][col] = [stone_sprite]
                    stone_sprite.position = (x, y)
                    self.wall_sprites.append(stone_sprite)
                    self.all_sprites.append(stone_sprite)

        self.player = arcade.Sprite(self.player_texture, scale=0.5)
        x = 7 * self.cell_size + self.cell_size // 2
        y = 5 * self.cell_size + self.cell_size // 2
        self.player.position = (x, y)
        self.all_sprites.append(self.player)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, self.wall_sprites
        )

    def on_draw(self):
        self.clear()
        self.all_sprites.draw()

    def on_update(self, delta_time: float):
        self.physics_engine.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.player.change_y = SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = SPEED

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.UP, arcade.key.DOWN]:
            self.player.change_y = 0
        if key in [arcade.key.LEFT, arcade.key.RIGHT]:
            self.player.change_x = 0


def setup_game(width=960, height=640, title="Leonardo Game"):
    game = GridGame(width, height, title)
    game.setup()
    return game


def main():
    setup_game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
