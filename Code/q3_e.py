#!/usr/bin/env python3

'''
Created on 3 Feb 2022

@author: ucacsjj
'''

from common.scenarios import full_scenario

from generalized_policy_iteration.policy_iterator import PolicyIterator
from generalized_policy_iteration.value_function_drawer import ValueFunctionDrawer

from p2.low_level_environment import LowLevelEnvironment
from p2.low_level_policy_drawer import LowLevelPolicyDrawer
from joblib import dump


def setParameters(policy_solver, paramVal):
    # print("max_policy_evaluation_steps_per_iteration: ", paramVal)
    print("theta: ", paramVal)
    # policy_solver.set_max_policy_evaluation_steps_per_iteration(paramVal)
    policy_solver.set_theta(paramVal)


if __name__ == '__main__':

    # Q3e:
    # Investigate different parameters

    parameters = [1] + [i * 5 for i in range(1, 21)]
    # parameterName = "mpespiSave"

    parameters = [10e-1, 10e-2, 10e-3, 10e-4, 10e-5]
    parameterName = "thetasSave"

    results = {}

    for paramVal in parameters:
        # Get the map for the scenario
        #airport_map, drawer_height = three_row_scenario()
        airport_map, drawer_height = full_scenario()

        # Set up the environment for the robot driving around
        airport_environment = LowLevelEnvironment(airport_map)

        # Configure the process model
        # airport_environment.set_nominal_direction_probability(1)
        airport_environment.set_nominal_direction_probability(0.8)

        # Create the policy iterator
        policy_solver = PolicyIterator(
            airport_environment)
        setParameters(policy_solver, paramVal)

        # Set up initial state
        policy_solver.initialize()

        # Bind the drawer with the solver
        # policy_drawer = LowLevelPolicyDrawer(
        #     policy_solver.policy(), drawer_height)
        # policy_solver.set_policy_drawer(policy_drawer)

        # value_function_drawer = ValueFunctionDrawer(
        #     policy_solver.value_function(), drawer_height)
        # policy_solver.set_value_function_drawer(value_function_drawer)

        # Compute the solution
        v, pi = policy_solver.solve_policy()
        results[paramVal] = policy_solver.get_evaluatorRunCount()

        # # Save screen shot; this is in the current directory
        # policy_drawer.save_screenshot("policy_iteration_results.jpg")

        # # Wait for a key press
        # value_function_drawer.wait_for_key_press()
        print("-------------------------------------------------")
    dump(results, f"../save/Q3/{parameterName}")
