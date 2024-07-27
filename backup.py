import os
import cv2
import datetime
import socket
import threading
#from pydrive.auth import GoogleAuth
#from pydrive.drive import GoogleDrive
from globals import *
from GUI import *

# GOOGLE DRIVE
#gauth = GoogleAuth()
#gauth.LocalWebserverAuth()
#drive = GoogleDrive(gauth)

def createExportDirectory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print("SUCCESS: Created directory '%s'" % path)            
    else:
        print("INFO: Directory '%s' already exists" % path)

def saveImage(image):
    datetimeStr = "{date:%Y-%m-%d_%H_%M_%S}".format(date=datetime.datetime.now())

    originalFilename = "photobooth_{0}_original.jpg".format(datetimeStr)

    # Save photo locally
    if cv2.imwrite(OUTPUT_PATH + originalFilename, image):
        print("SUCCESS: Saved original locally:", originalFilename)

    # Save photo to external usb drive
    saveToUSB(originalFilename, image)

    # Save photo to remote backup
    # todo check if drive object exists
    #saveOriginalThread = threading.Thread(target=backupToGoogleDrive, args=(originalFilename, OUTPUT_PATH, image))
    #saveOriginalThread.start() # Spawn new thread to save photo. Python threads kill themselves once completed
    
    if POLAROID_STYLE == True:
        polaroidFilename = "photobooth_{0}_polaroid.jpg".format(datetimeStr)
        polaroid = addPolaroidBorder(image)

        if cv2.imwrite(OUTPUT_PATH + polaroidFilename, polaroid):
            print("SUCCESS: Saved polaroid locally:", polaroidFilename)

        saveToUSB(polaroidFilename, polaroid)

        #savePolaroidThread = threading.Thread(target=backupToGoogleDrive, args=(polaroidFilename, OUTPUT_PATH, polaroid))
        #savePolaroidThread.start()
        return polaroidFilename

    # Return from here to print original print or return earlier with polaroid print if enabled
    return originalFilename


def checkUSBConnected(path):
    if not os.path.exists(path):
        print("ERROR: USB Drive not found.")
        return False
    else:
        print("SUCCESS: USB Drive connected.")
        return True

def saveToUSB(filename, image):
    if checkUSBConnected(USB_DRIVE_PATH) == True:
        cv2.imwrite(USB_DRIVE_PATH + filename, image)
        print("SUCCESS: Saved to USB Drive:", filename)
    else:
        print("ERROR: Did not save to USB Drive:", filename) 

def CheckInternetConnection(host="8.8.8.8", port=53, timeout=3):
  """
  Host: 8.8.8.8 (google-public-dns-a.google.com)
  OpenPort: 53/tcp
  Service: domain (DNS/TCP)
  """
  try:
    socket.setdefaulttimeout(timeout)
    socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
    print("SUCCESS: Connected to internet.")
    return True
  except socket.error as ex:
    print("ERROR: No internet connection:", ex)
    return False

def backupToGoogleDrive(filename, path, photo):
    if CheckInternetConnection():
        http = drive.auth.Get_Http_Object()
        
        driveFile = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": GDRIVE_FOLDER_ID}], "title": filename})

        driveFile.SetContentFile(path + filename)
        driveFile.Upload(param={"http": http})
            
        print("SUCCESS: Uploaded to GDrive:", filename)
    else:
        print("ERROR: Did not save to GDrive. No internet connection.")

    """ get IDs for files/folders
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file1 in file_list:       
        print ('title: %s, id: %s' % (file1['title'], file1['id']))
    """
