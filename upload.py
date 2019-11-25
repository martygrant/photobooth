from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)


folder_id = "1U1aCTd_K84IdQQ9_z1UUkZt7EbEk9_qT"
#file1 = drive.CreateFile({'title': 'photobooth/Hello.txt'})  # Create GoogleDriveFile instance with title 'Hello.txt'.
file1 = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": folder_id}], "title": "123.jpeg"})


file1.SetContentFile('photos/photobooth-2019-08-11_10_56_29_overlay.jpeg')
#file1.SetContentString('Hello World!') # Set content of the file from given string.
file1.Upload()

""" get IDs for files/folders
file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
for file1 in file_list:       
    print ('title: %s, id: %s' % (file1['title'], file1['id']))
"""

