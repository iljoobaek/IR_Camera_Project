# IR_Camera_Project

Requirements: (install all modules using pip3 or python3 setup.py install)
1. Python 3.5+
2. PyQt5 module
3. opencv-python-headless (Normal opencv installation interferes with PtQt module)
4. opencv-contrib-python-headless (For extra opencv module)
5. pyqtgraph
6. flycapture module, Download from: https://www.flir.com/products/flycapture-sdk/ for your version of ubuntu.
Other required modules: time, datetime, os, errno etc.

Usage: run vid_gui using sudo python3 vid_gui.py, sudo is required to get feed from the pt grey camera.
This is a crude version and won't work if the point grey camera is not connected.
