import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from pyqtgraph import ImageView
from models import Camera, Indices
from save_dirs import create_dirs
from datetime import datetime
from pycap import Pt_grey

class StartWindow(QMainWindow):
    def __init__(self, cam_list):
        super().__init__()
        self.timer           = None
        self.cam_list        = cam_list
        self.frame_save_flag = 0
        self.vid_save_flg    = 0

        # make left and right camera objects
        self.camL = Camera(0, 30)
        self.camR = Camera(0, 30)

        # make a pt grey camera object to start capture
        self.pt_grey         = Pt_grey()
        self.pt_grey.start_capture()
        
        # initialize and start a timer
        self.timer_save_frames = QTimer()
        self.timer_save_frames.setInterval(5)
        self.timer_save_frames.timeout.connect(self.save_image_frame)
        self.timer_save_frames.start()
        
        # make a central widget to hold all buttons and cam videos
        self.central_widget = QWidget()

        # buttons
        self.button_Save_frame       = QPushButton('Save Frame', self.central_widget)
        self.cont_frame_button       = QPushButton('Save Continous Frames', self.central_widget)
        self.stop_cont_frame_button  = QPushButton('Stop Saving Continous Frames', self.central_widget)
        self.button_feed             = QPushButton('Start Feed', self.central_widget)
        self.button_saveVideo        = QPushButton('Save Video', self.central_widget)
        self.button_stopVideo        = QPushButton('Stop Saving Video', self.central_widget)

        # make drop down menus for left and right cameras
        self.drop_down_L             = self.make_drop_down()
        self.drop_down_L.currentIndexChanged.connect(self.connect_cam_drop_L)
        self.drop_down_R             = self.make_drop_down()
        self.drop_down_R.currentIndexChanged.connect(self.connect_cam_drop_R)

        # make image view objects to show the cam feed
        self.image_view  = ImageView()
        self.image_viewL = ImageView()
        self.image_viewR = ImageView()

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 10)

        # make vertical layout
        self.layout = QVBoxLayout(self.central_widget)

        # make horizontal layout for buttons
        self.frame_hor_layout = QHBoxLayout()
        self.video_hor_layout = QHBoxLayout()

        # add buttons to the video hor layout
        self.frame_hor_layout.addWidget(self.button_Save_frame)
        self.frame_hor_layout.addWidget(self.cont_frame_button)
        self.frame_hor_layout.addWidget(self.stop_cont_frame_button)

        # add buttons to video hor layout
        self.video_hor_layout.addWidget(self.button_saveVideo)
        self.video_hor_layout.addWidget(self.button_stopVideo)

        # top layout, top buttons and RGB video feed
        self.layout.addWidget(self.button_feed)
        self.layout.addLayout(self.frame_hor_layout)
        self.layout.addLayout(self.video_hor_layout)
        self.layout.addWidget(self.image_view)

        # make a horizontal layout
        self.stereo_Layout = QHBoxLayout()

        # add the drop down button to the cam feed
        self.mini_cam_layout1 = QVBoxLayout()
        self.mini_cam_layout2 = QVBoxLayout()

        self.mini_cam_layout1.addWidget(self.drop_down_L)
        self.mini_cam_layout1.addWidget(self.image_viewL)

        self.mini_cam_layout2.addWidget(self.drop_down_R)
        self.mini_cam_layout2.addWidget(self.image_viewR)

        # add CamL and CamR feed to the layout
        self.stereo_Layout.addLayout(self.mini_cam_layout1)
        self.stereo_Layout.addLayout(self.mini_cam_layout2)

        # add the layout to the vertical layout
        self.layout.addLayout(self.stereo_Layout)

        self.layout.addWidget(self.slider)
        self.setCentralWidget(self.central_widget)

        # save frames
        self.button_Save_frame.clicked.connect(self.update_image)
        
        # start the video feed
        self.button_feed.clicked.connect(self.start_vid_feed)
        self.button_saveVideo.clicked.connect(self.Save_Video)
        self.slider.valueChanged.connect(self.update_brightness)

        self.button_stopVideo.clicked.connect(self.stop_save)

        self.cont_frame_button.clicked.connect(self.set_cont_flag)
        self.stop_cont_frame_button.clicked.connect(self.clear_cont_flag)
    
    def set_cont_flag(self):
        self.frame_save_flag = 1
    
    def clear_cont_flag(self):
        self.frame_save_flag = 0

    def stop_save(self):
        self.camL.close_vid()
        self.camR.close_vid()

    def update_brightness(self, value):
        self.camL.set_brightness(value)
        self.camR.set_brightness(value)

    def Save_Video(self):
        self.camL.init_video("Cam_L_")
        self.camR.init_video("Cam_R_")
        self.vid_save_flg = 1

    def start_vid_feed(self):
        self.timer = QTimer()
        self.timer.setInterval(35)
        self.timer.timeout.connect(self.update_movie)
        self.timer.start()

    def update_movie(self):
        self.camL.get_frame()
        self.image_viewL.setImage(self.camL.current_frame.T)
        if self.vid_save_flg == 1:
            self.camL.save_video()
        
        self.camR.get_frame()
        self.image_viewR.setImage(self.camR.current_frame.T)
        if self.vid_save_flg == 1:
            self.camR.save_video()
        
        self.pt_grey.get_frame()
        self.image_view.setImage(self.pt_grey.current_frame.T)

    def update_image(self):
        time_stamp = datetime.now()
        dt_string  = time_stamp.strftime("%d_%m_%Y_%H_%M_%S.%f")
        self.pt_grey.save_frame("RGB_", dt_string)
        self.camL.save_frame("Cam_L_", dt_string)
        self.camR.save_frame("Cam_R_", dt_string)

    def connect_cam_drop_L(self, string):
        self.camL.Camera_id = self.cam_list[int(string)]
        self.camL.init_camera()
    
    def connect_cam_drop_R(self, string):
        self.camR.Camera_id = self.cam_list[int(string)]
        self.camR.init_camera()

    def make_drop_down(self):
        new_drop_down = QComboBox(self)
        if self.is_iterable() == False:
            new_drop_down.addItem("Cam_0")
            return new_drop_down
        else:
            for index in self.cam_list:
                cam_item = "Cam_" + str(index)
                new_drop_down.addItem(cam_item)
            return new_drop_down
    
    def is_iterable(self):
        try:
            iter(self.cam_list)
        except Exception:
            return False
        else:
            return True

    # save the fames continuously
    def save_image_frame(self):
        if self.frame_save_flag == 1:
            time_stamp = datetime.now()
            dt_string  = time_stamp.strftime("%d_%m_%Y_%H_%M_%S.%f")
            self.camL.save_frame("Cam_L_", dt_string)
            self.camR.save_frame("Cam_R_", dt_string)
            self.pt_grey.save_frame("RGB_", dt_string)

if __name__ == "__main__":
    app     = QApplication([])
    create_dirs()
    cam_idx = Indices()
    window  = StartWindow(cam_idx.indices)
    window.show()
    app.exit(app.exec_())