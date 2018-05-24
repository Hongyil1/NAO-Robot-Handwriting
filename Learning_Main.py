"""

This module control the whole system of Q_learning

"""
import time
import drawAction
from ast import literal_eval

def update(sim, QLearning, num_episode, model):
    app = drawAction.drawAction()
    for episode in range(num_episode):
        print "\nEpisode: ", episode+1
        # Initial sate
        state = sim.reset()

        while True:
            # refresh simultor
            sim.refresh()

            # Choose action based on the state
            action = QLearning.choose_action(str(state))
            # print "action: ", action

            # take action and get next state and reward
            # Change string action to tuple
            if len(action) > 5:
                # Tuple
                format_action = literal_eval(action)
            else:
                # String
                format_action = action
            next_state, reward, done = sim.step(state, format_action)

            # Renew the q_table
            QLearning.renew_qtable(str(state), action, reward, str(next_state))
            state = next_state

            if done:
                break

        if model == "Robot":
            app.tts.say("Episode finish, please press Enter to clean the painter.")
            print "Episode finish, please press Enter to clean the painter."
            time.sleep(2)   # Have 2 seconds to press Enter Key


    # Save the q_table
    QLearning.q_table.to_pickle("q_table.pkl")
    print "Simulation finish."
    if model == "Simulator":
        print "Close the window"
        sim.destroy()




