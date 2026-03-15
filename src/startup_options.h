#pragma once

#include <QStringList>
#include <QtGui/qwindowdefs.h>

enum class RunMode
{
    Fullscreen,
    EmbeddedPreview,
    Config
};

struct StartupOptions
{
    RunMode mode = RunMode::Fullscreen;
    WId parentId = 0;
};

StartupOptions parseStartupOptions(const QStringList& args);