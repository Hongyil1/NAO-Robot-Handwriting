"""
environment module set up the simulation environment for simulator.
The State set = {current(), achieved[]}
current = ((E, S), penState)
(E, S) is the angle of robot's RElobowRoll and RShoulderRoll, penSatte is a string variable: "True" for pendown, "False" for penup
achieved = [((E1, S1), penState), ((E2, S2), penState), ...]:
achieved store the reward that has been achieved

The Action set = {True, False, (E1,S1), (E2,S2)...}. The action comes from rewards.

Reward is read from file and process. Format: ((E, S), Boolean(True for pendown, False for penup):
Once the reward is reach, it disapear from map.
"""
import tkinter as tk
import math
import time
import ctypes
from ast import literal_eval as make_tuple

width = 640
height = 480
class simulation(tk.Tk, object):
    def __init__(self):
        super(simulation, self).__init__()
        """
        Window parameters
        """
        self.title("Robot Arm Simulation")
        self.geometry('{0}x{1}'.format(width, height))
        self.mToPixel = 3779.5275591

        """
        Simulator parameters
        """
        self.action_space = ["True", "False"]   # The set of action
        self.reward_list_cor = []
        self.reward_list_angle = []
        self.imgae_list = []
        self.reward_count = 0

        """
        Arm paramters
        """
        self.l_upperarm = int(0.105 * self.mToPixel) * 0.55
        self.l_forearm = int(0.1137 * self.mToPixel) * 0.55
        self.r_joint1 = 10  # radius of joint1
        self.r_joint2 = 5   # radius of joint2
        self.r_pen = 1      # radius of pen
        self.Delta = 8.21   # Angle between X axis and upper arm in degree
        self.Theta = 15.79  # Angle between upper arm and forearm in degree
        self.upperarm = None
        self.forearm = None
        self.joints = None  # current joints state
        self.hand = None
        self.joint1 = None
        self.joint2 = None

        """
        Tablet parameter
        """
        self.up_boundary = height - int(0.205 * self.mToPixel * 0.55)
        self.down_boundary = height - int(0.155 * self.mToPixel * 0.55)
        self.left_boundary = width / 2 - int(0.06 * self.mToPixel * 0.55)
        self.right_boundary = width / 2 + int(0.06 * self.mToPixel * 0.55)

        # Initial the simulator
        self.build_simulation()

    # build up the simulator
    def build_simulation(self):

        self.canvas = tk.Canvas(self, bg='white',
                                width = width,
                                height = height)
        # Get the reward list
        self.image_process()

        # Get the joints position: forward kinematic
        initial_joints = self.joint_calculation(Elbow_roll= 80, Shoulder_roll= -50)
        old_pos = initial_joints[2]
        initial_penState = "False"

        # Move the arm to initial state
        self.arm_move(initial_joints, initial_penState, old_pos)

        # Draw tablet
        self.draw_tablet()

        # Draw Drawing area
        self.draw_drawArea()

        # Draw reward
        r_x = self.reward_list_cor[self.reward_count][0][0]
        r_y = self.reward_list_cor[self.reward_count][0][1]
        x1, y1 = r_x - 2, r_y - 2
        x2, y2 = r_x + 2, r_y + 2
        self.reward_oval = self.canvas.create_oval(x1, y1, x2, y2, fill='yellow')

        self.acion_count = 0

        self.canvas.pack()

    # Renew the current sate according to action. Return the next_state
    # reward and whether the epsiode is done.
    def step(self, current_state, action):
        """
        current_sate = (((E, S), penState), achieved[])

        ((E, S), penState)
        (E, S) are the angles of RElbowRoll and RShoulderRoll, penSatte is a string variable: "True" for pendown, "False" for penup

        achieved = [((E1, S1), penState), ((E2, S2), penState), ...]:
        achieved store the reward that has been achieved

        action = (E,S), "True" or "False"

        self.reward_list = [((E1, S1), penState), ((E2, S2), penState)...]

        """

        self.acion_count += 1

        current_angle = current_state[0][0]  # current (E, S)
        current_penState = current_state[0][1]
        next_angle = None
        next_penState = None

        if len(action) == 2:
            # Move action, set the angle
            next_angle = action
            next_penState = current_penState

            next_E = next_angle[0]
            next_S = next_angle[1]
            current_E = current_angle[0]
            current_S = current_angle[1]

            current_joints = self.joint_calculation(current_E, current_S)
            current_pos = current_joints[2]
            next_joints = self.joint_calculation(next_E, next_S)
            self.arm_move(next_joints, next_penState, current_pos)

        else:
            # Change the penState
            if current_penState != action:
                next_penState = action
                next_angle = current_angle
                self.canvas.delete(self.upperarm)
                self.canvas.delete(self.forearm)
                current_joints = self.joints
                # Change the color
                if next_penState == "True":
                    # Black
                    self.upperarm = self.canvas.create_line(current_joints[0][0], current_joints[0][1], current_joints[1][0],
                                                            current_joints[1][1],
                                                            fill='black', width=4)
                    self.forearm = self.canvas.create_line(current_joints[1][0], current_joints[1][1], current_joints[2][0],
                                                           current_joints[2][1],
                                                           fill='black', width=2)
                else:
                    # Red
                    self.upperarm = self.canvas.create_line(current_joints[0][0], current_joints[0][1], current_joints[1][0],
                                                            current_joints[1][1],
                                                            fill='red', width=4)
                    self.forearm = self.canvas.create_line(current_joints[1][0], current_joints[1][1], current_joints[2][0],
                                                           current_joints[2][1],
                                                           fill='red', width=2)
                self.refresh()
            else:
                # Same penState
                next_angle = current_angle
                next_penState = current_penState

        """
        Set the reward
        """
        current_achieved = current_state[1]
        next_achieved = []
        reward = 0

        # Initial State
        if len(current_achieved) == 0:
            if (next_angle, next_penState) == self.reward_list_angle[self.reward_count]:
                reward += 1
                achieve_reward = self.reward_list_angle[self.reward_count]
                next_achieved.append(achieve_reward)
                # Renew the reward
                self.renew_reward()
                done = False
            else:
                reward -= 1
                done = False
        else:
            if (next_angle, next_penState) == self.reward_list_angle[self.reward_count]\
                    and current_achieved[-1] == self.reward_list_angle[self.reward_count - 1]:
                reward += 1
                achieve_reward = self.reward_list_angle[self.reward_count]
                # Important, copy list problem!
                next_achieved = current_achieved[:]
                next_achieved.append(achieve_reward)
                if len(next_achieved) == len(self.reward_list_angle):
                    done = True
                else:
                    self.renew_reward()
                    done = False
            else:
                reward -= 1
                done = False

        # Take len(self.reward_list) actions then finish this episode
        if self.acion_count == len(self.reward_list_angle):
            done = True

        next_state = [(next_angle, next_penState), next_achieved]

        return next_state, reward, done

    # Return to the initial state
    def reset(self):
        """
        Return the initial state and start the next episode
        """

        time.sleep(0.5)
        # delect all elements in canvas
        self.canvas.delete("all")

        initial_joints = self.joint_calculation(Elbow_roll=80, Shoulder_roll=-50)
        old_pos = initial_joints[2]
        initial_penState = "False"

        # Move the arm to initial state
        self.arm_move(initial_joints, initial_penState, old_pos)

        # Draw tablet
        self.draw_tablet()

        # Draw draw area
        self.draw_drawArea()

        # Initial the reward_count
        self.reward_count = 0

        # Draw reward
        r_x = self.reward_list_cor[self.reward_count][0][0]
        r_y = self.reward_list_cor[self.reward_count][0][1]
        x1, y1 = r_x - 2, r_y - 2
        x2, y2 = r_x + 2, r_y + 2
        self.reward_oval = self.canvas.create_oval(x1, y1, x2, y2, fill='yellow')

        self.acion_count = 0

        # Return the state:
        initial_state = [((80, -50), initial_penState), []]

        self.refresh()

        return initial_state

    # renew the reward
    def renew_reward(self):

        self.reward_count += 1
        self.canvas.delete(self.reward_oval)
        r_x = self.reward_list_cor[self.reward_count][0][0]
        r_y = self.reward_list_cor[self.reward_count][0][1]
        x1, y1 = r_x - 2, r_y - 2
        x2, y2 = r_x + 2, r_y + 2
        self.reward_oval = self.canvas.create_oval(x1, y1, x2, y2, fill='yellow')
        self.refresh()

    # Refresh the canvas
    def refresh(self):
        time.sleep(0.005)
        # Enter event loop until all
        # pending events have been processed by Tcl.
        self.update()

    # foward kinematic
    def joint_calculation(self, Elbow_roll, Shoulder_roll):

        Delta = self.Delta
        Theta = self.Theta

        x_joint1 = int(width/2)
        y_joint1 = int(height)

        x_joint2 = int(x_joint1 - self.l_upperarm * math.sin(math.radians(Shoulder_roll - Delta)))
        y_joint2 = int(y_joint1 - self.l_upperarm * math.cos(math.radians(Shoulder_roll - Delta)))

        x_pen = int(x_joint2 - self.l_forearm * math.sin(math.radians(Elbow_roll + Theta + Shoulder_roll - Delta)))
        y_pen = int(y_joint2 - self.l_forearm * math.cos(math.radians(Elbow_roll + Theta + Shoulder_roll - Delta)))

        joints = [(x_joint1, y_joint1), (x_joint2, y_joint2), (x_pen, y_pen)]

        self.joints = joints # Current joints state

        return joints

    # Move the arm on the canvas
    def arm_move(self, new_joints, penState, old_pos):

        if self.upperarm != None:
            self.canvas.delete(self.upperarm)
            self.canvas.delete(self.forearm)
            self.canvas.delete(self.joint2)
            self.canvas.delete(self.hand)

        new_pos = new_joints[2] # current pen position

        # Joints and arms
        if penState == "True":
            # PenDown
            self.upperarm = self.canvas.create_line(new_joints[0][0], new_joints[0][1], new_joints[1][0], new_joints[1][1],
                                    fill = 'black', width = 4)
            self.forearm = self.canvas.create_line(new_joints[1][0], new_joints[1][1], new_joints[2][0], new_joints[2][1],
                                    fill = 'black', width = 2)

            if new_pos != old_pos:
                # Draw a line
                self.canvas.create_line(old_pos[0], old_pos[1], new_pos[0], new_pos[1],
                                        fill='black', width=2)
        else:
            # Penup
            self.upperarm = self.canvas.create_line(new_joints[0][0], new_joints[0][1], new_joints[1][0],
                                                   new_joints[1][1],
                                                   fill='red', width=4)
            self.forearm = self.canvas.create_line(new_joints[1][0], new_joints[1][1], new_joints[2][0],
                                                   new_joints[2][1],
                                                   fill='red', width=2)

        self.joint1 = self.canvas.create_oval(new_joints[0][0] - self.r_joint1, new_joints[0][1] - self.r_joint1,
                                              new_joints[0][0] + self.r_joint1, new_joints[0][1] + self.r_joint1,
                                fill = 'black')
        self.joint2 = self.canvas.create_oval(new_joints[1][0] - self.r_joint2, new_joints[1][1] - self.r_joint2,
                                              new_joints[1][0] + self.r_joint2, new_joints[1][1] + self.r_joint2,
                                fill = 'black')
        self.hand = self.canvas.create_oval(new_joints[2][0] - self.r_pen, new_joints[2][1] - self.r_pen,
                                            new_joints[2][0] + self.r_pen, new_joints[2][1] + self.r_pen,
                                fill = 'black')
        self.refresh()

    # Draw the tablet area
    def draw_tablet(self):
        self.canvas.create_line(self.left_boundary, self.up_boundary, self.left_boundary, self.down_boundary,
                                fill = 'black')
        self.canvas.create_line(self.right_boundary, self.up_boundary, self.right_boundary, self.down_boundary,
                                fill='black')
        self.canvas.create_line(self.left_boundary, self.up_boundary, self.right_boundary, self.up_boundary,
                                fill='black')
        self.canvas.create_line(self.left_boundary, self.down_boundary, self.right_boundary, self.down_boundary,
                                fill='black')

    # The area the letter will be draw
    def draw_drawArea(self):
        # draw the Draw area
        self.canvas.create_line(self.draw_area_xmin, self.draw_area_ymin, self.draw_area_xmin, self.draw_area_ymax,
                                fill='red')
        self.canvas.create_line(self.draw_area_xmax, self.draw_area_ymin, self.draw_area_xmax, self.draw_area_ymax,
                                fill='red')
        self.canvas.create_line(self.draw_area_xmin, self.draw_area_ymin, self.draw_area_xmax, self.draw_area_ymin,
                                fill='red')
        self.canvas.create_line(self.draw_area_xmin, self.draw_area_ymax, self.draw_area_xmax, self.draw_area_ymax,
                                fill='red')

    # Coordinate system transformation
    def imageToSimulator(self, x_i, y_i):

        """
        Map from Human handwriting image to simulator tablet
        """
        x_t_max, y_t_max, x_t_min, y_t_min = self.right_boundary, self.down_boundary, self.left_boundary, self.up_boundary
        x_t_centre = (x_t_min + x_t_max) / 2
        y_t_centre = (y_t_min + y_t_max) / 2

        # Read the resolution of screen
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)     #(x, y)
        draw_area_height = (y_t_max - y_t_min)   # Scale
        draw_area_width = screensize[0] / float(screensize[1]) * draw_area_height

        self.draw_area_xmin = int(x_t_centre - draw_area_width * 0.5)
        self.draw_area_xmax = int(x_t_centre + draw_area_width * 0.5)
        self.draw_area_ymin = int(y_t_centre - draw_area_height * 0.5)
        self.draw_area_ymax = int(y_t_centre + draw_area_height * 0.5)

        x_t = self.draw_area_xmin + (draw_area_width / float(screensize[0])) * x_i
        y_t = self.draw_area_ymin + (draw_area_height / float(screensize[1])) * y_i

        return round(x_t, 0), round(y_t, 0)

    # Generate the reward_list
    def image_process(self):
        """
        Proecess the data of human writing image and generate the reward_list
        :return:
        """

        # Initial the value
        x_max = -float("inf")
        y_max = -float("inf")
        x_min = float("inf")
        y_min = float("inf")

        # Read reward from file
        file = open("imageList.txt", "r")
        draw = file.readline()
        while draw:
            draw = draw.replace("[", "")
            draw = draw.replace("]", "")
            draw = list(make_tuple(draw))
            self.imgae_list.append((draw[0], "False"))
            for point in draw:
                if point[0] > x_max:
                    x_max = round(point[0], 0)
                if point[0] < x_min:
                    x_min = round(point[0], 0)
                if point[1] > y_max:
                    y_max = round(point[1], 0)
                if point[1] < y_min:
                    y_min = round(point[1], 0)
                self.imgae_list.append((point, "True"))   # pendown
            self.imgae_list.append((draw[-1], "False"))
            draw = file.readline()
        file.close()

        for tuple in self.imgae_list:
            x_i = tuple[0][0]
            y_i = tuple[0][1]
            x_t, y_t = self.imageToSimulator(x_i, y_i)
            """
            Change coordinate to angle
            """
            x_joint1 = int(width / 2)
            y_joint1 = int(height)

            x = x_t - x_joint1
            y = y_t - y_joint1
            E = self.RElbowRoll(x, y)
            S = self.RshoulderRoll(x, y, E)

            self.reward_list_cor.append(((int(x_t), int(y_t)), tuple[1])) # Penup
            self.reward_list_angle.append(((round(E, 2), round(S, 2)), tuple[1]))
            if (round(E, 2), round(S, 2)) not in self.action_space:
                self.action_space.append((round(E, 2), round(S, 2)))  # Generate the action_space

    # Inversed kinematic: calculate the Elbow angle
    def RElbowRoll(self, x, y):
        """
        The angle is relative to the current angle
        """

        # y = y + 0.098   # coordinate in right shoulder joint
        sqr1 = pow(x, 2) + pow(y, 2)
        sqr2 = pow(self.l_upperarm, 2) + pow(self.l_forearm, 2)
        E = - self.Theta + math.degrees(math.acos((sqr1 - sqr2) / (2 * self.l_upperarm * self.l_forearm)))
        return E

    # Inversed kinemacti: calculate the shoulder angle
    def RshoulderRoll(self, x, y, E):
        numerator1 = x * (self.l_upperarm + self.l_forearm * math.cos(math.radians(E + self.Theta)))
        numerator2 = y * self.l_forearm * math.sin(math.radians(E + self.Theta))
        denominator1 = y * (self.l_upperarm + self.l_forearm * math.cos(math.radians(E + self.Theta)))
        denominator2 = x * self.l_forearm * math.sin(math.radians(E + self.Theta))
        S = self.Delta + math.degrees(math.atan((numerator1 - numerator2) / (denominator1 + denominator2)))
        return S

















