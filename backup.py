import os
import cv2
import datetime
import socket
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from globals import *

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

def savePhoto(image):
    # Save photo locally
    filename = 'photobooth-{date:%Y-%m-%d_%H_%M_%S}.jpeg'.format(date=datetime.datetime.now())
    cv2.imwrite(OUTPUT_PATH + filename, image)
    print("SUCCESS: Saved locally:", filename)

    # Save photo to external usb drive
    saveToUSB(filename, image)
    
    """
    # Save photo to remote backup
    # todo check if drive object exists
    uploadThreadOne = threading.Thread(target=backupToGoogleDrive, args=(filename, OUTPUT_PATH, image))
    uploadThreadOne.start()
    
    # TODO PROBABLY DON'T NEED TO WAIT, TAKES ~2SECS, RESEARCH THIS
    uploadThreadOne.join()
    """

    

def checkUSBConnected():
    if not os.path.exists("/media/pi/2A47-4A89/photobooth/"):
        print("ERROR: USB Drive not found.")
        return False
    else:
        print("SUCCESS: USB Drive connected.")
        return True

def saveToUSB(filename, image):
    path = "/media/pi/2A47-4A89/photobooth/"
    if checkUSBConnected() == True:
        cv2.imwrite(path + filename, image)
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
        
        folder_id = "1U1aCTd_K84IdQQ9_z1UUkZt7EbEk9_qT"
        #file1 = drive.CreateFile({'title': 'photobooth/Hello.txt'})  # Create GoogleDriveFile instance with title 'Hello.txt'.
        driveFile = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": folder_id}], "title": filename})

        driveFile.SetContentFile(path + filename)
        #file1.SetContentString('Hello World!') # Set content of the file from given string.
        driveFile.Upload(param={"http": http})
            
        print("SUCCESS: Uploaded to GDrive:", filename)
    else:
        print("ERROR: Did not save to GDrive. No internet connection.")

    """ get IDs for files/folders
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file1 in file_list:       
        print ('title: %s, id: %s' % (file1['title'], file1['id']))
    """
