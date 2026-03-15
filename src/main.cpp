#include <QGuiApplication>
#include <QQmlContext>
#include <QQuickView>
#include <QWindow>
#include <QUrl>
#include <QFontDatabase>
#include <QDebug>

#include "app_paths.h"
#include "startup_options.h"
#include "resource_utils.h"

static QWindow* wrapParentWindow(WId id)
{
    if (!id)
        return nullptr;

    return QWindow::fromWinId(id);
}

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);
    QGuiApplication::setApplicationName("AnnoyingScreenSaver");

    StartupOptions options = parseStartupOptions(app.arguments());

#ifdef Q_OS_WIN
    if (options.mode == RunMode::Config) {
        return 0;
    }
#endif

    RuntimeFiles runtimeFiles;

    QString videoFile = runtimeFiles.extractResource(
        AppPaths::embeddedVideo(),
        "dog.mp4"
    );

    QString videoUrl = QUrl::fromLocalFile(videoFile).toString();
    QString fontUrl = AppPaths::embeddedFont();
    QString qmlUrl = AppPaths::qmlMain();

    int fontId = QFontDatabase::addApplicationFont(":/assets/fonts/8bitoperator_jve.ttf");
    if (fontId < 0)
        qWarning() << "Failed to load embedded font";

    QQuickView view;

    view.rootContext()->setContextProperty("videoSource", videoUrl);
    view.rootContext()->setContextProperty("fontSource", fontUrl);

    view.setResizeMode(QQuickView::SizeRootObjectToView);
    view.setColor(Qt::black);
    view.setFlags(Qt::FramelessWindowHint);

    view.setSource(QUrl(qmlUrl));

    if (view.status() == QQuickView::Error) {
        auto errors = view.errors();
        for (const auto &err : errors)
            qCritical().noquote() << err.toString();
        return 1;
    }

    if (options.mode == RunMode::EmbeddedPreview) {

        QWindow *parent = wrapParentWindow(options.parentId);

        if (!parent) {
            qCritical() << "QWindow::fromWinId failed";
            return 1;
        }

        view.setParent(parent);

        QRect geom = parent->geometry();

        if (geom.width() > 0 && geom.height() > 0)
            view.setGeometry(0, 0, geom.width(), geom.height());
        else
            view.resize(800, 600);

        view.show();

    } else {

        view.showFullScreen();

    }

    return app.exec();
}