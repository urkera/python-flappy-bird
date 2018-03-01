from PyQt4.QtGui import QGraphicsView
from PyQt4.QtCore import QRectF, Qt


class GView(QGraphicsView):
    def __init__(self, parent):
        super(GView, self).__init__(parent)

        self.zoom_avaliable = False

        self.left_clicked = False
        self.previous_pos = None

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.is_panning = False
        self.mouse_pressed = False
        self.drag_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = True
            if self.is_panning:
                self.setCursor(Qt.ClosedHandCursor)
                self.drag_pos = event.pos()
                event.accept()
            else:
                super(GView, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.mouse_pressed and self.is_panning:
            new_pos = event.pos()
            diff = new_pos - self.drag_pos
            self.drag_pos = new_pos
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - diff.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - diff.y())
            event.accept()
        else:
            super(GView, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if event.modifiers() & Qt.ControlModifier:
                self.setCursor(Qt.OpenHandCursor)
            else:
                self.is_panning = False
                self.setCursor(Qt.ArrowCursor)
            self.mouse_pressed = False
        super(GView, self).mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control and not self.mouse_pressed:
            self.is_panning = True
            self.setCursor(Qt.OpenHandCursor)
        else:
            super(GView, self).keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            if not self.mouse_pressed:
                self.is_panning = False
                self.setCursor(Qt.ArrowCursor)
        else:
            super(GView, self).keyPressEvent(event)

    def wheelEvent(self, event):
        if not self.zoom_avaliable:
            return

        zoom_factor = 2.0 ** (event.delta() / 240.0)

        self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.setResizeAnchor(QGraphicsView.NoAnchor)

        old_pos = self.mapToScene(event.pos())

        factor = self.matrix().scale(zoom_factor, zoom_factor).mapRect(QRectF(0, 0, 1, 1)).width()

        if factor < 0.0007 or factor > 1000:
            return

        self.scale(zoom_factor, zoom_factor)

        new_pos = self.mapToScene(event.pos())

        delta = new_pos - old_pos
        self.translate(delta.x(), delta.y())
