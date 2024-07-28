import cups
import cv2
from GUI import *
import time

def printImage(filename):
    conn = cups.Connection()
    printers = conn.getPrinters()
    printer = list(printers.keys())[0]
    print("Using printer '{0}'".format(printer))

    options = {
        'media': 'Custom.4x6in',
        'landscape': 'True',
        'fit-to-page': 'True',
        'scaling': '100',
        'Resolution': '300dpi'
    }

    job = conn.printFile(printer, OUTPUT_PATH + filename, "", options) # can specify print options here

    lightCount = 0

    # loop while print job is active (only allow one to be queued)
    # get the progress and print it to screen
    while True:    
        if conn.getJobs().get(job, None) is not None:
            lightsOff()

            # this would be better in a list, tracking the current light with each iteration
            if lightCount == 0:
                leftLED.on()
            if lightCount == 1:
                midLED.on()
            if lightCount == 2:
                rightLED.on()

            lightCount += 1

            if lightCount > 2:
                lightCount = 0

            jobProgress = conn.getJobAttributes(job)['job-media-progress']#
            progStr = "{0}%".format(str(jobProgress))
            print("Printing {0} (job {1}) progress: {2}".format(filename, job, progStr))

            printScreen(progStr)
            cv2.waitKey(1000)
            
        else:
            lightsOff()
            print("print job ({}) done!".format(filename))
            return
