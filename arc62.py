import arcade
import random

from pyglet.graphics import Batch
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'Game'
BOMBS_COUNT = 5
TILE_SCALING = 0.50
CAMERA_LERP = 1
class GridGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, antialiasing=True)
        arcade.set_background_color(arcade.color.SKY_BLUE)

        # Камеры: мир и GUI
        self.world_camera = arcade.camera.Camera2D()  # Камера для игрового мира
        self.gui_camera = arcade.camera.Camera2D()  # Камера для объектов интерфейса

        # Причина тряски — специальный объект ScreenShake2D
        self.camera_shake = arcade.camera.grips.ScreenShake2D(
            self.world_camera.view_data,  # Трястись будет только то, что попадает в объектив мировой камеры
            max_amplitude=15.0,  # Параметры, с которыми можно поиграть
            acceleration_duration=0.1,
            falloff_time=0.5,
            shake_frequency=10.0,
        )
        # Звук взрыва на будущее
        self.explosion_sound = arcade.load_sound(":resources:sounds/explosion1.wav")

        # Данные уровня
        self.tile_map = None

        # Слои с нашими спрайтами
        self.player_list = arcade.SpriteList()
        self.bomb_list = arcade.SpriteList()

        # Игрок
        self.player: arcade.Sprite | None = None

        # Границы мира (по карте)
        self.world_width = SCREEN_WIDTH
        self.world_height = SCREEN_HEIGHT

        # Батч для текста
        self.batch = Batch()
        self.text_info = arcade.Text(
            "WASD/стрелки — движение • Столкнись с красно‑серой «бомбой» (астероид) — камера дрожит",
            20, 20, arcade.color.BLACK, 14, batch=self.batch
        )

    def setup(self):
        # Загружаем уровень из TMX-файла
        self.tile_map = arcade.load_tilemap("assets\second_level.tmx", scaling=TILE_SCALING)
        self.wall_list = self.tile_map.sprite_lists["walls"]
        self.collision_list = self.tile_map.sprite_lists["collisions"]

        # Уточняем размеры мира по карте
        self.world_width = int(self.tile_map.width * self.tile_map.tile_width * TILE_SCALING)
        self.world_height = int(self.tile_map.height * self.tile_map.tile_height * TILE_SCALING)

        # Создаём игрока
        self.player_list = arcade.SpriteList()
        self.player = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png",
                                    scale=0.8)
        self.player_list.center_x = 400  # Примерные координаты
        self.player_list.center_y = 400  # Ставим туда, где не пересекается со стенами
        self.player_list.append(self.player)

        # Разбрасываем бомбочки
        self.bomb_list = arcade.SpriteList()
        bomb_texture = ":resources:/images/tiles/bomb.png"
        for _ in range(BOMBS_COUNT):
            scale = random.uniform(0.1, 0.5)  # Случайный масштаб для каждой бомбы
            bomb = arcade.Sprite(bomb_texture, scale=scale)
            # self._place_sprite_safely(bomb)
            self.bomb_list.append(bomb)

        # Физический движок
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, self.collision_list
        )


    def on_draw(self):
        self.clear()

        # 1) Мир
        self.camera_shake.update_camera()  # Запчасть от тряски камеры
        self.world_camera.use()
        self.wall_list.draw()
        self.player_list.draw()
        self.bomb_list.draw()
        self.camera_shake.readjust_camera()  # И это тоже
        
        # 2) GUI
        self.gui_camera.use()

        self.batch.draw()

    def on_update(self, dt: float):
        self.physics_engine.update()
        self.camera_shake.update(dt)  # Обновляем тряску камеры

        bombs_hit = arcade.check_for_collision_with_list(self.player, self.bomb_list)
        if bombs_hit:  # Наткнулись на бомбы
            for b in bombs_hit:
                b.remove_from_sprite_lists()
            self.explosion_sound.play()  # Бадабум!
            self.camera_shake.start()  # Начинаем тряску камеры. Остановится она сама через время, указанное в настройках

        position = (
            self.player.center_x,
            self.player.center_y
        )
        self.world_camera.position = arcade.math.lerp_2d(  # Изменяем позицию камеры
            self.world_camera.position,
            position,
            CAMERA_LERP,  # Плавность следования камеры
        )

        self.text_bombs = arcade.Text(
            f"Бомб осталось: {len(self.bomb_list)}",
            20, 46, arcade.color.DARK_SLATE_GRAY, 14, batch=self.batch
        )
def main():
    game = GridGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()