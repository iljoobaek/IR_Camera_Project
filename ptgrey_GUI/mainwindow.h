#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QPushButton>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QTimer>
#include <QPixmap>
#include <QLabel>
#include <QComboBox>
#include <QObject>

#include <QApplication>
#include <bits/stdc++.h>
#include <iostream>
#include <sys/stat.h>
#include <sys/types.h>
#include <string>
#include <ctime>
#include <sys/time.h>
//#include <opencv/highgui.h>
//#include "opencv2/highgui/highgui.hpp"
//#include <opencv2/imgcodecs.hpp>
//#include <cv_bridge/cv_bridge.h>

#include <opencv4/opencv2/core.hpp>
#include <opencv4/opencv2/videoio.hpp>
#include <opencv4/opencv2/highgui.hpp>
#include <opencv4/opencv2/imgproc.hpp>

#include <sstream>
#include <iostream>
#include "FlyCapture2.h"

using namespace std;
//using namespace cv;
using namespace FlyCapture2;

namespace Ui {
class MainWindow;
}

class camera_rgb{
public:
    // initialize cam variables
    FlyCapture2::Error err;
    Camera Cam;
    BusManager busMgr;
    PGRGuid guid;
    Image raw_rgb_frame;
    cv::Mat mat_rgb_frame;
    //cv::Mat rgb_view_frame;
    Image rgbFrame;
    unsigned int rowBytes;
    void get_frame();
    void save_frame(string, string);
};

class make_layout : public QMainWindow
{
    Q_OBJECT

public:
    // make a widget window to hold all the buttons and feed
    QWidget *window = new QWidget;

    // make all the required buttons
    QPushButton *but_StartFeed = new QPushButton("Start Feed", window);
    QPushButton *but_ContFrame = new QPushButton("Save Continuous Frames", window);
    QPushButton *but_StopFrame = new QPushButton("Stop Saving", window);

    // make a vertical layout to accomodate everything
    QVBoxLayout *layout = new QVBoxLayout;
    // make a horizontal layout for the buttons
    QHBoxLayout *button_hor = new QHBoxLayout;

    // layout for left camera
    QVBoxLayout *CamL_Drop = new QVBoxLayout;
    QVBoxLayout *CamR_Drop = new QVBoxLayout;

    // make another horizontal layout to display the video
    QHBoxLayout *video_hor = new QHBoxLayout;

    // make the display widgets for imageLabel
    QLabel *CameraL_view = new QLabel();
    QLabel *CameraR_view = new QLabel();

    QComboBox *Left_drop_down = new QComboBox;
    QComboBox *Right_drop_down = new QComboBox;

    // make two timer objects, one for display and one for saving frames
    QTimer *timer_disp = new QTimer(window);
    QTimer *timer_save = new QTimer(window);

    // flags for display and saving frames
    bool disp_flag = 0;
    bool save_flag = 0;

    // main camera list
    vector<int> main_cam_list;

    camera_rgb *left_camera;
    camera_rgb *right_camera;

    void make_template();
    int initialize_cam(camera_rgb *, int);
    void make_drop_down();
    void start_timers();
public slots:
    void update_frames();
    void save_frames();
    void start_cam_feed();
    void set_save_flag();
    void clear_save_flag();
};

#endif // MAINWINDOW_H
