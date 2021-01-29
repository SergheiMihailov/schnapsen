"""
RandomBot -- A simple strategy: enumerates all legal moves, and picks one
uniformly at random.
"""

# Import the API objects
from api import State
import random
import pickle
import os
import copy

from api import util

BOT_NAMES = ['rand', 'bully', 'rdeep', 'ml']
IS_TRAINING = True

class Bot:

    prob_select_best = 0.5
    discount_rate = 0.9
    learning_rate = 0.001
    score_weight = 0.005
    features_shape = (2, 3, 3)
    win_reward = 10

    policy_filename = os.path.realpath('bots/selection_reinforcement/selection_reinforcement_model.pkl') 
    
    # Load policy

    def init_policy(self):
        self.Q = [[
            [[0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 0, 0, 0], [0, 0, 0, 0]],
        ],[
            [[0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 0, 0, 0], [0, 0, 0, 0]],
        ],[
            [[0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 0, 0, 0], [0, 0, 0, 0]],
        ]]
        policy_file_write = open(self.policy_filename, 'w')
        policy_file_write.write(pickle.dumps(self.Q))
        policy_file_write.close()


    def __init__(self):
        try:
            policy_file_read = open(self.policy_filename, 'r')
            self.Q = pickle.load(policy_file_read)
            policy_file_read.close()
            # if self.Q == None:
            #     self.init_policy()    
        except:
            self.init_policy()  
            print('An error happened while loading the policy')
      
    def get_q_for_reduced_state(self, reduced_state):
        return self.Q[reduced_state[0]][reduced_state[1]][reduced_state[2]]

    def select_bot(self, reduced_state): 
        if random.random() > self.prob_select_best:
            return random.choice(BOT_NAMES)
        
        q_in_this_state = self.get_q_for_reduced_state(reduced_state)

        value_best_bot = max(q_in_this_state)
        best_bot_index = q_in_this_state.index(value_best_bot)

        bot_to_use_name = BOT_NAMES[best_bot_index]
        return bot_to_use_name 
  
    def adjust_value(self, state, state2, reward, bot_index, bot_index2): 
        print(reward)
        predicted_value = self.get_q_for_reduced_state(state)[bot_index] 
        actual_value = reward + self.discount_rate * self.get_q_for_reduced_state(state2)[bot_index2]
        updated_value = self.get_q_for_reduced_state(state)[bot_index] + self.learning_rate * (actual_value - predicted_value) 
        
        print(predicted_value, actual_value, updated_value)
        self.Q[state[0]][state[1]][state[2]][bot_index] = updated_value

    def reduce_state(self, state, notMyTurn=False):
        reduced_state = [0]*3
        # Time limit feature
        reduced_state[0] = 0 if state.get_max_time() < 10 else 1 if state.get_max_time() < 25 else 2

        # Score difference feature 
        score_diff = state.get_points(state.whose_turn()-1) - state.get_points(state.whose_turn() % 2)
        if notMyTurn:
            score_diff = -score_diff
        reduced_state[1] = 0 if score_diff < -3  else 2 if score_diff > 3 else 0
        # Cards left in stock feature
        reduced_state[2] = 1 if state.get_stock_size() >= 2 else 0

        return reduced_state

    def get_move(self, state):
        # type: (State) -> tuple[int, int]
        policy_file_read = open(self.policy_filename, 'r')
        self.Q = pickle.load(policy_file_read)
        policy_file_read.close()
        
        reduced_state = self.reduce_state(state)

        bot_to_use_name = self.select_bot(reduced_state)
        
        bot_to_use = util.load_player(bot_to_use_name)

        if IS_TRAINING:
            next_state = state.next(bot_to_use.get_move(state))
            next_state_reduced = self.reduce_state(next_state, notMyTurn=True)
            
            score_diff = state.get_points(state.whose_turn()-1) - state.get_points(state.whose_turn() % 2)
            
            reward = score_diff * self.score_weight + (self.win_reward if next_state.winner()[0] == state.whose_turn() else 0)
            
            next_bot_to_use_name = self.select_bot(next_state_reduced)
            self.adjust_value(reduced_state, next_state_reduced, reward, BOT_NAMES.index(bot_to_use_name), BOT_NAMES.index(next_bot_to_use_name))
            
            policy_file_write = open(self.policy_filename, 'w')
            policy_file_write.write(pickle.dumps(self.Q))
            policy_file_write.close()

        # Return a random choice
        return bot_to_use.get_move(state)