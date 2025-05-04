import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtGui import QPainter, QPen, QColor, QScreen
from PIL import ImageGrab

class ScreenshotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.start_point = QPoint()
        self.end_point = QPoint()
        self.dragging = False

    def init_ui(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 60);")
        self.showFullScreen()

        # Bouton de fermeture
        self.close_btn = QPushButton("×", self)
        self.close_btn.setFixedSize(40, 40)
        self.close_btn.move(self.screen().geometry().width()//2 - 20, 20)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #555555;
                border: 2px solid #777777;
                border-radius: 20px;
                color: white;
                font-size: 24px;
            }
            QPushButton:hover { background-color: #666666; }
        """)
        self.close_btn.clicked.connect(self.close)

    def paintEvent(self, event):
        if self.dragging:
            painter = QPainter(self)
            painter.setPen(QPen(Qt.gray, 2))
            painter.setBrush(QColor(128, 128, 128, 50))
            painter.drawRect(QRect(self.start_point, self.end_point))

    def get_scaled_rect(self):
        # Ajustement pour le scaling DPI
        screen = self.screen()
        scale_factor = screen.devicePixelRatio()
        
        rect = QRect(self.start_point, self.end_point).normalized()
        return QRect(
            int(rect.x() * scale_factor),
            int(rect.y() * scale_factor),
            int(rect.width() * scale_factor),
            int(rect.height() * scale_factor)
        )

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_point = event.position().toPoint()
            self.end_point = self.start_point
            self.dragging = True

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.end_point = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            scaled_rect = self.get_scaled_rect()
            
            # Capture avec Pillow
            screenshot = ImageGrab.grab(bbox=(
                scaled_rect.x(),
                scaled_rect.y(),
                scaled_rect.x() + scaled_rect.width(),
                scaled_rect.y() + scaled_rect.height()
            ))
            
            screenshot.save("C:/capture_test.png")  # Chemin absolu pour test
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScreenshotWindow()
    window.show()
    app.exec()