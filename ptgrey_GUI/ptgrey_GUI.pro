#-------------------------------------------------
#
# Project created by QtCreator 2020-07-06T23:53:33
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = ptgrey_GUI
TEMPLATE = app

DEFINES += QT_DEPRECATED_WARNINGS

SOURCES += \
        main.cpp \
        mainwindow.cpp

INCLUDEPATH += /usr/include/flycapture -I/usr/local/include/opencv4
LIBS +=  -L/usr/local/lib -lopencv_core -lopencv_imgcodecs -lopencv_highgui -lopencv_videoio -lopencv_imgproc

LIBS += -lflycapture



HEADERS  += mainwindow.h

FORMS    += mainwindow.ui
