#include "app_paths.h"

namespace AppPaths {

QString qmlMain()
{
    return QStringLiteral("qrc:/qml/main.qml");
}

QString embeddedFont()
{
    return QStringLiteral("qrc:/assets/fonts/8bitoperator_jve.ttf");
}

}