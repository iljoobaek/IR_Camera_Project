from datetime import datetime
import time
import sys
import cv2

class Camera:
    def __init__(self, camera_number, fps):
        self.Camera_id     = camera_number
        self.fps           = int(fps)
        self.cap_thermal   = None
        self.current_frame = None
        self.frame_width   = None
        self.frame_height  = None
        self.video_out     = None
        self.current_stat  = None

    def init_camera(self):
        self.cap_thermal = cv2.VideoCapture(self.Camera_id)
        if self.cap_thermal.isOpened():
            self.frame_width  = int(self.cap_thermal.get(3))
            self.frame_height = int(self.cap_thermal.get(4))

    def get_frame(self):
        self.current_stat, self.current_frame = self.cap_thermal.read()

    def close_cam(self):
        self.cap_thermal.release()
    
    def close_vid(self):
        self.video_out.release()

    def save_frame(self, cam_name = "RGB_", dt_string = "0"):
        cv2.imwrite("image/"+cam_name+dt_string+'.png',self.current_frame)
        print("Image Saved!")

    def set_brightness(self, value):
        self.cap_thermal.set(cv2.CAP_PROP_BRIGHTNESS, value)
        
    def init_video(self, cam_name = "RGB_"):
        dt_string       = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        video_name      = "video/" + cam_name + dt_string + ".avi"
        self.video_out  = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), self.fps, (self.frame_width, self.frame_height))
    
    def save_video(self):
        self.video_out.write(self.current_frame)


class Indices:
    def __init__(self):
        self.indices = self.store_indices()
    
    def store_indices(self):
        cam_ids = []
        for i in range(0, 10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                cam_ids.append(i)
                cap.release()
        return cam_ids
