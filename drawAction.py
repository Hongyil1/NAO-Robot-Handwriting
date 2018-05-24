"""

drawAction module contains almost all actions the NAO need in this project.

"""

import almath
import time
import motion
import Painter
import AngleCalculate
from naoqi import ALProxy


class drawAction():
    def __init__(self):
        """
        NAO robot parameter
        """
        self.memoryProxy = ALProxy("ALMemory")
        self.landmarkProxy = ALProxy("ALLandMarkDetection")
        self.motionProxy = ALProxy("ALMotion")
        self.awareness = ALProxy("ALBasicAwareness")
        self.tts = ALProxy("ALTextToSpeech")

        self.cal = AngleCalculate.AngleCalculate()

    # Let human write on the tablet
    def humanWrite(self):

        self.tts.say("Human write start")

        # Stop awareness
        self.awareness.stopAwareness()

        self.tts.say("Start the painter")
        painter = Painter.Painter()
        painter.humanWrite()

    # Move right arm above the tablet
    def prepare_Pen(self):

        # Stiffness
        self.motionProxy.stiffnessInterpolation("RHipRoll", 1.0, 0.2)
        self.motionProxy.stiffnessInterpolation("LHipRoll", 1.0, 0.2)
        self.motionProxy.stiffnessInterpolation("RHipPitch", 1.0, 0.2)
        self.motionProxy.stiffnessInterpolation("LHipPitch", 1.0, 0.2)
        self.motionProxy.stiffnessInterpolation("RHipYawPitch", 1.0, 0.2)
        self.motionProxy.stiffnessInterpolation("LHipYawPitch", 1.0, 0.2)
        self.motionProxy.stiffnessInterpolation("RArm", 1.0, 0.2)

        # Move Right hand
        self.motionProxy.angleInterpolation("RElbowYaw", 110.0 * almath.TO_RAD, 1.0, True)
        self.motionProxy.angleInterpolation("RShoulderPitch", 115.0 * almath.TO_RAD, 1.0, True)
        self.motionProxy.angleInterpolation("RShoulderRoll", -70.0 * almath.TO_RAD, 1.0, True)
        self.motionProxy.angleInterpolation("RShoulderPitch", 30.0 * almath.TO_RAD, 1.0, True)
        self.motionProxy.angleInterpolation("RElbowRoll", 80.0 * almath.TO_RAD, 1.0, True)
        self.motionProxy.angleInterpolation("RWristYaw", 80.0 * almath.TO_RAD, 1.0, True)
        self.motionProxy.angleInterpolation("RHand", 0.6, 1.0, True)

        # Move Right hand to initial state
        self.motionProxy.angleInterpolation("RShoulderPitch", 0.0 * almath.TO_RAD, 0.2, True)
        self.motionProxy.angleInterpolation("RElbowYaw", 0.0 * almath.TO_RAD, 1.0, True)
        self.motionProxy.angleInterpolation("RWristYaw", 90.0 * almath.TO_RAD, 0.2, True)
        self.motionProxy.angleInterpolation("RShoulderRoll", -50.0 * almath.TO_RAD, 1.0, True)

    # Go to ready Pos, and human can move the box to NAO
    def goToInitialPos(self):
        """
        Make NAO robot to a stable posture
        """
        # Stiffness body
        self.motionProxy.stiffnessInterpolation("Body", 1.0, 0.5)

        # Go to rest posture
        self.motionProxy.rest()

        # Stop basic awareness to stop head moving
        self.awareness.stopAwareness()

        # Stiffness
        self.motionProxy.stiffnessInterpolation("RHipRoll", 1.0, 0.2)
        self.motionProxy.stiffnessInterpolation("LHipRoll", 1.0, 0.2)
        self.motionProxy.stiffnessInterpolation("RHipPitch", 1.0, 0.2)
        self.motionProxy.stiffnessInterpolation("LHipPitch", 1.0, 0.2)
        self.motionProxy.stiffnessInterpolation("RHipYawPitch", 1.0, 0.2)
        self.motionProxy.stiffnessInterpolation("LHipYawPitch", 1.0, 0.2)
        self.motionProxy.stiffnessInterpolation("RArm", 1.0, 0.2)
        self.motionProxy.stiffnessInterpolation("LArm", 1.0, 0.2)
        self.motionProxy.stiffnessInterpolation("Head", 1.0, 0.2)

        # Move Left Hand
        names = ["LElbowRoll", "LShoulderRoll", "LElbowYaw"]
        angles = [-80.0* almath.TO_RAD, 30.0* almath.TO_RAD, -20.0* almath.TO_RAD]
        self.motionProxy.angleInterpolation(names, angles, 0.2, True)

        # Move Right Hand
        self.motionProxy.angleInterpolation("RHand", 0.0, 0.5, True)
        self.motionProxy.angleInterpolation("RElbowRoll", 70.0 * almath.TO_RAD, 0.2, True)
        self.motionProxy.angleInterpolation("RElbowYaw", 40.0 * almath.TO_RAD, 0.2, True)
        self.motionProxy.angleInterpolation("RShoulderRoll", -40.0 * almath.TO_RAD, 0.5, True)
        self.motionProxy.angleInterpolation("RShoulderPitch", 100.0 * almath.TO_RAD, 0.5, True)
        self.motionProxy.angleInterpolation("RWristYaw", 50.0 * almath.TO_RAD, 0.1, True)
        self.motionProxy.angleInterpolation("RShoulderRoll", -35.0 * almath.TO_RAD, 0.2, True)
        self.motionProxy.angleInterpolation("RElbowYaw", 30.0 * almath.TO_RAD, 0.1, True)
        self.motionProxy.angleInterpolation("RElbowRoll", 40.0 * almath.TO_RAD, 0.1, True)
        self.motionProxy.angleInterpolation("RShoulderRoll", -25.0 * almath.TO_RAD, 0.2, True)
        self.motionProxy.angleInterpolation("RElbowRoll", 20.0 * almath.TO_RAD, 0.2, True)
        self.motionProxy.angleInterpolation("RShoulderRoll", -15.0 * almath.TO_RAD, 0.2, True)
        self.motionProxy.angleInterpolation("RShoulderPitch", 90.0 * almath.TO_RAD, 0.5, True)

        # Move Head
        self.motionProxy.angleInterpolation("HeadPitch", 0.0 * almath.TO_RAD, 1.0, True)
        self.motionProxy.angleInterpolation("HeadYaw", 0.0 * almath.TO_RAD, 1.0, True)

        # Release the stiffness
        self.motionProxy.stiffnessInterpolation("RArm", 0.0, 1.0)
        self.motionProxy.stiffnessInterpolation("LArm", 0.0, 1.0)


        self.tts.say("I'm ready")
        print "Move the box to robot"

    # Move down the Pen.
    # Use position error sensor to judge whether the pen contact the tablet
    def penDown(self):

        # get Current Position
        path = "Motion/Position/Error/RShoulderPitch"
        PositionError = self.memoryProxy.getData(path)

        while PositionError <= 0:
            angle_RSPitch = self.motionProxy.getAngles("RShoulderPitch", True)[0]
            targetAngle = angle_RSPitch + 0.5 * almath.TO_RAD
            self.motionProxy.setAngles("RShoulderPitch", targetAngle, 0.1)  # Friction of max speed
            PositionError = self.memoryProxy.getData(path)

        angle_RSPitch = self.motionProxy.getAngles("RShoulderPitch", True)[0]
        self.motionProxy.setAngles("RShoulderPitch", angle_RSPitch, 0.2)  # Friction of max speed

    # Move up the pen
    def penUp(self):
        # Move up the pen
        self.motionProxy.angleInterpolation("RShoulderPitch", -5.0 * almath.TO_RAD, 2, True)

    # Read the point from the file and write directly
    def robot_drawing(self):

        self.motionProxy.angleInterpolation("RShoulderPitch", -10.0 * almath.TO_RAD, 0.2, True)

        self.tts.say("Read the data")
        self.cal.readFile()
        self.cal.imageToTablet()
        self.cal.angleCalculate()

        time.sleep(2)   # sleep 2 second

        names = ["RElbowRoll", "RShoulderRoll"]
        # calculate the Elbow angle and shoulder angle
        for i in range(len(self.cal.shoulderList)):
            self.penUp()
            angleLists = [self.cal.elbowList[i][0], self.cal.shoulderList[i][0]]
            isAbsolute = True
            self.motionProxy.angleInterpolation(names, angleLists, [1.0, 1.0], isAbsolute)
            self.penDown()
            angleLists = [self.cal.elbowList[i], self.cal.shoulderList[i]]
            timeLists = []
            EtimeLists = []
            StimeLists = []
            for j in range(len(self.cal.elbowList[i])):
                EtimeLists.append((j + 1) * 2)
                StimeLists.append((j + 1) * 2)
            timeLists.append(EtimeLists)
            timeLists.append(StimeLists)
            self.motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)

        self.penUp()
        self.tts.say("Drawing Finished")

    # Return to ready Pos
    def returnInitial(self):

        self.motionProxy.angleInterpolation("RShoulderRoll", -70.0 * almath.TO_RAD, 1.0, True)
        self.motionProxy.angleInterpolation("RElbowYaw", 0.0 * almath.TO_RAD, 1.0, True)
        self.motionProxy.angleInterpolation("RHand", 0.0, 1.0, True)
        self.motionProxy.angleInterpolation("RElbowRoll", 0.0 * almath.TO_RAD, 1.0, True)
        self.motionProxy.angleInterpolation("RShoulderPitch", 90.0 * almath.TO_RAD, 1.0, True)
        self.motionProxy.angleInterpolation("RShoulderRoll", 0.0 * almath.TO_RAD, 1.0, True)

    # Response to the key press
    def keyboardControl(self, command):

        if command == "Up":
            # Move up 0.01 meter
            currentPos = self.motionProxy.getPosition("RArm", motion.FRAME_TORSO, False)
            targetPos = almath.Position6D(currentPos)
            targetPos.x = targetPos.x + 0.01  # meter
            self.motionProxy.positionInterpolations("RArm", motion.FRAME_TORSO, list(targetPos.toVector()),
                                                    motion.AXIS_MASK_VEL, 2.0)
            self.adjust()

        if command == "Down":
            # Move down 0.01 meter
            currentPos = self.motionProxy.getPosition("RArm", motion.FRAME_TORSO, False)
            targetPos = almath.Position6D(currentPos)
            targetPos.x = targetPos.x - 0.01  # meter
            self.motionProxy.positionInterpolations("RArm", motion.FRAME_TORSO, list(targetPos.toVector()),
                                                    motion.AXIS_MASK_VEL, 2.0)
            self.adjust()

        if command == "Left":
            # Move left 0.01 meter
            currentPos = self.motionProxy.getPosition("RArm", motion.FRAME_TORSO, False)
            targetPos = almath.Position6D(currentPos)
            targetPos.y = targetPos.y + 0.01  # meter
            self.motionProxy.positionInterpolations("RArm", motion.FRAME_TORSO, list(targetPos.toVector()),
                                                    motion.AXIS_MASK_VEL, 2.0)
            self.adjust()

        if command == "Right":
            # Move right 0.01 meter
            currentPos = self.motionProxy.getPosition("RArm", motion.FRAME_TORSO, False)
            targetPos = almath.Position6D(currentPos)
            targetPos.y = targetPos.y - 0.01  # meter
            self.motionProxy.positionInterpolations("RArm", motion.FRAME_TORSO, list(targetPos.toVector()),
                                                    motion.AXIS_MASK_VEL, 2.0)
            self.adjust()

        if command == "PenUp":
            self.penUp()

        if command == "PenDown":
            self.penDown()

    # Readjust the shoulder pitch angle
    def adjust(self):
        # Detect the pressure
        self.motionProxy.angleInterpolation("RShoulderPitch", -3.0 * almath.TO_RAD, 0.2, True)
        # get Current Position
        path = "Motion/Position/Error/RShoulderPitch"
        PositionError = self.memoryProxy.getData(path)

        while PositionError <= 0:
            angle_RSPitch = self.motionProxy.getAngles("RShoulderPitch", True)[0]
            targetAngle = angle_RSPitch + 0.5 * almath.TO_RAD
            self.motionProxy.setAngles("RShoulderPitch", targetAngle, 0.1)  # Friction of max speed
            PositionError = self.memoryProxy.getData(path)
            # print "targetAngle: ", targetAngle

        angle_RSPitch = self.motionProxy.getAngles("RShoulderPitch", True)[0]
        self.motionProxy.setAngles("RShoulderPitch", angle_RSPitch, 0.2)  # Friction of max speed

    def graspPen(self, touchCommand):
        # Touch Frot tactile to grasp the pen
        touchCommand.subscribe("FrontTactileTouch")
        self.tts.say("Give me the pen and touch my Front Tactile")
        print "Give me the pen and touch my Front Tactile"
        touchCommand.touch_list = []
        count = 0
        while touchCommand.fort_touched == False:
            if count > 5:
                touchCommand.subscribe("FrontTactileTouch")
                count = 0
            time.sleep(1)
            count += 1
            pass
        touchCommand.fort_touched = False
        if "FrontTactile" in touchCommand.touch_list:
            touchCommand.touch_list = []
            self.motionProxy.angleInterpolation("RHand", 0.0, 0.2, True)
            print "Grasp the pen."

    def releasePen(self, touchCommand):
        # Release the pen
        touchCommand.touch_list = []
        touchCommand.subscribe("FrontTactileTouch")
        self.tts.say("Please touch Front Tactile to release the pen.")
        print "Please touch Front Tactile to release the pen."
        count = 0
        while touchCommand.fort_touched == False:
            if count > 5:
                touchCommand.subscribe("FrontTactileTouch")
                count = 0
            time.sleep(1)
            count += 1
            pass
        touchCommand.fort_touched = False

        if "FrontTactile" in touchCommand.touch_list:
            touchCommand.touch_list = []
            self.motionProxy.angleInterpolation("RHand", 0.6, 0.2, True)
            print "Release the pen."

