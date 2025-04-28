cmake_minimum_required(VERSION 3.16)
project(calculatorform LANGUAGES CXX)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt6 REQUIRED COMPONENTS Core Gui Widgets)

qt_add_executable(interface
                  interface.ui main.cpp)

set_target_properties(calculatorform PROPERTIES
    WIN32_EXECUTABLE TRUE
    MACOSX_BUNDLE TRUE
)

target_link_libraries(calculatorform  PUBLIC
    Qt::Core
    Qt::Gui
    Qt::Widgets
)