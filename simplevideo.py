#!/usr/bin/env python

#------------------------------------------------------------------------------
#                 PyuEye example - main modul
#
# Copyright (c) 2017 by IDS Imaging Development Systems GmbH.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#------------------------------------------------------------------------------

from pyueye_example_camera import Camera
from pyueye_example_utils import FrameThread
from pyueye_example_gui import PyuEyeQtApp, PyuEyeQtView
from PyQt4 import QtGui
import time


from pyueye import ueye

import cv2
import numpy as np

def process_image(self, image_data):
    ##tic = time.time()
    image = image_data.as_1d_image()#*2
    ##print time.time()-tic
    return QtGui.QImage(image.data,
                        image_data.mem_info.width,
                        image_data.mem_info.height,
                        QtGui.QImage.Format_RGB888)

def main():

    # we need a QApplication, that runs our QT Gui Framework    
    print 'a'
    app = PyuEyeQtApp()
    print 'b'
    # a basic qt window
    view = PyuEyeQtView()
    print 'c'
    view.show()
    print 'd'
    view.user_callback = process_image
    print 'e'
    # camera class to simplify uEye API access
    cam = Camera()
    print 'f'
    cam.init()
    cam.set_colormode(ueye.IS_CM_BGR8_PACKED)
    #cam.set_colormode(ueye.IS_CM_SENSOR_RAW8)
    #cam.set_aoi(0,0, 1280, 1024)
    cam.set_aoi(300,300, 400, 400)
    #cam.set_aoi(500,500,900,900)
    print 'g'
    cam.alloc()
    print 'h'
    cam.capture_video()
    print 'i'
    # a thread that waits for new images and processes all connected views
    print 'j'
    thread = FrameThread(cam, view)
    print 'k'
    thread.start()

    print 'l'
    
    # cleanup
    app.exit_connect(thread.stop)
    print '1'
    app.exec_()
    print '2'
    thread.stop()
    print '3'
    thread.join()
    print '4'
    cam.stop_video()
    print '5'
    cam.exit()
    print '6'
if __name__ == "__main__":
    main()

