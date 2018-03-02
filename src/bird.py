from PyQt4.QtCore import QRectF, QPointF
from PyQt4.QtGui import QBrush, QColor, QPen
from baseItem import BaseItem


class Bird(BaseItem):
    def __init__(self, r=None, pixmap=None):
        super(Bird, self).__init__()
        self.r = r
        self.gravity = -0.6
        self._jump = 15
        self.velocity = 0

        self.pixmap = None
        if pixmap:
            self.pixmap = pixmap
        else:
            self.brush = QBrush(QColor(153, 153, 0))
            p = QPen(QColor(0, 0, 0))
            p.setWidth(2)
            self.pen = p

    def get_rect(self):
        return self.mapToScene(self.boundingRect()).boundingRect()

    def jump(self):
        self.velocity += self._jump

    def update(self, *args):
        self.velocity += self.gravity
        self.velocity *= 0.9
        self.setY(self.scenePos().y() - self.velocity)
        super(Bird, self).update(*args)

    def boundingRect(self):
        return QRectF(0, 0, self.r * 2, self.r * 2)

    def paint(self, painter, option, widget=None):
        if self.pixmap is not None:
            painter.drawPixmap(QPointF(0, 0), self.pixmap)
        else:
            painter.setBrush(self.brush)
            painter.setPen(self.pen)
            painter.drawEllipse(0, 0, self.r * 2, self.r * 2)
