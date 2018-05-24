"""

QLearning module set up a Qtable.

"""

import numpy as np
import pandas as pd
from ast import literal_eval
from random import randint

class Q_Table:
    def __init__(self, actions, learning_rate, reward_decay, e_greedy):
        self.actions = actions
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        # Initial q_table
        self.q_table = pd.DataFrame(columns=self.actions, dtype= np.float64)

    def choose_action(self, state):
        # check whether the state is in table
        self.check_exist(state)

        # epsilon greedy
        if randint(1, 10) <= (10 * self.epsilon):
            # Choose best action
            # A primarily label-location based indexer, with integer position fallback.
            actions = self.q_table.ix[state,:]
            # randomly choose an action: some actions may have the same value
            actions = actions.reindex(np.random.permutation(actions.index))
            choose_action = actions.idxmax()
        else:
            # randomly choose an action
            index = randint(0, len(self.actions)-1)
            choose_action = self.actions[index]

        return choose_action

    def renew_qtable(self, state, action, reward, nextState):
        self.check_exist(nextState)

        q_state_action = self.q_table.loc[state, action]
        # Choose the largest q_value of next state
        q_nextState_atcion = self.q_table.loc[nextState,:].max()

        # renew
        self.q_table.loc[state, action] += self.lr * (reward + self.gamma
                                                     * q_nextState_atcion - q_state_action)

    def check_exist(self, state):
        tuple_state = literal_eval(state)
        if state not in self.q_table.index:
            row = pd.Series(
                data = [0.0]*len(self.actions),
                index= self.q_table.columns,
                name = state
            )
            # Give the those actions which are the same as state a large negative value
            if str(tuple_state[0][0]) in self.q_table.columns:
                row[str(tuple_state[0][0])] = -float("inf")
            if str(tuple_state[0][1]) in self.q_table.columns:
                row[str(tuple_state[0][1])] = -float("inf")
            self.q_table = self.q_table.append(row)