from PyQt4.QtCore import QRectF
from PyQt4.QtGui import QGraphicsItemGroup, QLinearGradient, QColor, QBrush, QPen
from baseItem import BaseItem


class PipeItem(BaseItem):
    def __init__(self, x=None, y=None, w=None, h=None):
        super(PipeItem, self).__init__()
        self.rect = QRectF(x, y, w, h)

        gradient = QLinearGradient(0, 0, w, 0)
        gradient.setColorAt(0.0, QColor(56, 180, 74))
        gradient.setColorAt(0.5, QColor(151, 180, 56, 225))
        gradient.setColorAt(1.0, QColor(56, 180, 74))

        self.brush = QBrush(gradient)

        p = QPen(QColor(0, 0, 0))
        p.setWidth(2)
        self.pen = p

    def get_rect(self):
        return self.mapToScene(self.rect).boundingRect()

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget=None):
        painter.setBrush(self.brush)
        painter.setPen(self.pen)
        painter.drawRect(self.rect)


class Obstacle(QGraphicsItemGroup):
    def __init__(self, w=None, h=None):
        super(Obstacle, self).__init__()
        self.rect1 = PipeItem(0, 0, w, h)
        self.rect2 = PipeItem(0, h + 120, w, 280 - h)

        self.addToGroup(self.rect1)
        self.addToGroup(self.rect2)

    def get_rects(self):
        return self.rect1.get_rect(), self.rect2.get_rect()

    def update(self, *args):
        self.setX(self.scenePos().x() - 5)
        super(Obstacle, self).update(*args)
