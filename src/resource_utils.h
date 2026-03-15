#pragma once

#include <QString>

class RuntimeFiles
{
public:
    RuntimeFiles();
    ~RuntimeFiles();

    QString extractResource(const QString& resourcePath,
                            const QString& fileName);

private:
    class Impl;
    Impl* impl;
};