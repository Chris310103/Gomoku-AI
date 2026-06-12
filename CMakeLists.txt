cmake_minimum_required(VERSION 3.16)

project(GomokuAI LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt6 REQUIRED COMPONENTS Widgets)

set(QT_APP_SRC ${CMAKE_SOURCE_DIR}/apps/desktop/src)

add_executable(${PROJECT_NAME}
    ${QT_APP_SRC}/main.cpp
    ${QT_APP_SRC}/mainwindow.h
    ${QT_APP_SRC}/mainwindow.cpp
    ${QT_APP_SRC}/boardwidget.h
    ${QT_APP_SRC}/boardwidget.cpp
    ${QT_APP_SRC}/gamemodel.h
    ${QT_APP_SRC}/gamemodel.cpp
    ${QT_APP_SRC}/gamecontroller.h
    ${QT_APP_SRC}/gamecontroller.cpp
    ${QT_APP_SRC}/aiclient.h
    ${QT_APP_SRC}/aiclient.cpp
    ${QT_APP_SRC}/python_ai_process.h
    ${QT_APP_SRC}/python_ai_process.cpp
)

target_link_libraries(${PROJECT_NAME} PRIVATE Qt6::Widgets)

add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
    ${CMAKE_SOURCE_DIR}/gomoku_ai/search/ai_stdin.py
    $<TARGET_FILE_DIR:${PROJECT_NAME}>/ai_stdin.py
)
