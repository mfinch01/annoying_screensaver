import os
os.environ["LC_NUMERIC"] = "C"

import locale
locale.setlocale(locale.LC_NUMERIC, "C")

import sys
import random
from datetime import datetime

from PySide6.QtCore import Qt, QTimer, QRect, QPoint
from PySide6.QtGui import QPainter, QColor, QFont, QFontMetrics
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

import mpv


class MatrixOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.columns = []
        self.chars = "01アイウエオカキクケコサシスセソABCDEFGHIJKLMNOPQRSTUVWXYZ#$%&*+-="
        self.font = QFont("JetBrains Mono", 14)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(50)

    def resizeEvent(self, event):
        fm = QFontMetrics(self.font)
        cell_w = max(10, fm.horizontalAdvance("W"))
        count = max(1, self.width() // cell_w)

        self.columns = []
        for i in range(count):
            self.columns.append({
                "x": i * cell_w,
                "y": random.randint(-500, 0),
                "speed": random.randint(8, 22),
                "length": random.randint(8, 24),
            })

        super().resizeEvent(event)

    def tick(self):
        for col in self.columns:
            col["y"] += col["speed"]
            if col["y"] - col["length"] * 18 > self.height() + 100:
                col["y"] = random.randint(-500, -50)
                col["speed"] = random.randint(8, 22)
                col["length"] = random.randint(8, 24)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setFont(self.font)

        # Положение псевдо-терминала
        term_rect = QRect(
            int(self.width() * 0.58),
            int(self.height() * 0.10),
            int(self.width() * 0.32),
            int(self.height() * 0.58),
        )

        # Фон окна терминала
        painter.fillRect(term_rect, QColor(0, 0, 0, 155))

        # Заголовок окна
        title_h = 34
        painter.fillRect(
            term_rect.x(),
            term_rect.y(),
            term_rect.width(),
            title_h,
            QColor(28, 28, 28, 220),
        )

        painter.setPen(QColor(230, 230, 230))
        painter.drawText(term_rect.adjusted(70, 0, -10, 0), Qt.AlignVCenter, "gnome-terminal")

        # Кнопки окна
        for i, color in enumerate([QColor("#ff5f56"), QColor("#ffbd2e"), QColor("#27c93f")]):
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPoint(term_rect.x() + 18 + i * 18, term_rect.y() + 17), 5, 5)

        # Матрица внутри терминала
        painter.setFont(self.font)
        char_h = 18
        content_left = term_rect.x() + 10
        content_right = term_rect.right() - 10
        content_top = term_rect.y() + title_h + 10
        content_bottom = term_rect.bottom() - 10
        usable_w = max(20, content_right - content_left)

        for col in self.columns:
            x = content_left + (col["x"] % usable_w)
            for j in range(col["length"]):
                y = content_top + col["y"] - j * char_h
                if y < content_top or y > content_bottom:
                    continue

                ch = random.choice(self.chars)
                alpha = max(25, 255 - j * 12)
                color = QColor(80, 255, 120, alpha)
                if j == 0:
                    color = QColor(230, 255, 230, 255)

                painter.setPen(color)
                painter.drawText(x, y, ch)


class ClockOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.time_label = QLabel(self)
        self.date_label = QLabel(self)

        self.time_label.setStyleSheet("""
            color: white;
            background: transparent;
        """)
        self.date_label.setStyleSheet("""
            color: rgba(255,255,255,220);
            background: transparent;
        """)

        self.time_label.setFont(QFont("Inter", 72, QFont.DemiBold))
        self.date_label.setFont(QFont("Inter", 26))

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

    def resizeEvent(self, event):
        # Положение часов
        self.time_label.setGeometry(70, self.height() - 180, 500, 90)
        self.date_label.setGeometry(74, self.height() - 105, 800, 40)
        super().resizeEvent(event)

    def update_time(self):
        now = datetime.now()
        self.time_label.setText(now.strftime("%H:%M"))
        self.date_label.setText(now.strftime("%A, %d %B %Y"))


class VideoContainer(QWidget):
    pass


class MainWindow(QWidget):
    def __init__(self, video_path):
        super().__init__()

        self.setWindowTitle("Custom Python Screensaver")
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.setCursor(Qt.BlankCursor)
        self.setStyleSheet("background: black;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.video = VideoContainer(self)
        layout.addWidget(self.video)

        self.clock = ClockOverlay(self)
        self.clock.raise_()

        self.matrix = MatrixOverlay(self)
        self.matrix.raise_()

        self.player = mpv.MPV(
            wid=str(int(self.video.winId())),
            input_default_bindings=False,
            input_vo_keyboard=False,
            osc=False,
            loop_file="inf",
            fs="yes",
            keep_open="yes",
            audio="no",
        )

        self.player.play(video_path)
        self.showFullScreen()

    def resizeEvent(self, event):
        self.clock.setGeometry(self.rect())
        self.matrix.setGeometry(self.rect())
        super().resizeEvent(event)

    def keyPressEvent(self, event):
        self.close()

    def mouseMoveEvent(self, event):
        self.close()

    def mousePressEvent(self, event):
        self.close()

    def closeEvent(self, event):
        try:
            self.player.terminate()
        except Exception:
            pass
        super().closeEvent(event)


def main():
    if len(sys.argv) < 2:
        print("Использование:")
        print("  python3 screensaver.py /полный/путь/к/видео.mp4")
        sys.exit(1)

    video_path = sys.argv[1]

    app = QApplication(sys.argv)
    window = MainWindow(video_path)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()