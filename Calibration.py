"""

Calibration module helps people to put the tablet to an appropriate place.
The edge of tablet should align with red guideline.

"""

import Image
import ImageTk
import vision_definitions
import Tkinter as tk
from naoqi import ALProxy

class Calibration():

    def __init__(self, root):
        # Diameter of landmark in meter
        self.landmarkTheoreticalSize = 0.06  # in meter
        """
        Camera parameter
        """
        self.camName = "bottomCam"
        self.camID = 1.0    # buttomCam
        self.resolution = vision_definitions.kVGA   # kVGA(640*480)
        self.colorSpace = vision_definitions.kRGBColorSpace # RGB
        self.fps = 5
        self.currentCamera = "CameraBottom"

        """
        Tkinter parameter
        """
        # self.window = tk.Tk()
        self.window = root
        self.window.title("Calibration")
        self.window.geometry("640x480") # Same size as camera
        self.window.bind("<Return>", exit_mainloop) # Press Enter to exit
        self.canvas = tk.Canvas(self.window, highlightthickness = 0, relief = 'ridge',
                   borderwidth = 0, width = 640, height = 480)
        self.canvas.pack(fill = 'both', expand =1) # fit the window size
        self.label = tk.Label(self.window, bg = 'yellow', text = 'Press Enter to exit',
                              width = 30, height = 2)

        self.label.pack()
        self.label.place(anchor = 'nw') # put the label in upper left corner

        """
        NAO robot parameter
        """
        self.memoryProxy = ALProxy("ALMemory")
        self.landmarkProxy = ALProxy("ALLandMarkDetection")
        self.motionProxy = ALProxy("ALMotion")
        self.awareness = ALProxy("ALBasicAwareness")
        self.tts = ALProxy("ALTextToSpeech")
        self.camProxy = ALProxy("ALVideoDevice")

    def startCalibrationWindow(self):

        image = grabImage(self.camProxy, self.camName, self.camID,
                          self.resolution, self.colorSpace, self.fps)
        # Change the format of image that Tkinter can use
        photo = ImageTk.PhotoImage(image)
        # Use this photo in canvas
        self.canvas.create_image(0, 0, anchor='nw', image=photo)

        # draw a vertical guideline
        self.canvas.create_line(320, 0, 320, 480, fill='red')

        self.window.update_idletasks()
        self.window.after(0, self.startCalibrationWindow)

def exit_mainloop(event):
    """
    Eixt the main loop of Tkinter
    """
    event.widget.quit()
    event.widget.destroy()

def grabImage(camProxy, name, camID, resolution, colorSpace, fps):
    """
        camID = 0: top camera; camID = 1: bottom camera
    """

    videoClient = camProxy.subscribeCamera(name,camID,resolution,colorSpace,fps)
    naoImage = camProxy.getImageRemote(videoClient)

    camProxy.unsubscribe(videoClient)

    # Work with the image returned and save it
    # Get the image size and pixel array
    imageWidth = naoImage[0]
    imageHeight = naoImage[1]
    pixelArray = naoImage[6]

    # Create a PIL Image from our pixel array
    im = Image.fromstring("RGB", (imageWidth,imageHeight), pixelArray)
    return im



