#include "startup_options.h"

#include <QProcessEnvironment>
#include <QString>

#ifdef Q_OS_WIN
#include <windows.h>
#endif

StartupOptions parseStartupOptions(const QStringList& args)
{
    StartupOptions opt;

#ifdef Q_OS_WIN

    if (args.size() >= 2) {

        QString arg = args.at(1).toLower();

        if (arg.startsWith("/c") || arg.startsWith("-c")) {
            opt.mode = RunMode::Config;
            return opt;
        }

        if (arg.startsWith("/s") || arg.startsWith("-s")) {
            opt.mode = RunMode::Fullscreen;
            return opt;
        }

        if (arg.startsWith("/p") || arg.startsWith("-p")) {

            opt.mode = RunMode::EmbeddedPreview;

            QString handle;

            int sep = arg.indexOf(':');

            if (sep >= 0)
                handle = arg.mid(sep + 1);
            else if (args.size() >= 3)
                handle = args.at(2);

            bool ok = false;

#ifdef _WIN64
            qulonglong value = handle.toULongLong(&ok);
#else
            ulong value = handle.toULong(&ok);
#endif

            if (ok)
                opt.parentId = static_cast<WId>(value);

            return opt;
        }
    }

#endif

    QByteArray xs = qgetenv("XSCREENSAVER_WINDOW");

    if (!xs.isEmpty()) {

        bool ok = false;

        qulonglong id = QString::fromLatin1(xs).toULongLong(&ok, 0);

        if (ok) {
            opt.mode = RunMode::EmbeddedPreview;
            opt.parentId = static_cast<WId>(id);
            return opt;
        }
    }

    opt.mode = RunMode::Fullscreen;
    return opt;
}