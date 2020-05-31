import PyCapture2
import cv2
import numpy as np 

class Pt_grey():
    def __init__(self):
        self.bus     = PyCapture2.BusManager()
        self.numCams = self.bus.getNumOfCameras()
        self.camera  = None
        self.current_frame = None
        print(self.numCams)

    def start_capture(self):
        self.camera = PyCapture2.Camera()
        cam_id      = self.bus.getCameraFromIndex(0)
        self.camera.connect(cam_id)
        self.camera.startCapture()

    def get_frame(self):
        image              = self.camera.retrieveBuffer()
        cv_image           = np.array(image.getData(), dtype="uint8").reshape((image.getRows(), image.getCols()))
        self.current_frame = cv_image

    def save_frame(self, cam_name = "RGB_", dt_string = "0"):
        cv2.imwrite("image/" + cam_name + dt_string + '.png', self.current_frame)
        print("image saved!")

def main():
    pt_grey_cam = Pt_grey()
    pt_grey_cam.start_capture()
    while True:
        pt_grey_cam.get_frame()
        cv2.waitKey(10)

if __name__ == "__main__":
    main()
