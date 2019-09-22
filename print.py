import cups
import cv2
import time

conn = cups.Connection()

printers = conn.getPrinters()

canonPrinter = list(printers.keys())[0] # 0 for canon, 1 for pdf
print(canonPrinter)

"""
#job = conn.printFile(canonPrinter, "arrow.png", "", {'fit-to-page':'True'})
job = conn.printTestPage(canonPrinter)


print(conn.getJobs())
t = list(conn.getJobs().keys())[0]
print(conn.getJobAttributes(t))
time.sleep(2)
print(conn.getJobAttributes(t)['job-state-reasons'])


while True:
    if conn.getJobs().get(t, None) is not None:
        jobProgress = conn.getJobAttributes(t)['job-media-progress']
        print(jobProgress)
        time.sleep(2)
    else:
        # should wait for 5 secs or so
        print("done!")
"""
#file = "//home/pi/Desktop/photobooth/photos/photobooth-2019-09-19_23_16_00_original.jpeg"
#file = "glasgow.jpeg"

img = cv2.imread("//home/pi/Desktop/photobooth/photos/photobooth-2019-09-22_10_26_19_original.jpeg")

img = cv2.resize(img, None, fx=0.12, fy=0.12)

cv2.imwrite("scaled.jpg", img)

conn.printFile(canonPrinter, "scaled.jpg", "", {'print-media':'A6'})

