from pygame import *
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QMainWindow, QHBoxLayout, QPushButton

#еобходимые классы

#класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, wight, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (wight, height)) #вместе 55,55 - параметры
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
        # Название окна
        self.setWindowTitle('Настройки')
        
        # Элементы интерфейса
        layout = QVBoxLayout()
        
        # Метка и поле для первого игрока
        label_player1 = QLabel("Имя первого игрока:")
        edit_player1 = QLineEdit()
        layout.addWidget(label_player1)
        layout.addWidget(edit_player1)
        
        # Метка и поле для второго игрока
        label_player2 = QLabel("Имя второго игрока:")
        edit_player2 = QLineEdit()
        layout.addWidget(label_player2)
        layout.addWidget(edit_player2)
        
        # Поле для выбора количества жизней
        label_lives = QLabel("Количество жизней:")
        edit_lives = QLineEdit()
        layout.addWidget(label_lives)
        layout.addWidget(edit_lives)
        
        # Кнопка сохранения настроек
        btn_save = QPushButton("Сохранить")
        btn_save.clicked.connect(lambda: self.save_settings(edit_player1.text(), edit_player2.text(), int(edit_lives.text())))
        layout.addWidget(btn_save)
        
        # Устанавливаем общий макет окна
        self.setLayout(layout)
    
    def save_settings(self, player1_name, player2_name, lives_count):
        g_player1_name = self.player1_name
        g_player2_name = self.player2_name
        g_lifes_count = self.lives_count
        #print(f'Игрок 1: {player1_name}, Игрок 2: {player2_name}, Жизней: {lives_count}')
        # Здесь должна быть логика передачи полученных значений обратно в игру


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings_window = None
        self.initUI()
    
    def initUI(self):
        # Настраиваем название главного окна
        self.setWindowTitle('Игра Понг')
        
        # Центральное содержимое окна
        central_widget = QWidget()
        layout = QHBoxLayout(central_widget)
        
        # Первая кнопка - Старт с базовыми настройками
        start_button = QPushButton("Старт с базовыми настройками")
        start_button.clicked.connect(self.start_game_with_defaults)
        layout.addWidget(start_button)
        
        # Вторая кнопка - Открытие окна настроек
        settings_button = QPushButton("Настройки")
        settings_button.clicked.connect(self.open_settings)
        layout.addWidget(settings_button)
        
        # Устанавливаем центральное содержимое
        self.setCentralWidget(central_widget)
    
    def open_settings(self):
        if not self.settings_window:
            self.settings_window = SettingsWindow()
        self.settings_window.show()
    
    def start_game_with_defaults(self):
        # Логика старта игры с дефолтными значениями
        game = True
        finish = False

#игровая сцена:
back = (200, 255, 255) #цвет фона (background)
win_width = 600
win_height = 500
window = display.set_mode((win_width, win_height))
window.fill(back)


#флаги, отвечающие за состояние игры
g_player1_name = 'A'
g_player2_name = 'B'
g_lifes_count = 10
lifes_1 = g_lifes_count
lifes_2 = g_lifes_count
ball_lost = False

game = True
finish = False
clock = time.Clock()
FPS = 60



#создания мяча и ракетки   
racket1 = Player('racket.png', 30, 200, 4, 50, 150) 
racket2 = Player('racket.png', 520, 200, 4, 50, 150)
ball = GameSprite('tenis_ball.png', 200, 200, 4, 50, 50)


font.init()
font = font.Font(None, 35)
lose1 = font.render(g_player1_name + ' LOSE!', True, (180, 0, 0))
lose2 = font.render(g_player2_name + ' LOSE!', True, (180, 0, 0))

speed_x = 3
speed_y = 3

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())

while game:
    for e in event.get():
        if e.type == QUIT:
           game = False
  
    if finish != True:
        window.fill(back)
        racket1.update_l()
        racket2.update_r()
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            speed_x *= -1
      
       #если мяч достигает границ экрана, меняем направление его движения
        if ball.rect.y > win_height-50 or ball.rect.y < 0:
           speed_y *= -1


       #если мяч улетел дальше ракетки, выводим условие проигрыша для первого игрока
        if ball.rect.x < 0:
            if not ball_lost:
            #Уменьшаем число жизней игрока только один раз!
                lifes_1 -= 1
                ball.rect.x = 250
                ball.rect.y = 250

                ball_lost = True
            else:
            #Мяч снова внутри игровой зоны, сбрасываем флаг
                ball_lost = False

        if lifes_1 <= 0:
            ball.rect.x = 700
            ball.rect.y = 700
            finish = True
            window.blit(lose1, (200, 200))
            game_over = True


       #если мяч улетел дальше ракетки, выводим условие проигрыша для второго игрока
        if ball.rect.x > win_width:
            if not ball_lost:
                lifes_2 -= 1
                ball.rect.x = 250
                ball.rect.y = 250
                ball_lost = True
            else:
                ball_lost = False

        if lifes_2 <= 0:
            ball.rect.x = 700
            ball.rect.y = 700
            finish = True
            window.blit(lose2, (200, 200))
            game_over = True

        lifes1_font = font.render('Жизни ' + g_player1_name + ': ' + str(lifes_1), True, (180, 0, 0))
        window.blit(lifes1_font, (200, 50))

        lifes2_font = font.render('Жизни ' + g_player2_name + ': ' + str(lifes_2), True, (180, 0, 0))
        window.blit(lifes2_font, (200, 100))

        racket1.reset()
        racket2.reset()
        ball.reset()


    display.update()
    clock.tick(FPS)
