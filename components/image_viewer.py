from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QDialog,
    QGraphicsPixmapItem,
    QGraphicsScene,
    QGraphicsView,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
)


class ZoomGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._scene = QGraphicsScene(self)
        self._item = QGraphicsPixmapItem()
        self._scene.addItem(self._item)
        self.setScene(self._scene)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)

    def set_pixmap(self, pixmap: QPixmap):
        self._item.setPixmap(pixmap)
        self._scene.setSceneRect(self._item.boundingRect())

    def fit_image(self):
        if not self._item.pixmap().isNull():
            self.resetTransform()
            self.fitInView(self._item, Qt.AspectRatioMode.KeepAspectRatio)

    def zoom_100(self):
        if not self._item.pixmap().isNull():
            self.resetTransform()

    def wheelEvent(self, event):
        if self._item.pixmap().isNull():
            return super().wheelEvent(event)
        self.scale(1.2 if event.angleDelta().y() > 0 else 1 / 1.2, 1.2 if event.angleDelta().y() > 0 else 1 / 1.2)
        event.accept()


class ImageViewer(QDialog):
    def __init__(self, pixmap: QPixmap, title: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(900, 700)
        layout = QVBoxLayout(self)
        self.view = ZoomGraphicsView(self)
        self.view.set_pixmap(pixmap)
        layout.addWidget(self.view, 1)
        controls = QHBoxLayout()
        fit_button = QPushButton("Ajustar")
        fit_button.clicked.connect(self.view.fit_image)
        actual_size_button = QPushButton("100%")
        actual_size_button.clicked.connect(self.view.zoom_100)
        close_button = QPushButton("Fechar")
        close_button.clicked.connect(self.accept)
        controls.addStretch(1)
        controls.addWidget(fit_button)
        controls.addWidget(actual_size_button)
        controls.addWidget(close_button)
        layout.addLayout(controls)

    def showEvent(self, event):
        super().showEvent(event)
        self.view.fit_image()
