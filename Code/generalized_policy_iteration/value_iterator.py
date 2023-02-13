'''
Created on 29 Jan 2022

@author: ucacsjj
'''

from .dynamic_programming_base import DynamicProgrammingBase
import numpy as np
from time import sleep
from joblib import load, dump

# This class ipmlements the value iteration algorithm


class ValueIterator(DynamicProgrammingBase):

    def __init__(self, environment):
        DynamicProgrammingBase.__init__(self, environment)

        # The maximum number of times the value iteration
        # algorithm is carried out is carried out.
        self._max_optimal_value_function_iterations = 2000
        self.iterations = 0

    # Method to change the maximum number of iterations

    def set_max_optimal_value_function_iterations(self, max_optimal_value_function_iterations):
        self._max_optimal_value_function_iterations = max_optimal_value_function_iterations

    #

    def loadValue(self):
        v = load("../save/Q3/VALUEITER-values0_8")
        for x in range(self._environment.map().width()):
            for y in range(self._environment.map().height()):
                self._v.set_value(x, y, v.value(x, y))

    def saveComputed(self):
        dump(self._v, "../save/Q3/VALUEITER-values0_8")

    def solve_policy(self):

        # Initialize the drawers
        if self._policy_drawer is not None:
            self._policy_drawer.update()

        if self._value_drawer is not None:
            self._value_drawer.update()

        self._compute_optimal_value_function()

        # self.loadValue()

        self._extract_policy()

        # Draw one last time to clear any transients which might
        # draw changes
        if self._policy_drawer is not None:
            self._policy_drawer.update()

        if self._value_drawer is not None:
            self._value_drawer.update()

        self.saveComputed()

        return self._v, self._pi

    # Q3f:
    # Finish the implementation of the methods below.

    def q(self, state, action):
        # Q function, value for state action pair
        new_value = 0
        s_primes, rewards, probs = self._environment.next_state_and_reward_distribution(
            state, action)
        # if state == (59, 30):
        #     actions = ["RIGHT","UP_RIGHT","UP","UP_LEFT","LEFT","DOWN_LEFT","DOWN","DOWN_RIGHT","TERMINATE","NONE"]
        #     print("Action: ", actions[action])
        #     # print("Action val: ", action_val)
        #     # print("Best: ", best_action)
        #     # print("Best action val: ", best_action_val)
        #     print("Sprimes: ",[s.coords() for s in s_primes])
        #     print("Sprime values: ",[self._v.value(s_prime.coords()[0], s_prime.coords()[1]) for s_prime in s_primes])
        #     print("rewards: ",rewards)
        #     print("probs: ",probs)

        for s_prime, r, p in zip(s_primes, rewards, probs):
            if s_prime is None:
                # case where current state is the goal state
                new_value += r
            if s_prime is not None:
                s_prime = s_prime.coords()
                new_value += p * (r + self.gamma() *
                                  self._v.value(s_prime[0], s_prime[1]))
        # if state == (59,30):
        #     print("Action value: ",new_value)
        #     print("--------------------------")
        return new_value

    def validActionSpace(self, x, y):
        if not self._environment.map().cell(x, y).is_terminal():
            return self._environment.action_space.n - 2
        return self._environment.action_space.n

    def _compute_optimal_value_function(self):

        # This method returns no value.
        # The method updates self._pi
        steps = 0
        while True:
            delta = 0
            self.iterations += 1
            # a = set()
            for x in range(self._environment.map().width()):
                for y in range(self._environment.map().height()):
                    original_value = self._v.value(x, y)
                    # Make sure current cell has a state value (Not a wall, baggage claim, chair or toilet)
                    if not np.isnan(original_value):
                        optimalVal = -np.inf
                        for action in range(self.validActionSpace(x, y)):
                            optimalVal = max(
                                self.q((x, y), action), optimalVal)
                        self._v.set_value(x, y, optimalVal)

                        diff = abs(original_value-self._v.value(x, y))
                        delta = max(diff, delta)
                    # else:
                    #     a.add(self._environment.map().cell(x,y).cell_type())
            # print(a)

            steps += 1
            # difference = abs(original - self._v._values)
            # difference = difference[~np.isnan(difference)]
            # print(np.max(difference))
            # print(delta)
            # print("--------")
            # self._value_drawer.update()
            # sleep(0.2)

            if delta < self.theta():
                break
        print(f"Computed optimal value function in {steps} steps")

    def greedy(self, state):
        best_action = -1
        best_action_val = -np.inf
        for action in range(self.validActionSpace(state[0], state[1])):
            action_val = self.q(state, action)
            if action_val > best_action_val:
                best_action = action
                best_action_val = action_val
        return best_action

    def _extract_policy(self):

        # This method returns no value.
        # The policy is in self._pi

        for x in range(self._environment.map().width()):
            for y in range(self._environment.map().height()):
                # Take greedy action according to the evaluated value function
                if not np.isnan(self._v.value(x, y)):
                    # Again making sure current cell has a state value (Not a wall, baggage claim, chair or toilet)
                    self._pi.set_action(x, y, self.greedy((x, y)))
