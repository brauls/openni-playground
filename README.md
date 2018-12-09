# openni-playground

This is a playground project to try out some features of the [OpenNI2](https://github.com/occipital/OpenNI2/tree/develop) project along with the [primesense python wrapper](https://github.com/elmonkey/Python_OpenNI2) on a Raspberry Pi 3 Model B+. As a sensor I am using the ASUS Xtion PRO LIVE.

## Used hardware

* Raspberry Pi 3 Model B+
* ASUS Xtion PRO LIVE RGB and depth sensor

## Using OpenNI2 on Raspberry Pi

As a first step I wanted the Raspberry Pi (with Raspbian installed), OpenNI2 and the ASUS sensor to be working together successfully. To test that I used the sample program SimpleRead which comes with the [OpenNI2](https://github.com/occipital/OpenNI2/tree/develop) project (inside the `Samples` subfolder). To be able to execute it I had to build and install the OpenNI2 SDK on my Raspberry Pi.

### Building OpenNI2 from source on the Raspberry Pi

First I cloned the [OpenNI2](https://github.com/occipital/OpenNI2.git) project's develop branch onto my Raspberry Pi.

```
git clone --single-branch -b develop https://github.com/occipital/OpenNI2.git
```

Then I installed the dependencies listed in the prerequisites section of the [OpenNI2 README](https://github.com/occipital/OpenNI2/tree/develop).

Next I had to make some adjustments to be able to compile and afterwards install OpenNI2 successfully. The sources that helped me to figure it out are listed below.

#### Helpful resources

* [OpenNI2 README](https://github.com/occipital/OpenNI2/tree/develop) itself, especially the build prerequisites when building for Linux and the packaging part.
* [Getting Raspberry Pi, OpenNI2, and Asus Xtion Pro Live To Work Together](https://ariandy1.wordpress.com/2013/02/27/getting-raspberry-pi-openni-and-asus-xtion-pro-live-to-work/)
* [Depth Imaging with the Asus Xtion Pro Live Sensor and the KIPR Link (Part 1)](http://files.kipr.org/gcer/2013/proceedings/Rand_Depth_Imaging_1.pdf)
* [OpenNI2.2 ARM Binaries on Raspberry Pi](https://forums.structure.io/t/openni2-2-arm-binaries-on-raspberry-pi/874/2)
* [Problem when run 'ReleaseVersion.py': subprocess.CalledProcessError](https://github.com/occipital/OpenNI2/issues/135)
* [Issue running ReleaseVersion.py](https://github.com/occipital/OpenNI2/issues/86)
* [GCC 7.2 Array subscript is below array bounds](https://www.bountysource.com/issues/58645535-gcc-7-2-array-subscript-is-below-array-bounds)

#### Changes I made to the sources

* in file `/OpenNI2/ThirdParty/PSCommon/BuildSystem/Platform.Arm`
  * I commented out line 4 `CFLAGS += -march=armv7-a -mtune=cortex-a9 -mfpu=neon -mfloat-abi=softfp #-mcpu=cortex-a8` and instead added `CFLAGS += -mtune=arm1176jzf-s -mfpu=vfp -mfloat-abi=hard`
  * commented out line 12 `DEFINES += XN_NEON`
* in file `/OpenNI2/Packaging/ReleaseVersion.py`
  * in lines 198 and 202 I changed the make calls by replacing the part where it says `'-j' + calc_jobs_number()` by just `-j1`
  * furthermore I passed another parameter `ALLOW_WARNINGS=1` to the make calls

After those changes in the sources I was able to compile by navigating inside the folder `/OpenNI2/Packaging` and then performing the command `sudo python2 ReleaseVersion.py Arm`.

The results of the build can be found inside the folder `OpenNI2/Packaging/Final`.

### Installing and testing

I extracted the installer archive inside the folder `/usr/local/src`. By navigating inside the extracted folder and calling `sudo chmod +x install.sh` and `sudo ./install.sh` I was able to install the OpenNI2 SDK.

Next I tried out the example program `SimpleRead` by navigating inside the folder `Samples/Bin` and then calling `sudo ./SimpleRead`. The result was a continuous stream of sensor data similar to one of the [resources](https://ariandy1.wordpress.com/2013/02/27/getting-raspberry-pi-openni-and-asus-xtion-pro-live-to-work/) I used.

### A little demo app using OpenCV

Next I tested some sample projects using the [primesense python wrapper](https://github.com/elmonkey/Python_OpenNI2) and OpenCV to get some visual results. The original examples can be found [here](https://github.com/elmonkey/Python_OpenNI2/blob/master/samples) and are only customized a little bit.
To be able to run the examples I followed [this](https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/) guide to install OpenCV on my Raspberry Pi, first. Inside the virtual environment `cv` (created during the guide) I also installed the `primesense` package using the command `pip install primesense`.
