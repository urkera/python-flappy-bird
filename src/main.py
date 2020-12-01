from PyQt4.QtCore import *
from PyQt4.QtGui import *

from form import Ui_MainWindow
from obstacle import Obstacle
from bird import Bird

from random import randint
import res_rc


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, w=None, h=None):
        super(Window, self).__init__()
        self.setupUi(self)

        self.w, self.h = w, h

        self.setFixedSize(self.w + 23, self.h + 23)

        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.graphicsView.zoom_avaliable = True

        self.obstacles = []
        self.timer = QTimer(self)
        self.bird = None
        self.animation = None
        self.game_started = False

        self.show_info_screen()

    def show_info_screen(self):
        bg = QGraphicsRectItem(QRectF(0, 0, self.w, self.h))
        grad = QLinearGradient(0, 0, 0, self.h)
        grad.setColorAt(0.00, QColor(78, 192, 202))
        grad.setColorAt(0.85, QColor(233, 252, 217))
        grad.setColorAt(1.00, QColor(222, 216, 149))
        bg.setBrush(QBrush(grad))
        bg.setPos(0, 0)
        self.scene.addItem(bg)
        text = QGraphicsTextItem()
        text.setHtml("<b>Oyuna Başlamak İçin F5 Tuşuna Basın...<br>"
                     "Space Tuşuna Basarak Zıplayabilirsiniz<br>"
                     "Engellere takıldığınızda tekrar başlamak için<br>"
                     "Tekrar F5 tuşuna basınız.</b><br>")
        text.setFont(QFont("Verdana", 16))
        text.setDefaultTextColor(QColor(0, 169, 230))
        text.setPos(QPointF(20, 130))
        self.scene.addItem(text)

    def start_game(self):
        self.game_started = True
        self.scene.clear()
        self.create_game_window(self.w, self.h)

        self.bird = self.create_bird()
        self.create_obstacle()

        self.timer.start(20)
        self.animation = True
        self.connect(self.timer, SIGNAL("timeout()"), self.update_scene)

    def create_bird(self):
        r = 20
        pix = QPixmap(":/images/bird.png").scaled(r * 2, r * 2)
        b = Bird(r=r, pixmap=pix)
        b.setPos(250, 80)
        self.scene.addItem(b)
        return b

    def create_obstacle(self):
        w, h = 60, randint(30, 250)
        obs = Obstacle(w=w, h=h)
        obs.setPos(720 - w, 0)
        self.scene.addItem(obs)
        self.obstacles.append(obs)

    def create_game_window(self, w, h):
        r = QRectF(0, 0, w, h)
        self.graphicsView.setSceneRect(r)
        game_window = QGraphicsRectItem(r)
        brush = QBrush(QPixmap(":/images/background.png"))
        game_window.setBrush(brush)
        self.scene.addItem(game_window)

    def set_animation_state(self, state):
        if state:
            self.connect(self.timer, SIGNAL("timeout()"), self.update_scene)
        else:
            self.disconnect(self.timer, SIGNAL("timeout()"), self.update_scene)
            self.obstacles = []
            self.animation = False
            self.game_started = False

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_F5:
            self.start_game()
        if event.key() == Qt.Key_Space and self.game_started:
            self.bird.jump()

    def update_scene(self):
        bird_rect = self.bird.get_rect()
        self.scene.update()
        self.bird.update()
        bird_pos = self.bird.scenePos()
        if (bird_pos.y() >= self.h - (2 * self.bird.r)) or (bird_pos.y() <= 0):
            self.set_animation_state(False)
            return
        for obs in self.obstacles:
            obs_rects = obs.get_rects()
            obs.update()
            if bird_rect.intersects(obs_rects[0]) or bird_rect.intersects(obs_rects[1]):
                self.set_animation_state(False)
            if obs.scenePos().x() <= -60:
                self.scene.removeItem(obs)
                self.obstacles.remove(obs)
            if obs.scenePos().x() == 400:
                self.create_obstacle()


def main():
    import sys
    application = QApplication(sys.argv)
    window = Window(w=600, h=400)
    window.show()
    sys.exit(application.exec_())


if __name__ == "__main__":
    main()
