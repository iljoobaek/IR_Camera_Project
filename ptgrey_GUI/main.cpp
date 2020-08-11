#include "mainwindow.h"
#include <QApplication>
#include <bits/stdc++.h>
#include <iostream>
#include <sys/stat.h>
#include <sys/types.h>
#include <string>
#include <ctime>
#include <sys/time.h>
#include "FlyCapture2.h"
#include <time.h>
#include <cstdlib>
#include <time.h>

using namespace std;
//using namespace cv;
using namespace FlyCapture2;

/*********** GLIBAL VARS *********/
string current_dt;

/** @brief
 * Get the current date and time as string
 */
string Get_Date_Time(){
    time_t rawtime;
    timeval currentTime;
    struct tm *timeinfo;

    char buffer[80];
    gettimeofday(&currentTime, NULL);
    int milli = currentTime.tv_usec/1000;
    time(&rawtime);
    timeinfo = localtime(&rawtime);

    strftime(buffer, sizeof(buffer), "%d_%m_%Y_%H_%M_%S", timeinfo);
    char Current_Time[84] = "";
    sprintf(Current_Time, "%s_%03d", buffer, milli);
    return Current_Time;
}

/** @brief
 * Create the directory to save images
 */
int create_dirs(){
    if (mkdir("image", 0777) == -1){
        cout << "directory already present" << endl;
        return 0;
    }
    else return 0;
}

/** @brief
* Function to Print the vector as a string
*/
void print_vec(vector<int> const &ip_vector){
   for(uint i = 0; i < ip_vector.size(); i++){
       cout << ip_vector.at(i) << " ";
   }
}

/** @brief
* Make the basic layout with buttons and provisions for widgets
*/
void make_layout::make_template(){
   // add the buttons to hor layout
   button_hor->addWidget(but_ContFrame);
   button_hor->addWidget(but_StopFrame);

   // add the start feed button and layout of start stop buttons
   layout->addWidget(but_StartFeed);
   layout->addLayout(button_hor);


   // add the drop down menu to camL widget
   CamL_Drop->addWidget(Left_drop_down);
   CamL_Drop->addWidget(CameraL_view);

   // add the drop down to cam R widget
   CamR_Drop->addWidget(Right_drop_down);
   CamR_Drop->addWidget(CameraR_view);

   // add the two cameras to the horizontal video widget
   video_hor->addLayout(CamL_Drop);
   video_hor->addLayout(CamR_Drop);

   // add the video hor layout to the main layout
   layout->addLayout(video_hor);

   window->setLayout(layout);
   window->show();
}

int make_layout::initialize_cam(camera_rgb *cam, int cam_num){
    cam->busMgr.GetCameraFromIndex(cam_num, &cam->guid);
    cam->err = cam->Cam.Connect(&cam->guid);
    if (cam->err != PGRERROR_OK){
        cout << "Please connect the camera" << endl;
        return 1;
    }
    else{
        cam->Cam.StartCapture();
        return 0;
    }
}

void camera_rgb::get_frame(){
    // retrieve the raw frame
    Cam.RetrieveBuffer(&raw_rgb_frame);
    raw_rgb_frame.Convert(FlyCapture2::PIXEL_FORMAT_BGR, &rgbFrame);
    // convert to opencv matrix form
    rowBytes = (double)rgbFrame.GetReceivedDataSize()/(double)rgbFrame.GetRows();
    mat_rgb_frame = cv::Mat(rgbFrame.GetRows(), rgbFrame.GetCols(), CV_8UC3, rgbFrame.GetData(), rowBytes);
    cv::flip(mat_rgb_frame, mat_rgb_frame, 0);
    cv::flip(mat_rgb_frame, mat_rgb_frame, +1);
}

void camera_rgb::save_frame(string current_date_time, string img_type){
    string image_name = "image/" + img_type + current_date_time +".tiff";
    ostringstream Image;
    Image << image_name;
    raw_rgb_frame.Save(Image.str().c_str());

    //Cam.Save(leftImage.str().c_str());
    cv::imwrite(image_name, mat_rgb_frame);
}

void make_layout::make_drop_down(){
    string RGB_Left = "Cam_Rgb_0";
    string RGB_Right = "Cam_Rgb_1";

    Left_drop_down->addItem(RGB_Left.c_str(), "RGBL");
    Left_drop_down->addItem(RGB_Right.c_str(), "RGBR");

    Right_drop_down->addItem(RGB_Left.c_str(), "RGBR");
    Right_drop_down->addItem(RGB_Right.c_str(), "RGBL");
}

void make_layout::start_timers(){
    QObject::connect(timer_disp, SIGNAL(timeout()), this, SLOT(update_frames()));
    QObject::connect(timer_save, SIGNAL(timeout()), this, SLOT(save_frames()));
    QObject::connect(but_StartFeed, SIGNAL(clicked(bool)), this, SLOT(start_cam_feed()));
    QObject::connect(but_ContFrame, SIGNAL(clicked(bool)), this, SLOT(set_save_flag()));
    QObject::connect(but_StopFrame, SIGNAL(clicked(bool)), this, SLOT(clear_save_flag()));
    timer_disp->start(60);
    timer_save->start(60);
}

void make_layout::update_frames(){
    if (disp_flag == 1){
        left_camera->get_frame();
        right_camera->get_frame();
//        cv::cvtColor(left_camera->mat_rgb_frame, left_camera->mat_rgb_frame, cv::COLOR_BGR2GRAY);
//        cv::cvtColor(right_camera->mat_rgb_frame, right_camera->mat_rgb_frame, cv::COLOR_BGR2GRAY);
//        QPixmap Left_img = QPixmap::fromImage(QImage((unsigned char*)left_camera->mat_rgb_frame.data,
//                                              left_camera->mat_rgb_frame.cols,
//                                              left_camera->mat_rgb_frame.rows,
//                                              QImage::Format_Grayscale8));
//        QPixmap Right_img = QPixmap::fromImage(QImage((unsigned char*)right_camera->mat_rgb_frame.data,
//                                              right_camera->mat_rgb_frame.cols,
//                                              right_camera->mat_rgb_frame.rows,
//                                              QImage::Format_Grayscale8));
//        CameraL_view->setPixmap(Left_img);
//        CameraR_view->setPixmap(Right_img);

    }
}

void make_layout::save_frames(){
    if (save_flag == 1){
        current_dt = Get_Date_Time();
        left_camera->save_frame(current_dt, "CamL_");
        right_camera->save_frame(current_dt, "CamR_");
    }
}


void make_layout::start_cam_feed(){
    int idLeft  = Left_drop_down->currentIndex();
    int idRight = Right_drop_down->currentIndex();
    initialize_cam(left_camera, idLeft);
    initialize_cam(right_camera, idRight);
    std::cout << "both cams initialized" << endl;
    disp_flag = 1;
}


void make_layout::set_save_flag(){
    save_flag = 1;
}

void make_layout::clear_save_flag(){
    save_flag = 0;
}

int main(int argc, char *argv[])
{
    cout << Get_Date_Time() << endl;
    QApplication a(argc, argv);

    camera_rgb Cam_L;
    camera_rgb Cam_R;
    create_dirs();

    make_layout NewLayOut;
    NewLayOut.make_drop_down();
    NewLayOut.left_camera = &Cam_L;
    NewLayOut.right_camera = &Cam_R;
    NewLayOut.make_template();
    NewLayOut.start_timers();

//    NewLayOut.initialize_cam(&Cam_L, 0);
//    Cam_L.get_frame();
//    Cam_L.save_frame(Get_Date_Time(), "CamL");


    return a.exec();
}
