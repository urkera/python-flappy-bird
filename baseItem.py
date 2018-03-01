from PyQt4.QtGui import QGraphicsItem, QBrush, QPen
from PyQt4.QtCore import Qt


class BaseItem(QGraphicsItem):
    def __init__(self, pen=None, brush=None):
        super(BaseItem, self).__init__()
        self._pen = None
        self._brush = None
        self.set_pen(pen)
        self.set_brush(brush)

    def get_brush(self):
        return self._brush

    def set_brush(self, brush):
        self._brush = QBrush(Qt.NoBrush)
        if (brush is not None) and isinstance(brush, QBrush):
            self._brush = brush

    brush = property(get_brush, set_brush)

    def get_pen(self):
        return self._pen

    def set_pen(self, pen):
        self._pen = QPen(Qt.NoPen)
        if (pen is not None) and isinstance(pen, QPen):
            self._pen = pen

    pen = property(get_pen, set_pen)
