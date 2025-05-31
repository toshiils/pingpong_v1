import sys
from pygame import *
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout

# Цвет фона и размеры окна 
back = (200, 255, 255)
win_width = 600
win_height = 500 

# Глобальные переменные
g_player1_name = 'Игрок 1'
g_player2_name = 'Игрок 2'
g_lifes_count = 10

# Класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed


class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Настройки')

        layout = QVBoxLayout()

        self.edit_player1 = QLineEdit()
        self.edit_player2 = QLineEdit()
        self.edit_lives = QLineEdit()

        layout.addWidget(QLabel("Имя первого игрока:"))
        layout.addWidget(self.edit_player1)

        layout.addWidget(QLabel("Имя второго игрока:"))
        layout.addWidget(self.edit_player2)

        layout.addWidget(QLabel("Количество жизней:"))
        layout.addWidget(self.edit_lives)

        btn_save = QPushButton("Сохранить и начать игру")
        btn_save.clicked.connect(self.save_settings)
        layout.addWidget(btn_save)

        self.setLayout(layout)

    def save_settings(self):
        global g_player1_name, g_player2_name, g_lifes_count
        g_player1_name = self.edit_player1.text() or "Игрок 1"
        g_player2_name = self.edit_player2.text() or "Игрок 2"
        try:
            g_lifes_count = int(self.edit_lives.text())
        except ValueError:
            g_lifes_count = 10  # значение по умолчанию

        self.close()
        start_game()


def start_game():
    global window
    window = display.set_mode((win_width, win_height))
    window.fill(back)

    lifes_1 = g_lifes_count
    lifes_2 = g_lifes_count
    ball_lost = False
    finish = False

    racket1 = Player('racket.png', 30, 200, 4, 50, 150)
    racket2 = Player('racket.png', 520, 200, 4, 50, 150)
    ball = GameSprite('tenis_ball.png', 200, 200, 4, 50, 50)

    font.init()
    font_obj = font.Font(None, 35)
    lose1 = font_obj.render(g_player1_name + ' проиграл(а)!', True, (180, 0, 0))
    lose2 = font_obj.render(g_player2_name + ' проиграл(а)!', True, (180, 0, 0))

    speed_x = 3
    speed_y = 3

    clock = time.Clock()
    FPS = 60
    game = True

    while game:
        for e in event.get():
            if e.type == QUIT:
                game = False

        if not finish:
            window.fill(back)
            racket1.update_l()
            racket2.update_r()
            ball.rect.x += speed_x
            ball.rect.y += speed_y

            if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
                speed_x *= -1

            if ball.rect.y > win_height - 50 or ball.rect.y < 0:
                speed_y *= -1

            if ball.rect.x < 0:
                if not ball_lost:
                    lifes_1 -= 1
                    ball.rect.x, ball.rect.y = 250, 250
                    ball_lost = True
            elif ball.rect.x > win_width:
                if not ball_lost:
                    lifes_2 -= 1
                    ball.rect.x, ball.rect.y = 250, 250
                    ball_lost = True
            else:
                ball_lost = False

            if lifes_1 <= 0:
                finish = True
                window.blit(lose1, (190, 200))
            elif lifes_2 <= 0:
                finish = True
                window.blit(lose2, (190, 200))

            lifes1_font = font_obj.render(f'Жизни {g_player1_name}: {lifes_1}', True, (180, 0, 0))
            lifes2_font = font_obj.render(f'Жизни {g_player2_name}: {lifes_2}', True, (180, 0, 0))
            window.blit(lifes1_font, (190, 20))
            window.blit(lifes2_font, (190, 60))

            racket1.reset()
            racket2.reset()
            ball.reset()

        display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = SettingsWindow()
    win.show()
    sys.exit(app.exec_())
