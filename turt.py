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
        self.stone_texture = arcade.load_texture(':resources:images/tiles/stoneCenter.png')
        self.sand_texture = arcade.load_texture(':resources:images/tiles/sandCenter.png')
        self.player_texture = arcade.load_texture(':resources:images/enemies/slimeBlue.png')

    def setup(self):
        self.grid = [[0 for i in range(15)] for j in range(10)]
        for i in range(10):
            for j in range(15):
                x = j * self.cell_size + self.cell_size // 2
                y = i * self.cell_size + self.cell_size // 2
                if i == 0 or j ==0 or i == 9 or j == 14:
                    s_p = arcade.Sprite(self.stone_texture, scale=1)
                    s_p.position = (x, y)
                    self.grid[i][j] = (x,y)
                    self.wall_sprites.append(s_p)
                    self.all_sprites.append(s_p)
                else:
                    s_p = arcade.Sprite(self.sand_texture, scale=0.5)
                    s_p.position = (x, y)
                    self.grid[i][j] = [s_p]
                    self.wall_sprites.append(s_p)
                    self.all_sprites.append(s_p)
        self.player = arcade.Sprite(self.player_texture, scale=0.5)
        x = self.cell_size + self.cell_size // 2
        y = self.cell_size + self.cell_size // 2
        self.player.position = (x,y)
        self.all_sprites.append(self.player)
        self.phisik = arcade.PhysicsEngineSimple(self.player, self.wall_sprites)

    def on_draw(self):
        self.clear()
        self.all_sprites.draw()

    def on_update(self, delta_time: float):
        self.phisik.update()

    def on_key_press(self, key, modifiers):
        ...

    def on_key_release(self, key, modifiers):
        pass


def setup_game(width=960, height=640, title="Leonardo Game"):
    game = GridGame(width, height, title)
    game.setup()
    return game


def main():
    setup_game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()