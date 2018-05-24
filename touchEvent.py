"""

touchEvent mode control the NAO's head sensor touch.

"""

from naoqi import ALProxy
from naoqi import ALModule

class ReactToTouchModule(ALModule):
    """
    A simple module able to react to touch events
    """

    def __init__(self, name):

        ALModule.__init__(self, name)
        # No need for IP and port here because we have
        # our Python broker connected to NAOqi broker
        self.fort_touched = False
        self.middle_touched = False
        self.rear_touched = False
        self.name = name
        self.touch_list = []
        self.sub_event = []

        # Create a proxy to ALTextToSpeech for later use
        self.tts = ALProxy("ALTextToSpeech")
        # Create a proxy to ALMotion for later use
        self.motion = ALProxy("ALMotion")


    def subscribe(self, *args):
        # Subscribe to TouchChanged event
        global memory
        memory = ALProxy("ALMemory")

        if "FrontTactileTouch" in args:
            memory.subscribeToEvent("FrontTactilTouched", self.name, "Front_Event")
            self.sub_event.append("FrontTactilTouched")

        if "MiddleTactileTouch" in args:
            memory.subscribeToEvent("MiddleTactilTouched", self.name, "Middle_Event")
            self.sub_event.append("MiddleTactilTouched")

        if "RearTactileTouch" in args:
            memory.subscribeToEvent("RearTactilTouched", self.name, "Rear_Event")
            self.sub_event.append("RearTactilTouched")

    def Front_Event(self, name, value):

        self.unsubscribe()
        self.tts.say(name)
        print "Touched: ", name
        if (value == 1.0):
            self.fort_touched = True
            if len(self.touch_list) == 0:
                self.touch_list.append("FrontTactile")

    def Middle_Event(self, name, value):

        self.unsubscribe()
        self.tts.say(name)
        print "Touched: ", name
        if (value == 1.0):
            self.middle_touched = True
            if len(self.touch_list) == 0:
                self.touch_list.append("MiddleTactile")

    def Rear_Event(self, name, value):

        self.unsubscribe()
        self.tts.say(name)
        print "Touched: ", name
        if (value == 1.0):
            self.rear_touched = True
            if len(self.touch_list) == 0:
                self.touch_list.append("RearTactile")

    def unsubscribe(self):

        if "FrontTactilTouched" in self.sub_event:
            memory.unsubscribeToEvent("FrontTactilTouched", self.name)
        if "MiddleTactilTouched" in self.sub_event:
            memory.unsubscribeToEvent("MiddleTactilTouched", self.name)
        if "RearTactilTouched" in self.sub_event:
            memory.unsubscribeToEvent("RearTactilTouched", self.name)

        self.sub_event = []

