import os
import errno

class create_dirs():
    def __init__(self):
        self.parent_dir = os.getcwd()
        self.video_dir  = os.path.join(self.parent_dir, "video")
        self.image_dir  = os.path.join(self.parent_dir, "image")
        self.makedirs(self.video_dir)
        self.makedirs(self.image_dir)

    def makedirs(self, directory):
        try:
            os.mkdir(directory)
            print("dir created")
        except OSError as err:
            if err.errno != errno.EEXIST:
                raise
            pass

if __name__ == "__main__":
    new_dirs = create_dirs()