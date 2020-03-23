# photobooth

This repo is for a Raspberry Pi powered photobooth for parties and events. The code here can be run on a Raspberry Pi connected to a camera, some buttons and a printer to build a fun photobooth that lets people capture and print photos without any assistance.

# todo
* add section for setting up google drive, notification service, CUPS
* add hardware setup section with wiring etc.

## Requirements
### Software
* python3 (tested on 3.4.2)
* CUPS (1.7.5+)
* pycups (1.9.74) 
* picamera (1.10)
* OpenCV (3.4.3)
* PiDrive (1.3.1)
* numpy (1.8.2)
* gpiozero (1.4.0)

### Hardware
* Raspberry Pi (I'm using 3b running Jessie (4.9.35-v7+)
* Raspberry Pi Camera v2 (or similar)
* Your own selections of a monitor, buttons, lights, printer etc. 

## Useful tutorials and links used for building this project
* https://www.hackster.io/sabat54i/wedding-photo-booth-with-raspberry-pi-1cea3a
* https://www.hackster.io/ericBcreator/photo-booth-powered-by-a-raspberry-pi-23b491
* https://www.instructables.com/id/Raspberry-Pi-photo-booth-controller/
* https://gpiozero.readthedocs.io/en/stable/recipes.html#button
* https://dordnung.de/raspberrypi-ledstrip/

## Image resolution and printing
The Raspberry Pi camera is capable of a number of different resolutions. Your will probably want to setup your photobooth to print 6x4 photos so you should choose a resolution with the same aspect ratio (3:2). A smaller resolution is used during the countdown preview so it can maintain a high frame rate.

## Potential problems
* Depending on the resolution of images you capture you may need to [increase your Pi's GPU memory](https://www.raspberrypi.org/forums/viewtopic.php?t=190182). 
* You may want to [disable the screensaver on your Pi](https://www.raspberrypi.org/documentation/configuration/screensaver.md) so the photobooth can always be used during operation.

## original components
| Item        | Cost           |
| ------------- |:-------------:|
| Raspberry Pi | Already had |
| Monitor | Already had |
| Printer | Already had |
| Power extension cable | Already had |
| Mouse | Already had |
| Keyboard | Already had |
| Pi Camera | £23 |
| Arcade Buttons | £22.34 |
| Transistors for Button LEDs | £9.90 |
| Power supply for Button LEDs | £11.99 |
| Ribbon cable | £5.99 |
| Crimping tool | £9.99 |
| Cable ends dupont style | £7.99 |
| Cable ends spade style | £7.50 |
| CNC Wood | £73.30 |
| B&Q back panel, paint, hardware (brackets, screws, command strips, wire, tape etc) | £49.35 |
| External light | £24.99 |
| Light power supply | £10.99 |
| Photo paper | £7.29 |
| SD card | £9.99 |
| eBay Printer (didn't use) | £19.48 |
| Pi case with fan | £8.99 |
| HDMI/VGA adaptor | £5.85 |
| Total | £308.93 |
