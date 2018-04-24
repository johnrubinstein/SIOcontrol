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

    # reshape the image data as 1dimensional array
    ##tic = time.time()
    image = image_data.as_1d_image()#*2
    ##print time.time()-tic
    # make a gray image
    ##image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #image = cv2.medianBlur(image,5)
    # find circles in the image # does not seem necessary
    ###circles = cv2.HoughCircles(image, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 100)
    # make a color image again to mark the circles in green
    ##image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    
    #if circles is not None:
#	   # convert the (x, y) coordinates and radius of the circles to integers
#	   circles = np.round(circles[0, :]).astype("int") 
#	   # loop over the (x, y) coordinates and radius of the circles
#	   for (x, y, r) in circles:
#		  # draw the circle in the output image, then draw a rectangle
#		  # corresponding to the center of the circle
#		  cv2.circle(image, (x, y), r, (0, 255, 0), 6)
    
    # show the image with Qt
    return QtGui.QImage(image.data,
                        image_data.mem_info.width,
                        image_data.mem_info.height,
                        QtGui.QImage.Format_RGB888)

def main():

    # we need a QApplication, that runs our QT Gui Framework    
    app = PyuEyeQtApp()

    # a basic qt window
    view = PyuEyeQtView()
    view.show()
    view.user_callback = process_image

    # camera class to simplify uEye API access
    cam = Camera()
    cam.init()
    #cam.set_fps(4)
    cam.set_colormode(ueye.IS_CM_BGR8_PACKED)
    #cam.set_colormode(ueye.IS_CM_SENSOR_RAW8)
    #cam.set_aoi(0,0, 1280, 1024)
    cam.set_aoi(300,300, 400, 400)
    #cam.set_aoi(500,500,900,900)
    cam.alloc()
    cam.capture_video()

    # a thread that waits for new images and processes all connected views
    thread = FrameThread(cam, view)
    thread.start()

    # cleanup
    app.exit_connect(thread.stop)
    app.exec_()

    thread.stop()
    thread.join()

    cam.stop_video()
    cam.exit()

if __name__ == "__main__":
    main()

