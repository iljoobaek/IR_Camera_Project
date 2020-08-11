#include "mainwindow.h"
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
#include "FlyCapture2.h"

using namespace std;
using namespace cv;
using namespace FlyCapture2;

/**********GLOBAL VARS***********/
string current_dt;

/** @brief
 * Get the current date and time stamp as a string
 */
string Get_DateTime(){
    time_t rawtime;
    timeval currentTime;
    struct tm *timeinfo;

    char buffer[80];
    gettimeofday(&currentTime, NULL);
    int milli = currentTime.tv_usec / 1000;

    time(&rawtime);
    timeinfo = localtime(&rawtime);

    strftime(buffer, sizeof(buffer), "%d_%m_%Y_%H_%M_%S", timeinfo);

    char Current_Time[84] = "";
    sprintf(Current_Time, "%s_%03d", buffer, milli);
    return Current_Time;
}

/** @brief
 * Return the camera ids, open the cams from
 * index 0-10 and append the opened cam ids to
 * the empty vector array created in the function
 * @param[in] None
 * @return result_vector
 */
vector<int> get_camIds(){
    vector<int> camIds;
    VideoCapture cap;
    for (int i=0; i<10; i++){
        cap.open(i);
        if (cap.isOpened()){
            camIds.push_back(i);
        }
        cap.release();
    }
    return camIds;
}

/** @brief
 * Create the directory to save images
*/
int create_dirs(){
    if (mkdir("image", 0777) == -1){
        cout << "directory already present" << endl;
        return 0;
    }
    else{
        return 0;
    }
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
 * Initialize the camera with the given cam number and open it
 * if it opens return 0 indicating success or if not, 1 indicating
 * failure.
 */
int Camera_IR::init_cam(int cam_num){
    cam_id = cam_num;
    // use the default camera api, or autodetect it
    int ApiID = cv::CAP_ANY;
    // open the camera with the said id
    cap.open(cam_num, ApiID);
    // if an error occured, print and exit
    if(!cap.isOpened()){
        cout<<"Error, unable to open the required camera"<<endl;
        return 1;
    }
    // otherwise return 0 to indicate success
    return 0;
}

/** @brief
 * Get the latest camera frame, useful for timed calls
 */
void Camera_IR::get_frame(){
    cap.read(frame);
}

/** @brief
 * Save the frames to desired folder
 */
void Camera_IR::save_frame(string current_date_time, string img_type){
    string image_name = "image/" + img_type + current_date_time +".tiff";
    imwrite(image_name, frame);
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

    // add the Rgb cam to the the v layout
    RGB_Drop->addWidget(main_drop_down);
    RGB_Drop->addWidget(RGB_view);

    // add this layout to the vertical layout
    layout->addLayout(RGB_Drop);

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

/** @brief
 * Show the frames in the display widget, Qlabel
 */
void make_layout::show_frames(QLabel *cam_label, Camera_IR *cam_obj){
    // access the recently acquired frame from the camera object and show

    cvtColor(cam_obj->frame, cam_obj->frame, COLOR_BGR2GRAY);
    // convert frame to qimage
    QPixmap new_pix = QPixmap::fromImage(QImage((unsigned char*)cam_obj->frame.data,
                                                cam_obj->frame.cols,
                                                cam_obj->frame.rows,
                                                QImage::Format_Grayscale8));
    cam_label->setPixmap(new_pix);
}

/** @brief
 * update the camera L and R frames if feed is on
 */
void make_layout::update_frames(){
    if (disp_flag){
        CamL.get_frame();
        CamR.get_frame();
//        if (err == PGRERROR_OK){
//            acquire_rgb_frame();
//            show_rgb();
//        }
        //show_frames(CameraL_view, &CamL);
        //show_frames(CameraR_view, &CamR);
    }
}

/** @brief
 * show the camera L and R frames if the save flag is active
 */
void make_layout::save_frames(){
    if (save_flag){
        current_dt = Get_DateTime();
        CamL.save_frame(current_dt, "CamL_");
        CamR.save_frame(current_dt, "CamR_");
//        if (err == PGRERROR_OK){
//            save_rgb_frame(current_dt, "RGB_");
//        }
    }
}

/** @brief
 * start the qt timers and connect them to respective functions
 */
void make_layout::start_timers(){
    QObject::connect(timer_disp, SIGNAL(timeout()), this, SLOT(update_frames()));
    QObject::connect(timer_save, SIGNAL(timeout()), this, SLOT(save_frames()));
    // make connections to functions for other buttons as well
    QObject::connect(but_StartFeed, SIGNAL(clicked(bool)), this, SLOT(start_cam_feed()));
    QObject::connect(but_ContFrame, SIGNAL(clicked(bool)), this, SLOT(set_save_flag()));
    QObject::connect(but_StopFrame, SIGNAL(clicked(bool)), this, SLOT(clear_save_flag()));
    timer_disp->start(10);
    timer_save->start(10);
}

void make_layout::set_save_flag(){
    save_flag = 1;
}

void make_layout::clear_save_flag(){
    save_flag = 0;
}


/** @brief
 * make the drop down menus to show camera indices
 */
void make_layout::make_drop_down(vector<int> cam_list){

    main_cam_list = cam_list;
    string RGB_camera = "CAM_RGB";
    main_drop_down->addItem(RGB_camera.c_str(), "RGB");
    Left_drop_down->addItem(RGB_camera.c_str(), "RGB");
    Right_drop_down->addItem(RGB_camera.c_str(),"RGB");

    for(int i=0; i<cam_list.size(); i++){
        string cam_id = "CAM_" + to_string(cam_list[i]);
        main_drop_down->addItem(cam_id.c_str(), to_string(cam_list[i]).c_str());
        Left_drop_down->addItem(cam_id.c_str(), to_string(cam_list[i]).c_str());
        Right_drop_down->addItem(cam_id.c_str(), to_string(cam_list[i]).c_str());
    }
}

/** @brief
 * Start the cam feed and initialize the cameras
 */
void make_layout::start_cam_feed(){
    int idRGB   = main_drop_down->currentIndex();
    int idLeft  = Left_drop_down->currentIndex();
    int idRight = Right_drop_down->currentIndex();
    CamL.init_cam(main_cam_list[idLeft-1]);
    CamR.init_cam(main_cam_list[idRight-1]);
//    if (err == PGRERROR_OK){
//        cam_RGB.StartCapture();
//    }
    disp_flag = 1;
}

/** @brief
 * Acquire the rgb frame and convert it to opencv matrix format
 */
void make_layout::acquire_rgb_frame(){
    // retrieve the raw frame
    cam_RGB.RetrieveBuffer(&raw_rgb_frame);
    // convert from bgr to rgb
    raw_rgb_frame.Convert(FlyCapture2::PIXEL_FORMAT_BGR, &rgbFrame);
    // convert to the opencv matrix format
    rowBytes = (double)rgbFrame.GetReceivedDataSize()/(double)rgbFrame.GetRows();
    mat_rgb_frame = Mat(rgbFrame.GetRows(), rgbFrame.GetCols(), CV_8UC3, rgbFrame.GetData(), rowBytes);
}

/** @brief
 * display the rgb frame
 */
void make_layout::show_rgb(){
    // convert frame to qimage
    cv::resize(mat_rgb_frame, rgb_view_frame, cv::Size(), 0.3, 0.3);
    cvtColor(rgb_view_frame, rgb_view_frame, COLOR_BGR2GRAY);
    QPixmap rgb_pix = QPixmap::fromImage(QImage((unsigned char*)rgb_view_frame.data,
                                                rgb_view_frame.cols,
                                                rgb_view_frame.rows,
                                                QImage::Format_Grayscale8));
    RGB_view->setPixmap(rgb_pix);
}

/** @brief
 * Save the rgb frames with given date time stamp to desired folder
 */
void make_layout::save_rgb_frame(string current_date_time, string img_type){
    string image_name = "image/" + img_type + current_date_time +".tiff";
    imwrite(image_name, mat_rgb_frame);
}

// Main function
int main(int argc, char *argv[])
{
    // create the image dirs
    create_dirs();

    // get the list of available cameras and print them
    vector<int> open_cams = get_camIds();
    cout << "The list of cams : ";
    print_vec(open_cams);

    // print the current time and date
    cout << Get_DateTime() << endl;
    current_dt = Get_DateTime();

    // start the application
    QApplication a(argc, argv);
    //MainWindow w;
    // w.show();

    // test the widget
    make_layout NewLayOut;
    NewLayOut.make_drop_down(open_cams);
    NewLayOut.make_template();
    NewLayOut.start_timers();
    // NewLayOut.show_frames(NewLayOut.CameraL_view , &NewLayOut.CamL);

    // convert a qt string to string and display
    cout << NewLayOut.Left_drop_down->currentText().toUtf8().constData() << endl;
    cout << NewLayOut.Left_drop_down->currentIndex() << endl;

    return a.exec();
}
