// License: Apache 2.0. See LICENSE file in root directory.
// Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

#include <librealsense2/rs.hpp> // Include RealSense Cross Platform API

#include <fstream>              // File IO
#include <iostream>             // Terminal IO
#include <sstream>              // Stringstreams
#include <opencv2/opencv.hpp>
#include <opencv2/viz.hpp>
#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/imgcodecs.hpp>
#include <ctime>
#include <sys/time.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <string>
#include <cmath>
// // 3rd party header for writing png files
// #define STB_IMAGE_WRITE_IMPLEMENTATION
// #include "stb_image_write.h"
using namespace std;
using namespace cv;

// Helper function for writing metadata to disk as a csv file
void metadata_to_csv(const rs2::frame& frm, const std::string& filename);

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
// This sample captures 30 frames and writes the last frame to disk.
// It can be useful for debugging an embedded system with no display.
int main(int argc, char * argv[]) try
{
    // Declare depth colorizer for pretty visualization of depth data
    rs2::colorizer color_map;

    // Declare RealSense pipeline, encapsulating the actual device and sensors
    rs2::pipeline pipe;
    // Start streaming with default recommended configuration
    pipe.start();

    // Capture 30 frames to give autoexposure, etc. a chance to settle
    for (auto i = 0; i < 30; ++i) pipe.wait_for_frames();
    rs2::frameset data = pipe.wait_for_frames();
    rs2::frame depth = data.get_depth_frame();
    const int width = depth.as<rs2::video_frame>().get_width();
    const int height = depth.as<rs2::video_frame>().get_height();

    // Wait for the next set of frames from the camera. Now that autoexposure, etc.
    // has settled, we will write these to disk
    while (1)
    {
        // for (auto&& frame : pipe.wait_for_frames())
        // {
        //     // We can only save video frames as pngs, so we skip the rest
        //     if (auto vf = frame.as<rs2::video_frame>())
        //     {
        //         auto stream = frame.get_profile().stream_type();
        //         // Use the colorizer to get an rgb image for the depth stream
        //         if (vf.is<rs2::depth_frame>()) {
        //             vf = color_map.process(frame);
        //         }
        //         else{
        //             break;
        //         }

        //         // Write images to disk
        //         std::stringstream png_file;
        //         string current_time = Get_DateTime();
        //         // png_file << "rs-save-to-disk-output-" << vf.get_profile().stream_name() << ".png";
        //         png_file << "data/" << current_time << ".png";
        //         stbi_write_png(png_file.str().c_str(), vf.get_width(), vf.get_height(),
        //                     vf.get_bytes_per_pixel(), vf.get_data(), vf.get_stride_in_bytes());
        //         std::cout << "Saved " << png_file.str() << std::endl;

        //         // // Record per-frame metadata for UVC streams
        //         // std::stringstream csv_file;
        //         // csv_file << "data/meta-data-" << current_time << ".csv";
        //         // // csv_file << "rs-save-to-disk-output-" << vf.get_profile().stream_name()
        //         // //          << "-metadata.csv";
        //         // metadata_to_csv(vf, csv_file.str());
        //     }
        // }
        rs2::frameset data = pipe.wait_for_frames();
        rs2::frame depth = data.get_depth_frame();
        string current_time = Get_DateTime();
        Mat depth_img(Size(width, height), CV_16UC1, (void*)depth.get_data(), Mat::AUTO_STEP);
        imwrite(("data/"+current_time+".png").c_str(), depth_img);
    }

    return EXIT_SUCCESS;
}
catch(const rs2::error & e)
{
    std::cerr << "RealSense error calling " << e.get_failed_function() << "(" << e.get_failed_args() << "):\n    " << e.what() << std::endl;
    return EXIT_FAILURE;
}
catch(const std::exception & e)
{
    std::cerr << e.what() << std::endl;
    return EXIT_FAILURE;
}

void metadata_to_csv(const rs2::frame& frm, const std::string& filename)
{
    std::ofstream csv;

    csv.open(filename);

    //    std::cout << "Writing metadata to " << filename << endl;
    csv << "Stream," << rs2_stream_to_string(frm.get_profile().stream_type()) << "\nMetadata Attribute,Value\n";

    // Record all the available metadata attributes
    for (size_t i = 0; i < RS2_FRAME_METADATA_COUNT; i++)
    {
        if (frm.supports_frame_metadata((rs2_frame_metadata_value)i))
        {
            csv << rs2_frame_metadata_to_string((rs2_frame_metadata_value)i) << ","
                << frm.get_frame_metadata((rs2_frame_metadata_value)i) << "\n";
        }
    }

    csv.close();
}
