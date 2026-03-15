#include <QGuiApplication>
#include <QQmlContext>
#include <QQmlEngine>
#include <QQuickView>
#include <QWindow>
#include <QUrl>
#include <QFontDatabase>
#include <QCoreApplication>
#include <QDebug>
#include <QObject>

#include "app_paths.h"
#include "startup_options.h"

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

    const QString fontUrl = AppPaths::embeddedFont();
    const QString qmlUrl = AppPaths::qmlMain();

    const QString fontResourcePath = fontUrl.startsWith("qrc:")
        ? QStringLiteral(":") + fontUrl.mid(4)
        : fontUrl;

    const int fontId = QFontDatabase::addApplicationFont(fontResourcePath);
    if (fontId < 0)
        qWarning() << "Failed to load embedded font:" << fontResourcePath;

    QQuickView view;

    QObject::connect(
        view.engine(),
        &QQmlEngine::quit,
        &app,
        &QCoreApplication::quit
    );

    view.rootContext()->setContextProperty("fontSource", fontUrl);

    view.setResizeMode(QQuickView::SizeRootObjectToView);
    view.setColor(Qt::black);
    view.setFlags(Qt::FramelessWindowHint);
    view.setSource(QUrl(qmlUrl));

    if (view.status() == QQuickView::Error) {
        const auto errors = view.errors();
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

        const QRect geom = parent->geometry();

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