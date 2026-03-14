import os
import sys

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine


def main():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    base_dir = os.path.dirname(os.path.abspath(__file__))

    video_path = os.path.join(base_dir, "dog.mp4")
    font_path = os.path.join(base_dir, "8bitoperator_jve.ttf")
    qml_path = os.path.join(base_dir, "main.qml")

    engine.rootContext().setContextProperty(
        "videoSource",
        QUrl.fromLocalFile(video_path).toString()
    )
    engine.rootContext().setContextProperty(
        "fontSource",
        QUrl.fromLocalFile(font_path).toString()
    )

    engine.load(QUrl.fromLocalFile(qml_path))

    if not engine.rootObjects():
        sys.exit(1)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()