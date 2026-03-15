cmake_minimum_required(VERSION 3.21)
project(AnnoyingScreenSaver LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 REQUIRED COMPONENTS Core Gui Qml Quick Multimedia)

qt_standard_project_setup()

qt_add_executable(AnnoyingScreenSaver
    src/main.cpp
    src/app_paths.cpp
    src/resource_utils.cpp
    src/startup_options.cpp
    resources/resources.qrc
)

target_include_directories(AnnoyingScreenSaver PRIVATE src)

target_link_libraries(AnnoyingScreenSaver PRIVATE
    Qt6::Core
    Qt6::Gui
    Qt6::Qml
    Qt6::Quick
    Qt6::Multimedia
)

if (WIN32)
    set_target_properties(AnnoyingScreenSaver PROPERTIES
        WIN32_EXECUTABLE TRUE
    )
endif()