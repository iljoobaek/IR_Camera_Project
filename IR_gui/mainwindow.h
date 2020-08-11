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
#include <opencv4/opencv2/core.hpp>
#include <opencv4/opencv2/videoio.hpp>
#include <opencv4/opencv2/highgui.hpp>
#include <opencv4/opencv2/imgproc.hpp>
#include <sstream>
#include <iostream>
#include "FlyCapture2.h"

using namespace std;
using namespace cv;
using namespace FlyCapture2;


namespace Ui {
class MainWindow;
}

/** @brief
 * Class with camera all the camera functions
 * Adopted from Python GUI
 */
class Camera_IR{
public:
    int cam_id;
    bool stat;
    Mat frame;
    VideoCapture cap;
    int init_cam(int);
    void get_frame();
    void save_frame(string, string);
};


/** @brief
 * Make the gui layout
 */
class make_layout : public QMainWindow{
    Q_OBJECT

public:
    // make a widget window to hold all the buttons and feed
    QWidget *window = new QWidget;

    // make all required buttons

    //QPushButton *buttonPtr = new QPushButton("Button Name");
    QPushButton *but_StartFeed = new QPushButton("Start Feed", window);
    QPushButton *but_ContFrame = new QPushButton("Save Continuous Frames", window);
    QPushButton *but_StopFrame = new QPushButton("Stop Saving", window);

    // make a vertical layout
    QVBoxLayout *layout = new QVBoxLayout;
    // make a horizontal layout for buttons
    QHBoxLayout *button_hor = new QHBoxLayout;

    // layout for rgb and drop down
    QVBoxLayout *RGB_Drop = new QVBoxLayout;
    // layout for cam L and drop down
    QVBoxLayout *CamL_Drop = new QVBoxLayout;
    // layout for cam R and drop down
    QVBoxLayout *CamR_Drop = new QVBoxLayout;

    // make another horizontal layout to display IR video
    QHBoxLayout *video_hor = new QHBoxLayout;

    // make the display widgets for imageLabel
    QLabel *CameraL_view = new QLabel();
    QLabel *CameraR_view = new QLabel();
    QLabel *RGB_view  = new QLabel();

    // make camera objects
    Camera_IR CamL;
    Camera_IR CamR;

    // make a combo box
    QComboBox *main_drop_down = new QComboBox;
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

    // all the rgb camera variables
    Camera cam_RGB;
    CameraInfo cam_RGB_Info;
    FlyCapture2::Error err = cam_RGB.Connect(0);
    Image raw_rgb_frame;
    Mat mat_rgb_frame;
    Mat rgb_view_frame;
    Image rgbFrame;
    unsigned int rowBytes;
    void save_rgb_frame(string, string);
    void show_rgb();


    void make_template();
    void show_frames(QLabel *cam_label, Camera_IR *cam_obj);
    void make_drop_down(vector<int>);
    void start_timers();
    void acquire_rgb_frame();

public slots:
    void update_frames();
    void save_frames();
    void start_cam_feed();
    void set_save_flag();
    void clear_save_flag();

};

//class MainWindow : public QMainWindow
//{
//    Q_OBJECT

//public:
//    explicit MainWindow(QWidget *parent = 0);
//    ~MainWindow();

//private:
//    Ui::MainWindow *ui;

//};

#endif // MAINWINDOW_H
