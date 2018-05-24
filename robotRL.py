"""

This module set up the robot leaning environment.

The State set = {current(), achieved[]}
current = ((E, S), penState)
(E, S) is the angle of robot's RElobowRoll and RShoulderRoll, penSatte is a string variable: "True" for pendown, "False" for penup
achieved = [((E1, S1), penState), ((E2, S2), penState), ...]:
achieved store the reward that has been achieved

The Action set = {True, False, (E1,S1), (E2,S2)...}. The action comes from rewards.

Reward is read from file and process. Format: ((E, S), Boolean(True for pendown, False for penup):
Once the reward is reach, it disapear from map.
"""

import drawAction
import time
import almath
from naoqi import ALProxy


class robot_RL():
    def __init__(self, reward_list):
        self.motionProxy = ALProxy("ALMotion")
        self.reward_list = reward_list
        self.draw = drawAction.drawAction()
        self.reward_count = 0
        self.action_count = 0
        """
        Arm movement parameter
        """
        self.names = ["RElbowRoll", "RShoulderRoll"]
        self.isAbsolute = True
        self.timeLists = [2, 2]

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
        self.action_count += 1

        current_angle = current_state[0][0]  # current (E, S)
        current_penState = current_state[0][1]
        next_angle = None
        next_penState = None

        if len(action) == 2:
            # Set the angle
            next_angle = action
            next_penState = current_penState

            next_E = next_angle[0]  # Degree
            next_S = next_angle[1]  # Degree

            # Move the arm
            E = next_E * almath.TO_RAD
            S = next_S * almath.TO_RAD
            angleLists = [E, S]
            self.motionProxy.angleInterpolation(self.names, angleLists, self.timeLists, self.isAbsolute)

        else:
            # Change penstate
            if current_penState != action:
                next_penState = action
                next_angle = current_angle

                # Move the arm
                if next_penState == "True":
                    self.draw.penDown()
                else:
                    self.draw.penUp()

            else:
                # Same state
                next_angle = current_angle
                next_penState = current_penState

        """
        Set the reward
        """
        current_achieved = current_state[1]
        next_achieved = []
        reward = 0

        # Initial state
        if len(current_achieved) == 0:
            if (next_angle, next_penState) == self.reward_list[self.reward_count]:
                reward += 1
                achieve_reward = self.reward_list[self.reward_count]
                next_achieved.append(achieve_reward)
                self.renew_reward()
                done = False
            else:
                reward -= 1
                done = False

        else:
            if (next_angle, next_penState) == self.reward_list[self.reward_count]\
                and current_achieved[-1] == self.reward_list[self.reward_count - 1]:
                reward += 1
                achieve_reward = self.reward_list[self.reward_count]
                next_achieved = current_achieved[:]
                next_achieved.append(achieve_reward)
                if len(next_achieved) == len(self.reward_list):
                    done = True
                else:
                    self.renew_reward()
                    done = False
            else:
                reward -= 1
                done = False

        # Take len(self.reward_list) actions then finish this episode
        if self.action_count == len(self.reward_list):
            done = True

        next_state = [(next_angle, next_penState), next_achieved]

        return next_state, reward, done

    def reset(self):
        time.sleep(0.5)

        # Move arm to initial state
        self.draw.penUp()
        initial_penstate = "False"

        E = 80 * almath.TO_RAD
        S = -50 * almath.TO_RAD
        angleLists = [E, S]
        self.motionProxy.angleInterpolation(self.names, angleLists, self.timeLists, self.isAbsolute)

        # initialize the reward count
        self.reward_count = 0

        # Initialize the action count
        self.action_count = 0

        # Return the initial state
        initial_state = [((80, -50), initial_penstate), []]

        return initial_state

    def renew_reward(self):
        self.reward_count += 1

    def refresh(self):
        time.sleep(0.05)

