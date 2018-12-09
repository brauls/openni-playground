"""IR Video Stream

Testing out the IR Video Stream using OpenNI2 and OpenCV.
See https://github.com/elmonkey/Python_OpenNI2/blob/master/samples/ex6_ird_stream.py
for the original example (customized a little bit).
"""

import numpy as np
import cv2
from primesense import openni2

from examples import IS_INITIALIZED

def show_ir_viewer():
    """Shows an ir viewer inside a new window

    Returns as soon as the stream has been terminated.
    """
    if not IS_INITIALIZED:
        print "Device not initialized"
        return

    device = openni2.Device.open_any()

    ir_stream = device.create_ir_stream()
    ir_stream.start()

    done = False
    while not done:
        key = cv2.waitKey(1) & 255
        if key == 27:
            print "ESC pressed"
            done = True

        _, ir4d = _get_ir_from_stream(ir_stream)

        cv2.imshow("ir", ir4d)

    cv2.destroyAllWindows()
    ir_stream.stop()
    openni2.unload()
    print "Terminated"

def _get_ir_from_stream(ir_stream):
    """
    Returns numpy ndarrays representing raw and ranged infra-red(IR) images.
    Outputs:
        ir    := raw IR, 1L ndarray, dtype=uint16, min=0, max=2**12-1
        ir4d  := IR for display, 3L ndarray, dtype=uint8, min=0, max=255
    """
    ir_frame = ir_stream.read_frame()
    ir_frame_data = ir_stream.read_frame().get_buffer_as_uint16()
    ir4d = np.ndarray(
        (ir_frame.height, ir_frame.width),
        dtype=np.uint16,
        buffer=ir_frame_data
    ).astype(np.float32)
    ir4d = np.uint8((ir4d/ir4d.max()) * 255)
    ir4d = cv2.cvtColor(ir4d, cv2.COLOR_GRAY2RGB)
    return ir_frame, ir4d
