'''
Created on 29 Jan 2022

@author: ucacsjj
'''

from .dynamic_programming_base import DynamicProgrammingBase

# This class ipmlements the value iteration algorithm


class ValueIterator(DynamicProgrammingBase):

    def __init__(self, environment):
        DynamicProgrammingBase.__init__(self, environment)

        # The maximum number of times the value iteration
        # algorithm is carried out is carried out.
        self._max_optimal_value_function_iterations = 2000

    # Method to change the maximum number of iterations
    def set_max_optimal_value_function_iterations(self, max_optimal_value_function_iterations):
        self._max_optimal_value_function_iterations = max_optimal_value_function_iterations

    #
    def solve_policy(self):

        # Initialize the drawers
        if self._policy_drawer is not None:
            self._policy_drawer.update()

        if self._value_drawer is not None:
            self._value_drawer.update()

        self._compute_optimal_value_function()

        self._extract_policy()

        # Draw one last time to clear any transients which might
        # draw changes
        if self._policy_drawer is not None:
            self._policy_drawer.update()

        if self._value_drawer is not None:
            self._value_drawer.update()

        return self._v, self._pi

    # Q3f:
    # Finish the implementation of the methods below.
    def _compute_optimal_value_function(self):

        # This method returns no value.
        # The method updates self._pi

        # while True:
        #     delta = 0
        #     for state in range(self.state_space): #Need mod
        #         original_value = self._v.value() # Need mod
        #         # Asynchronously update the value function
        #         for action in range(self._environment.action_space): # Need mod
        #             self.value[state] = max(self.bellman(
        #                 state, action), self.value[state])
        #         delta = max(abs(original_value-self.value[state]), delta)
        #     if delta < self._theta:
        #         # Reached desired accuracy
        #         break

        raise NotImplementedError()

    def _extract_policy(self):

        # This method returns no value.
        # The policy is in self._pi

        # for state in range(self.state_space): # Need mod
        #     # Take greedy action according to the evaluated value function
        #     self.policy.set_action(x, y, self.greedy(state))
        raise NotImplementedError()

    def q(self, state, action):
        # Bellman optimality equation
        dynamics = self.env.P[state][action]
        new_value = 0
        for next_step in dynamics:
            probability, nextstate, reward, done = next_step
            new_value += probability * \
                (reward + self.discount * self.value[nextstate])
        return new_value

    def greedy(self, state):
        best_action = -1
        best_action_val = -np.inf
        for action in range(self._environment.action_space):
            action_val = self.q(state, action)
            if action_val > best_action_val:
                best_action = action
                best_action_val = action_val
        return best_action
