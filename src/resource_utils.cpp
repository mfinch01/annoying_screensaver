#include "resource_utils.h"

#include <QTemporaryDir>
#include <QFile>
#include <QByteArray>
#include <QDebug>

class RuntimeFiles::Impl
{
public:
    QTemporaryDir tempDir;
};

RuntimeFiles::RuntimeFiles()
{
    impl = new Impl();

    if (!impl->tempDir.isValid())
        qFatal("Failed to create temporary directory");
}

RuntimeFiles::~RuntimeFiles()
{
    delete impl;
}

QString RuntimeFiles::extractResource(const QString& resourcePath,
                                       const QString& fileName)
{
    QFile in(resourcePath);

    if (!in.open(QIODevice::ReadOnly))
        qFatal("Cannot open resource %s", qPrintable(resourcePath));

    QString outPath = impl->tempDir.filePath(fileName);

    QFile out(outPath);

    if (!out.open(QIODevice::WriteOnly))
        qFatal("Cannot create temp file %s", qPrintable(outPath));

    QByteArray data = in.readAll();

    if (out.write(data) != data.size())
        qFatal("Failed writing temp file");

    out.close();

    return outPath;
}