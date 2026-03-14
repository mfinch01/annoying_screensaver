import os
import sys

from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QGuiApplication, QWindow
from PyQt6.QtQuick import QQuickView


def main():
    app = QGuiApplication(sys.argv)

    base_dir = os.path.dirname(os.path.abspath(__file__))

    video_path = os.path.join(base_dir, "dog.mp4")
    font_path = os.path.join(base_dir, "8bitoperator_jve.ttf")
    qml_path = os.path.join(base_dir, "main.qml")

    view = QQuickView()
    view.rootContext().setContextProperty(
        "videoSource",
        QUrl.fromLocalFile(video_path).toString()
    )
    view.rootContext().setContextProperty(
        "fontSource",
        QUrl.fromLocalFile(font_path).toString()
    )
    view.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
    view.setColor(Qt.GlobalColor.black)
    view.setSource(QUrl.fromLocalFile(qml_path))

    if view.status() == QQuickView.Status.Error:
        for err in view.errors():
            print(err.toString(), file=sys.stderr)
        sys.exit(1)

    xs_win = os.environ.get("XSCREENSAVER_WINDOW")

    if xs_win:
        # Режим XScreenSaver: встраиваемся в переданное X11-окно
        try:
            win_id = int(xs_win, 0)
        except ValueError:
            print(f"Bad XSCREENSAVER_WINDOW: {xs_win}", file=sys.stderr)
            sys.exit(1)

        parent = QWindow.fromWinId(win_id)
        if parent is None:
            print("QWindow.fromWinId() failed", file=sys.stderr)
            sys.exit(1)

        view.setFlags(Qt.WindowType.FramelessWindowHint)
        view.setParent(parent)

        geom = parent.geometry()
        if geom.width() > 0 and geom.height() > 0:
            view.setGeometry(0, 0, geom.width(), geom.height())
        else:
            view.resize(800, 600)

        view.show()
    else:
        # Обычный режим: своё fullscreen окно
        view.setFlags(Qt.WindowType.FramelessWindowHint)
        view.showFullScreen()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()