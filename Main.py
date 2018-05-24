"""

Main module to run NAO handwriting learning program.
There are three modes: robot writing, reinforcement learning and keyboard control.
Modes can be selected by touching different area of NAO's head sensor.

Accept auguments: -ip -port
(example: -ip 192.168.1.100)

@ author: Hongyi Lin(838776)
@ since: 23rd Feb 2018

"""


import argparse
import drawAction
import Calibration
import time
import subprocess
import Painter
import tkinter as tk
import pandas as pd

from naoqi import ALBroker
from touchEvent import ReactToTouchModule
from Learning_Main import update
from environment import simulation
from robotRL import robot_RL
from QLearning import Q_Table


if __name__ == "__main__":
    """
    Set the Broker
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-ip", type=str, default="localhost",
                        help="Robot ip address")
    parser.add_argument("-port", type=int, default=9559,
                        help="Robot port number")
    args = parser.parse_args()

    myBroker = ALBroker("myBroker",
                        "0.0.0.0",  # Listen to anyone
                        0,  # Find a free port and use it
                        args.ip,  # Parent broker ip
                        args.port)  # Parent broker port

    app = drawAction.drawAction()

    # Stop awareness
    app.awareness.stopAwareness()

    # Go to initial state
    app.tts.say("Go to initial state")
    print "Go to initial state"
    app.goToInitialPos()
    first_time = True

    # Mode choose
    global touchCommand
    touchCommand = ReactToTouchModule("touchCommand")
    touchCommand.touch_list = []
    touchCommand.subscribe("FrontTactileTouch", "MiddleTactileTouch", "RearTactileTouch")
    while True:
        print ""
        print "[1] Touch Front Tactile to start Human-robot interaction."
        print "[2] Touch Middle Tactile to start keyboard control model."
        print "[3] Touch Rear Tactile to end the program."
        print ""
        app.tts.say("Please choose next step.")
        count = 0
        while touchCommand.fort_touched == False and touchCommand.middle_touched == False\
                and touchCommand.rear_touched == False:
            if count > 5:
                # Resubscribe in case miss the touch
                touchCommand.subscribe("FrontTactileTouch", "MiddleTactileTouch", "RearTactileTouch")
                count = 0
            time.sleep(1)
            count += 1
            pass
        touchCommand.fort_touched = False
        touchCommand.middle_touched = False
        touchCommand.rear_touched = False

        """
        Human-Robot interation. 
        In this section, you can choose the robot writing mode and RL mode.
        In this section, you will be required to write down some sample letters for NAO to learn.
        """

        if "FrontTactile" in touchCommand.touch_list:
            touchCommand.touch_list = []
            # touchCommand.buttonName = None
            app.tts.say("Human robot interaction start.")
            print "Human robot interaction start"
            print "Please take the tablet to write."
            app.tts.say("Please take the tablet to write.")
            app.humanWrite()

            # If the box hasn't been located, start the calibration program
            if first_time:
                first_time = False
                root1 = tk.Tk()
                calibration1 = Calibration.Calibration(root1)
                calibration1.tts.say("Open the window")
                print "Open the calibration window."
                print "Please give me the tablet."
                app.tts.say("Please give me the tablet.")
                calibration1.startCalibrationWindow()
                calibration1.window.mainloop()

            app.prepare_Pen()
            # Touch Frot tactile to grasp the pen
            app.graspPen(touchCommand)

            # Robot write or Learning
            touchCommand.subscribe("FrontTactileTouch", "MiddleTactileTouch", "RearTactileTouch")
            while True:
                print ""
                print "[1] Touch Front Tactile to start robot writing."
                print "[2] Touch Middle Tactile to start Reinforcement Learning."
                print "[3] Touch Rear Tactile to break the loop"
                print ""
                app.tts.say("Please choose the model.")
                count = 0
                while touchCommand.fort_touched == False \
                        and touchCommand.middle_touched == False\
                        and touchCommand.rear_touched == False:
                    if count > 5:
                        touchCommand.subscribe("FrontTactileTouch", "MiddleTactileTouch", "RearTactileTouch")
                        count = 0
                    time.sleep(1)
                    count += 1
                    pass
                touchCommand.fort_touched = False
                touchCommand.middle_touched = False
                touchCommand.rear_touched = False

                #####################
                #   Robot writing   #
                #####################
                """
                In robot writing mode, NAO will read the target points from the file. 
                And write the letters given by human directly. 
                """
                if "FrontTactile" in touchCommand.touch_list:
                    touchCommand.touch_list = []
                    # Robot writing
                    app.tts.say("Robot writing start.")
                    subprocess.Popen("Py -2.7 Painter.py")
                    app.robot_drawing()

                #############################
                #   Reinforcement Learning  #
                #############################
                """
                In RL mode, you can training the robot to find the corrrect order to
                connect all the target points and then get the target letters.
                There are two kinds of learning method: simulator and robot learning.
                """
                if "MiddleTactile" in touchCommand.touch_list:
                    touchCommand.touch_list = []

                    # Simulation in simulator. Learning 20 times
                    app.tts.say("Reinforcement Learning simulator start.")
                    str_action_space = []
                    sim = simulation()
                    for i in range(0, len(sim.action_space)):
                        action = str(sim.action_space[i])
                        str_action_space.append(action)
                    QLearning = Q_Table(actions=str_action_space, learning_rate=0.01,
                                        reward_decay=0.9, e_greedy=1)
                    num_episode = 20
                    model = "Simulator"
                    reward_list = []
                    reward_list = sim.reward_list_angle[:]
                    sim.after(100, update(sim, QLearning, num_episode=num_episode, model=model))
                    sim.mainloop()
                    # Save the q_table
                    QLearning.q_table.to_pickle("q_table.pkl")

                    # Choose next step:
                    # [1] Use simulator to learn 5 more times
                    # [2] Use robot to learn 2 more times
                    touchCommand.subscribe("FrontTactileTouch", "MiddleTactileTouch", "RearTactileTouch")
                    while True:
                        print ""
                        print "[1] Touch Front Tactile to use simulator to learn 5 more times."
                        print "[2] Touch Middle Tactile to use robot to learn 2 more times."
                        print "[3] Touch Rear Tactile to break the loop"
                        print ""
                        app.tts.say("Please choose the model.")
                        count = 0
                        while touchCommand.fort_touched == False \
                                and touchCommand.middle_touched == False \
                                and touchCommand.rear_touched == False:
                            if count > 5:
                                touchCommand.subscribe("FrontTactileTouch", "MiddleTactileTouch", "RearTactileTouch")
                                count = 0
                            time.sleep(1)
                            count += 1
                            pass
                        touchCommand.fort_touched = False
                        touchCommand.middle_touched = False
                        touchCommand.rear_touched = False

                        #########################################
                        #   Simulator learning 5 more times     #
                        #########################################
                        if "FrontTactile" in touchCommand.touch_list:
                            touchCommand.touch_list = []
                            app.tts.say("simulator learnng start.")
                            # Read the q_table
                            new_qTable = pd.read_pickle("q_table.pkl")
                            # Renew the q_table
                            QLearning.q_table = new_qTable
                            num_episode = 5
                            model = "Simulator"
                            reward_list = []
                            reward_list = sim.reward_list_angle[:]
                            sim = simulation()
                            sim.after(100, update(sim, QLearning, num_episode=num_episode, model=model))
                            sim.mainloop()
                            # Save the q_table
                            QLearning.q_table.to_pickle("q_table.pkl")

                        #################################
                        #   Robot learning 2 more times #
                        #################################
                        if "MiddleTactile" in touchCommand.touch_list:
                            touchCommand.touch_list = []
                            app.tts.say("Robot learnng start.")
                            # Read the q_table
                            new_qTable = pd.read_pickle("q_table.pkl")
                            subprocess.Popen("Py -2.7 Painter.py")
                            robot_sim = robot_RL(reward_list)
                            # Renew the q_table
                            QLearning.q_table = new_qTable
                            num_episode = 2
                            model = "Robot"
                            update(robot_sim, QLearning, num_episode = num_episode, model = model)
                            # Save the q_table
                            QLearning.q_table.to_pickle("q_table.pkl")
                            app.penUp()
                            app.tts.say("robot learning finish, please close the window.")

                        # Break the loop
                        if "RearTactile" in touchCommand.touch_list:
                            touchCommand.touch_list = []
                            app.tts.say("Break the loop")
                            print "break the loop"
                            break

                        # global touchCommand
                        touchCommand.subscribe("FrontTactileTouch", "MiddleTactileTouch", "RearTactileTouch")

                # Brek the loop
                if "RearTactile" in touchCommand.touch_list:
                    touchCommand.touch_list = []
                    app.tts.say("Break the loop")
                    print "break the loop"
                    break

                # global touchCommand
                touchCommand.subscribe("FrontTactileTouch", "MiddleTactileTouch", "RearTactileTouch")

            # Release the pen
            app.releasePen(touchCommand)

            # Return to initial pos
            app.returnInitial()

        #########################
        #   Keyboard control    #
        #########################
        """
        Keyboard control mode allow user control NAO's write hand to draw.
            Key: "W", "A", "S", "D", "Up", "Down"
        Command: up, left, down, right, Penup, Pendown
        "Space": claer the screen and save the writing.
        "Esc": close the window.  
        """
        if "MiddleTactile" in touchCommand.touch_list:
            # touchCommand.buttonName = None
            touchCommand.touch_list = []
            app.tts.say("Keyboard control start")

            if first_time:
                # First time, calibration
                first_time = False
                root1 = tk.Tk()
                calibration1 = Calibration.Calibration(root1)
                calibration1.tts.say("Open the window")
                print "Open the calibration window."
                print "Please give me the tablet."
                app.tts.say("Please give me the tablet.")
                calibration1.startCalibrationWindow()
                calibration1.window.mainloop()
            app.prepare_Pen()

            # Touch Frot tactile to grasp the pen
            app.graspPen(touchCommand)

            painter = Painter.Painter()
            painter.keyboardControl()
            app.penUp()

            # Release the pen
            app.releasePen(touchCommand)

            # Return to initial pos
            app.returnInitial()

        # if touchCommand.buttonName == "RearTactile":
        if "RearTactile" in touchCommand.touch_list:
            touchCommand.touch_list = []
            # touchCommand.buttonName = None
            app.tts.say("End the programe")
            print "Please Move the box away."
            app.tts.say("Please move the box away.")
            time.sleep(3)
            break

        # global touchCommand
        touchCommand.subscribe("FrontTactileTouch", "MiddleTactileTouch", "RearTactileTouch")

    app.motionProxy.stiffnessInterpolation("Body", 1.0, 0.5)
    app.motionProxy.rest()
    print "Programe Finish"

