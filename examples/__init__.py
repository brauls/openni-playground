"""Usage examples of the Python_OpenNI2 wrapper

The examples are taken from https://github.com/elmonkey/Python_OpenNI2/tree/master/samples.
"""

from primesense import openni2
from primesense.utils import InitializationError

IS_INITIALIZED = False

try:
    openni2.initialize("/usr/local/src/OpenNI-Linux-Arm-2.3/Redist")
    if openni2.is_initialized():
        IS_INITIALIZED = True
        print "OpenNI2 is initialized"
    else:
        print "OpenNI2 is not initialized"
except InitializationError as err:
    print("OpenNI2 is not initialized", err)
