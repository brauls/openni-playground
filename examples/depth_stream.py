"""Depth Video Stream

Testing out the Depth Video Stream using OpenNI2 and OpenCV.
See https://github.com/elmonkey/Python_OpenNI2/blob/master/samples/ex1_depth_stream.py
for the original example (customized a little bit).
"""

import numpy as np
import cv2
from primesense import openni2
from primesense import _openni2 as c_api

from examples import IS_INITIALIZED

def show_depth_viewer():
    """Shows a depth viewer inside a new window

    Returns as soon as the stream has been terminated.
    """
    if not IS_INITIALIZED:
        print "Device not initialized"
        return

    device = openni2.Device.open_any()

    depth_stream = _depth_stream_from_device(device)
    depth_stream.start()

    done = False
    while not done:
        key = cv2.waitKey(1) & 255
        if key == 27:
            print "ESC pressed"
            done = True

        _, d4d = _get_depth_from_stream(depth_stream)
        cv2.imshow("depth", d4d)

    cv2.destroyAllWindows()
    depth_stream.stop()
    openni2.unload()
    print "Terminated"

def _depth_stream_from_device(device):
    depth_stream = device.create_depth_stream()
    print("The depth video mode is", depth_stream.get_video_mode())
    depth_stream.set_video_mode(c_api.OniVideoMode(
        pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM,
        resolutionX=320,
        resolutionY=240,
        fps=30
    ))
    depth_stream.set_mirroring_enabled(False)
    return depth_stream

def _get_depth_from_stream(depth_stream):
    """
    Returns numpy ndarrays representing the raw and ranged depth images.
    Outputs:
        dmap:= distancemap in mm, 1L ndarray, dtype=uint16, min=0, max=2**12-1
        d4d := depth for display, 3L ndarray, dtype=uint8, min=0, max=255
    Note1:
        fromstring is faster than asarray or frombuffer
    Note2:
        .reshape(120,160) #smaller image for faster response
                OMAP/ARM default video configuration
        .reshape(240,320) # Used to MATCH RGB Image (OMAP/ARM)
                Requires .set_video_mode
    """
    dmap = np.fromstring(
        depth_stream.read_frame().get_buffer_as_uint16(),
        dtype=np.uint16
    ).reshape(240, 320)  # Works & It's FAST
    d4d = np.uint8(dmap.astype(float) *255/ 2**12-1) # Correct the range. Depth images are 12bits
    d4d = cv2.cvtColor(d4d, cv2.COLOR_GRAY2RGB)
    # Shown unknowns in black
    d4d = 255 - d4d
    return dmap, d4d
