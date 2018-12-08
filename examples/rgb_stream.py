"""RGB Video Stream

Testing out the RGB Video Stream using OpenNI2 and OpenCV.
See https://github.com/elmonkey/Python_OpenNI2/blob/master/samples/ex2_rgb_stream.py
for the original example.
"""

import numpy as np
import cv2
from primesense import openni2
from primesense import _openni2 as c_api

openni2.initialize("/usr/local/src/OpenNI-Linux-Arm-2.3/Redist")
if openni2.is_initialized():
    print "OpenNI2 is initialized"
else:
    print "OpenNI2 is not initialized"

DEVICE = openni2.Device.open_any()

RGB_STREAM = DEVICE.create_color_stream()
print("The rgb video mode is", RGB_STREAM.get_video_mode())
RGB_STREAM.set_video_mode(c_api.OniVideoMode(
    pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888,
    resolutionX=320,
    resolutionY=240,
    fps=30
))

RGB_STREAM.start()

DONE = False
while not DONE:
    KEY = cv2.waitKey(1) & 255
    if KEY == 27:
        print "ESC pressed"
        DONE = True

    BGR = np.fromstring(
        RGB_STREAM.read_frame().get_buffer_as_uint8(),
        dtype=np.uint8
    ).reshape(240, 320, 3)
    RGB = cv2.cvtColor(BGR, cv2.COLOR_BGR2RGB)

    cv2.imshow("rgb", RGB)

cv2.destroyAllWindows()
RGB_STREAM.stop()
openni2.unload()
print "Terminated"
