import arcade
import random

from pyglet.graphics import Batch


class GridGame(arcade.Window):
    def __init__(self):
        super().__init__(700, 700, "Пример клеточного поля со спрайтами")
        self.cell_size = 60
        self.all_sprites = arcade.SpriteList()
        # Загружаем текстуры из встроенных ресурсов
        self.grass_texture = arcade.load_texture(":resources:images/tiles/grassCenter.png")
        self.water_texture = arcade.load_texture(":resources:images/tiles/water.png")
        self.coin_texture = arcade.load_texture(":resources:images/items/coinGold.png")
        # Создаём батч для текста
        self.batch = Batch()
        self.text = arcade.Text("Я здесь!",
                                self.cell_size // 2,
                                self.cell_size // 2 - 30,
                                arcade.color.RED, 12,
                                anchor_x="center", batch=self.batch)

    def setup(self):
        """Настраиваем игру здесь. Вызывается при старте и при рестарте"""
        # Инициализируем списки спрайтов
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()  # Сюда попадёт слой Collision!

        # ===== ВОЛШЕБСТВО ЗАГРУЗКИ КАРТЫ! (Почти без магии.) =====
        # Грузим тайловую карту
        map_name = "first_level.tmx"
        # Параметр 'scaling' ОЧЕНЬ важен! Умножает размер каждого тайла
        tile_map = arcade.load_tilemap('assets\one.tmx', scaling=0.50)

        # --- Достаём слои из карты как спрайт-листы ---
        # Слой "walls" (стены) — просто для отрисовки
        self.wall_list = tile_map.sprite_lists["walls"]
        # Слой "chests" (сундуки) — красота!
        self.chests_list = tile_map.sprite_lists["chests"]
        # Слой "exit" (выходы с уровня) — красота!
        self.exit_list = tile_map.sprite_lists["exit"]
        # САМЫЙ ГЛАВНЫЙ СЛОЙ: "Collision" — наши стены и платформы для физики!
        self.collision_list = tile_map.sprite_lists["collision"]
        # --- Создаём игрока ---
        # Карту загрузили, теперь создаём героя, который будет по ней бегать
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png",
                                           0.5)
        # Ставим игрока куда-нибудь на землю (посмотрите в Tiled, где у вас земля!)
        self.player_sprite.center_x = 128  # Примерные координаты
        self.player_sprite.center_y = 256  # Примерные координаты
        self.player_list.append(self.player_sprite)

        # --- Физический движок ---
        # Используем PhysicsEngineSimple, который знаем и любим
        # Он даст нам движение и коллизии со стенами (self.wall_list)!
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.collision_list
        )

    def on_draw(self):
        """Отрисовка экрана."""
        self.clear()

        # Рисуем слои карты в правильном порядке
        self.wall_list.draw()
        self.chests_list.draw()
        self.exit_list.draw()
        self.player_list.draw()

        # self.collision_list.draw()  # Обычно НЕ рисуем слой коллизий в финальной игре, но для отладки бывает полезно


def main():
    game = GridGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
