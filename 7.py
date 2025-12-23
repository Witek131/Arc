import arcade
from arcade.camera import Camera2D
from pyglet.graphics import Batch

SCREEN_W = 1280
SCREEN_H = 720
TITLE = "Прыгскокология"

# Физика и движение
GRAVITY = 7            # Пикс/с^2
MOVE_SPEED = 6          # Пикс/с
JUMP_SPEED = 40          # Начальный импульс прыжка, пикс/с
LADDER_SPEED = 3        # Скорость по лестнице

# Качество жизни прыжка
COYOTE_TIME = 0.08        # Сколько после схода с платформы можно ещё прыгнуть
JUMP_BUFFER = 0.12        # Если нажали прыжок чуть раньше приземления, мы его «запомним» (тоже лайфхак для улучшения качества жизни игрока)
MAX_JUMPS = 1             # С двойным прыжком всё лучше, но не сегодня

# Камера
CAMERA_LERP = 0.12        # Плавность следования камеры
WORLD_COLOR = arcade.color.SKY_BLUE
class Platformer(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_W, SCREEN_H, TITLE, antialiasing=True)
        arcade.set_background_color(WORLD_COLOR)

        # Камеры
        self.world_camera = Camera2D()
        self.gui_camera = Camera2D()

        # Списки спрайтов
        self.player_list = arcade.SpriteList()
        self.walls = arcade.SpriteList(use_spatial_hash=True)  # Очень много статичных — хэш спасёт вас
        self.platforms = arcade.SpriteList()  # Двигающиеся платформы
        self.ladders = arcade.SpriteList()
        self.coins = arcade.SpriteList()
        self.hazards = arcade.SpriteList()  # Шипы/лава

        # Игрок
        self.player = None
        self.spawn_point = (128, 256)  # Куда респавнить после шипов

        # Физика
        self.engine = None

        # Ввод
        self.left = self.right = self.up = self.down = self.jump_pressed = False
        self.jump_buffer_timer = 0.0
        self.time_since_ground = 999.0
        self.jumps_left = MAX_JUMPS

        # Счёт
        self.score = 0
        self.batch = Batch()
        self.text_info = arcade.Text("WASD/стрелки — ходьба/лестницы • SPACE — прыжок",
                                     16, 16, arcade.color.GRAY, 14, batch=self.batch)

    def setup(self):
        # --- Игрок ---
        self.player_list.clear()
        self.player = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png",
                                    scale=0.8)
        self.player.center_x, self.player.center_y = self.spawn_point
        print(self.player.center_x, self.player.center_y)
        self.player_list.append(self.player)

        # --- Мир: сделаем крошечную арену руками ---
        # Пол из «травы»
        for x in range(0, 1600, 64):
            tile = arcade.Sprite(":resources:images/tiles/grassMid.png", scale=0.5)
            tile.center_x = x
            tile.center_y = 64
            self.walls.append(tile)

        # Пара столбиков-стен
        for y in range(64, 64 + 64 * 6, 64):
            s = arcade.Sprite(":resources:images/tiles/stoneCenter.png", 0.5)
            s.center_x = 800
            s.center_y = y
            self.walls.append(s)

        # Лестница
        for y in range(64, 64 + 64 * 4, 64):
            l = arcade.Sprite(":resources:images/tiles/ladderMid.png", 0.5)
            l.center_x = 600
            l.center_y = y
            self.ladders.append(l)

        # Двигающаяся платформа (влево-вправо)
        plat = arcade.Sprite(":resources:images/tiles/grassHalf_left.png", 0.5)
        plat.center_x = 400
        plat.center_y = 265
        # Говорим движку, куда платформе можно кататься
        plat.boundary_left = 300
        plat.boundary_right = 700
        plat.change_x = 5  # Поедем вправо
        self.platforms.append(plat)

        # Монетки
        for x in (350, 450, 550, 650, 900, 950):
            c = arcade.Sprite(":resources:images/items/coinGold.png", 0.5)
            c.center_x = x
            c.center_y = 340 if x < 700 else 140
            self.coins.append(c)

        # Шипы (притворимся лавой)
        for x in range(1600, 2000, 64):
            h = arcade.Sprite(":resources:images/tiles/lavaTop_high.png", 0.5)
            h.center_x = x
            h.center_y = 64
            self.hazards.append(h)

        # --- Физический движок платформера ---
        # Статичные — в walls, подвижные — в platforms, лестницы — ladders.
        self.engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player,
            gravity_constant=GRAVITY,
            walls=self.walls,
            platforms=self.platforms,
            ladders=self.ladders
        )

        # Сбросим вспомогательные таймеры
        self.jump_buffer_timer = 0
        self.time_since_ground = 999.0
        self.jumps_left = MAX_JUMPS

    def on_draw(self):
        self.clear()

        # --- Мир ---
        self.world_camera.use()
        self.walls.draw()
        self.platforms.draw()
        self.ladders.draw()
        self.hazards.draw()
        self.coins.draw()
        self.player_list.draw()

        # --- GUI ---
        self.gui_camera.use()
        self.batch.draw()

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left = True
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right = True
        elif key in (arcade.key.UP, arcade.key.W):
            self.up = True
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down = True
        elif key == arcade.key.SPACE:
            self.jump_pressed = True
            self.jump_buffer_timer = JUMP_BUFFER

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left = False
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right = False
        elif key in (arcade.key.UP, arcade.key.W):
            self.up = False
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down = False
        elif key == arcade.key.SPACE:
            self.jump_pressed = False
            # Вариативная высота прыжка: отпустили рано — подрежем скорость вверх
            if self.player.change_y > 0:
                self.player.change_y *= 0.45

    def on_update(self, dt: float):
        # Обработка горизонтального движения
        move = 0
        if self.left and not self.right:
            move = -MOVE_SPEED
        elif self.right and not self.left:
            move = MOVE_SPEED
        self.player.change_x = move

        # Лестницы имеют приоритет над гравитацией: висим/лезем
        on_ladder = self.engine.is_on_ladder()  # На лестнице?
        if on_ladder:
            # По лестнице вверх/вниз
            if self.up and not self.down:
                self.player.change_y = LADDER_SPEED
            elif self.down and not self.up:
                self.player.change_y = -LADDER_SPEED
            else:
                self.player.change_y = 0

        # Если не на лестнице — работает обычная гравитация движка
        # Прыжок: can_jump() + койот + буфер
        grounded = self.engine.can_jump(y_distance=6)  # Есть пол под ногами?
        if grounded:
            self.time_since_ground = 0
            self.jumps_left = MAX_JUMPS
        else:
            self.time_since_ground += dt

        # Учтём «запомненный» пробел
        if self.jump_buffer_timer > 0:
            self.jump_buffer_timer -= dt

        want_jump = self.jump_pressed or (self.jump_buffer_timer > 0)

        # Можно прыгать, если стоим на земле или в пределах койот-времени
        if want_jump:
            can_coyote = (self.time_since_ground <= COYOTE_TIME)
            if grounded or can_coyote:
                # Просим движок прыгнуть: он корректно задаст начальную вертикальную скорость
                self.engine.jump(JUMP_SPEED)
                self.jump_buffer_timer = 0

        # Обновляем физику — движок сам двинет игрока и платформы
        self.engine.update()

        # Собираем монетки и проверяем опасности
        for coin in arcade.check_for_collision_with_list(self.player, self.coins):
            coin.remove_from_sprite_lists()
            self.score += 1

        if arcade.check_for_collision_with_list(self.player, self.hazards):
            # «Ау» -> респавн
            self.player.center_x, self.player.center_y = self.spawn_point
            self.player.change_x = self.player.change_y = 0
            self.time_since_ground = 999
            self.jumps_left = MAX_JUMPS

        # Камера — плавно к игроку и в рамках мира
        target = (self.player.center_x, self.player.center_y)
        cx, cy = self.world_camera.position
        smooth = (cx + (target[0] - cx) * CAMERA_LERP,
                  cy + (target[1] - cy) * CAMERA_LERP)

        half_w = self.world_camera.viewport_width / 2
        half_h = self.world_camera.viewport_height / 2
        # Ограничим, чтобы за края уровня не выглядывало небо
        world_w = 2000  # Мы руками построили пол до x = 2000
        world_h = 900
        cam_x = max(half_w, min(world_w - half_w, smooth[0]))
        cam_y = max(half_h, min(world_h - half_h, smooth[1]))

        self.world_camera.position = (cam_x, cam_y)
        self.gui_camera.position = (SCREEN_W / 2, SCREEN_H / 2)

        # Обновим счёт
        self.text_score = arcade.Text(f"Счёт: {self.score}",
                                      16, SCREEN_H - 36, arcade.color.DARK_SLATE_GRAY,
                                      20, batch=self.batch)
def main():
    game = Platformer()
    arcade.run()

if __name__ == "__main__":
    main()