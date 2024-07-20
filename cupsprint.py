import cups
import cv2
from GUI import *


def printImage(filename):
    conn = cups.Connection()
    printers = conn.getPrinters()
    printer = list(printers.keys())[1]
    print("Using printer '{0}'".format(printer))

    job = conn.printFile(printer, filename, "", {}) # can specify print options here

    # loop while print job is active (only allow one to be queued)
    # get the progress and print it to screen
    while True:    
        if conn.getJobs().get(job, None) is not None:
            jobProgress = conn.getJobAttributes(job)['job-media-progress']

            progStr = "{0}%".format(str(jobProgress))
            print("Printing {0} (job {1}) progress: {2}".format(filename, job, progStr))

            screen = printScreen(progStr)
            renderFrame(screen)
            cv2.waitKey(1000)
            
        else:
            print("print done!")
            return
