import arcade

# Параметры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Пример столкновения спрайтов"


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.ASH_GREY)

        # Создаём спрайт игрока
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png", scale=0.5)
        self.player_sprite.center_x = SCREEN_WIDTH // 2
        self.player_sprite.center_y = SCREEN_HEIGHT // 2
        self.player_sprites = arcade.SpriteList()
        self.player_sprites.append(self.player_sprite)

        # Создаём список спрайтов для монет
        self.coin_list = arcade.SpriteList()

    def setup(self):
        """Создание и размещение монет"""
        for _ in range(10):  # Создаём 10 монет
            coin = arcade.Sprite(":resources:images/items/coinGold.png", scale=0.5)
            # В Arcade есть своя разновидность рандома
            coin.center_x = arcade.math.rand_in_circle((SCREEN_WIDTH//2, SCREEN_HEIGHT//2), SCREEN_WIDTH//2)[0]
            coin.center_y = arcade.math.rand_in_circle((SCREEN_WIDTH//2, SCREEN_HEIGHT//2), SCREEN_HEIGHT//2)[1]
            self.coin_list.append(coin)

    def on_draw(self):
        """Отрисовка всех спрайтов"""
        self.clear()
        self.coin_list.draw()  # Отрисовываем монеты
        self.player_sprites.draw()  # Отрисовываем игрока

    def on_update(self, delta_time):
        """Обновляем состояние игры"""
        self.player_sprite.update()

        # Проверяем столкновение игрока с монетами
        coins_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        # Удаляем монеты, с которыми произошло столкновение
        for coin in coins_hit_list:
            coin.remove_from_sprite_lists()

    def on_key_press(self, key, modifiers):
        """Обработка нажатий клавиш для управления игроком"""
        if key == arcade.key.UP:
            self.player_sprite.change_y = 5
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -5
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -5
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = 5

    def on_key_release(self, key, modifiers):
        """Остановка движения при отпускании клавиш"""
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


def main():
    game = MyGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()