"""RGB Video Stream

Testing out the RGB Video Stream using OpenNI2 and OpenCV.
See https://github.com/elmonkey/Python_OpenNI2/blob/master/samples/ex2_rgb_stream.py
for the original example.
"""

import numpy as np
import cv2
from primesense import openni2
from primesense import _openni2 as c_api

from examples import IS_INITIALIZED

def show_rgb_viewer():
    """Shows an rgb viewer inside a new window

    Returns as soon as the stream has been terminated.
    """
    if not IS_INITIALIZED:
        print "Device not initialized"
        return

    device = openni2.Device.open_any()

    rgb_stream = _rgb_stream_from_device(device)
    rgb_stream.start()

    done = False
    while not done:
        key = cv2.waitKey(1) & 255
        if key == 27:
            print "ESC pressed"
            done = True

        bgr = np.fromstring(
            rgb_stream.read_frame().get_buffer_as_uint8(),
            dtype=np.uint8
        ).reshape(240, 320, 3)
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

        cv2.imshow("rgb", rgb)

    cv2.destroyAllWindows()
    rgb_stream.stop()
    openni2.unload()
    print "Terminated"

def _rgb_stream_from_device(device):
    rgb_stream = device.create_color_stream()
    print("The rgb video mode is", rgb_stream.get_video_mode())
    rgb_stream.set_video_mode(c_api.OniVideoMode(
        pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888,
        resolutionX=320,
        resolutionY=240,
        fps=30
    ))
    return rgb_stream