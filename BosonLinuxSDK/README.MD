------------
Description:
------------

This is a code example demonstrating FLIR Boson camera command and control using Boson SDK commands.
It's written for interface with a Linux system and performs the following commands in sequential order:

* Connects to the camera
* Reads and displays the Camera Serial Number
* Reads and changes the bit depth of the output
* Reads and displays the current Software Revision of the Camera
* Reads and displays the Sensor Part Number
* Reads data from the Camera Flash
* Gets the current Frame Count
* Changes the FFCMode to Manual, then back again
* Performs a manual FFC

----------
To compile
----------
First, compile by running
```
./build.sh
```

--------------
To run:
--------------
Run example_linux in the examples directory after compiling.

Obtain processor temperature
```
./examples/boson_cpu_temp
```

Obtain sensor temperature
```
./examples/boson_fpa_temp
```

Run multiple examples
```
./example_linux
```

--------------
Build Notes
--------------
This was built on tested with Boson SDK rev 2.0.5. 2.0.5 is included, but the latest SDK can be found at
https://www.flir.com/support/products/boson#Resources
