"""

This module do the calculation for simulator

"""

import math
import almath
import ctypes
from ast import literal_eval as make_tuple


class AngleCalculate():
    def __init__(self):
        self.a = 0.105  # Length of Upper arm in meter
        self.b = 0.1137 # Length of forearm in meter
        self.Delta = 8.21   # Angle between X axis and upper arm in degree
        self.Theta = 15.79  # Angle between upper arm and forearm in degree

        self.imageList = []
        self.tabletList = []
        self.elbowList = []
        self.shoulderList = []
        self.x_t_max = 0.205    # in meter  0.205 (shoulder coordinate)
        self.x_t_min = 0.155    # in meter  0.155
        self.y_t_max = 0.06    #  0.06
        self.y_t_min = -0.06    # -0.06
        self.pixelToMeter = 0.00026458333333333

    def readFile(self):
        self.imageList = []
        # Read drawList from file
        file = open("imageList.txt", "r")
        draw = file.readline()
        while draw:
            newstr = draw.replace("[", "")
            newstr = newstr.replace("]", "")
            draw = list(make_tuple(newstr))
            self.imageList.append(draw)
            draw = file.readline()
        file.close()

    def imageToTablet(self):

        # Read the resolution of screen
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)     #(x, y)
        draw_area_height = (self.x_t_max - self.x_t_min)  # Scale
        draw_area_width = screensize[0] / float(screensize[1]) * draw_area_height

        x_t_centre = (self.x_t_min + self.x_t_max) / 2
        y_t_centre = (self.y_t_min + self.y_t_max) / 2

        draw_area_xmax = x_t_centre + draw_area_height * 0.5
        draw_area_ymax = y_t_centre + draw_area_width * 0.5


        self.tabletList = []
        for list in self.imageList:
            line = []
            for tuple in list:
                x_t = draw_area_xmax - (draw_area_height / (screensize[1] * self.pixelToMeter)) * tuple[1] * self.pixelToMeter
                y_t = draw_area_ymax - (draw_area_width / (screensize[0] * self.pixelToMeter)) * tuple[0] * self.pixelToMeter
                point = (round(x_t, 3), round(y_t, 3))
                line.append(point)
            self.tabletList.append(line)



    def RElbowRoll(self, x, y):     # in degree
        """
        The angle is relative to the current angle
        """
        # y = y + 0.098   # coordinate in right shoulder joint
        sqr1 = pow(x, 2) + pow(y, 2)
        sqr2 = pow(self.a, 2) + pow(self.b, 2)
        E = - self.Theta + math.degrees(math.acos((sqr1 - sqr2) / (2*self.a*self.b)))
        return E

    def RShoulderRoll(self, x, y, E):    # in degree
        numerator1 = y * (self.a + self.b * math.cos(math.radians(E + self.Theta)))
        numerator2 = x * self.b * math.sin(math.radians(E + self.Theta))
        denominator1 = x * (self.a + self.b * math.cos(math.radians(E + self.Theta)))
        denominator2 = y * self.b * math.sin(math.radians(E + self.Theta))
        S = self.Delta + math.degrees(math.atan((numerator1 - numerator2) / (denominator1 + denominator2)))
        return S

    def angleCalculate(self):
        self.elbowList = []
        self.shoulderList = []
        for list in self.tabletList:
            Elist = []
            Slist = []
            for tuple in list:
                E = self.RElbowRoll(tuple[0], tuple[1])
                S = self.RShoulderRoll(tuple[0], tuple[1], E)
                # Change to radian
                E = E * almath.TO_RAD
                S = S * almath.TO_RAD
                E = round(E, 2)
                S = round(S, 2)
                Elist.append(E)
                Slist.append(S)
            self.elbowList.append(Elist)
            self.shoulderList.append(Slist)








