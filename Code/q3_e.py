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
from joblib import dump, load


def setParameters(policy_solver, crtParam, paramVal):

    if crtParam == "MPESPI":
        policy_solver.set_max_policy_evaluation_steps_per_iteration(paramVal)
    elif crtParam == "THETA":
        policy_solver.set_theta(paramVal)
    elif crtParam == "GAMMA":
        policy_solver.set_gamma(paramVal)


if __name__ == '__main__':

    # Q3e:
    # Investigate different parameters

    repetitions = 5

    parametersToTest = {
        "MPESPI": [[1] + [i * 5 for i in range(1, 21)], "mpespiSave"],
        "THETA": [[1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 2, 4, 6, 8, 10, 12, 14, 16], "thetasSave"],
        "GAMMA": [[0.01 * i for i in range(80, 101)], "gammaSave"]
    }

    currentParameter = "THETA"
    parameters = parametersToTest[currentParameter][0]
    saveName = parametersToTest[currentParameter][1]

    results = {}

    for paramVal in parameters:
        count = 0
        print(f"{currentParameter} value: {paramVal}")
        for _ in range(repetitions):

            # Get the map for the scenario
            airport_map, drawer_height = full_scenario()

            # Set up the environment for the robot driving around
            airport_environment = LowLevelEnvironment(airport_map)

            # Configure the process model
            airport_environment.set_nominal_direction_probability(0.8)

            # Create the policy iterator
            policy_solver = PolicyIterator(
                airport_environment, interRender=True)
            setParameters(policy_solver, currentParameter, paramVal)

            # Set up initial state
            policy_solver.initialize()

            # # Bind the drawer with the solver
            # policy_drawer = LowLevelPolicyDrawer(
            #     policy_solver.policy(), drawer_height)
            # policy_solver.set_policy_drawer(policy_drawer)

            # value_function_drawer = ValueFunctionDrawer(
            #     policy_solver.value_function(), drawer_height)
            # policy_solver.set_value_function_drawer(value_function_drawer)

            # Compute the solution
            v, pi = policy_solver.solve_policy()
            # p = load("../save/Q3/stdPolicy")
            # print("Matching policy: ", p._policy == pi._policy)

            count += policy_solver.get_evaluatorRunCount()

            # Save screen shot; this is in the current directory
            # policy_drawer.save_screenshot("policy_iteration_policy_gamma0_975.pdf")
            # value_function_drawer.save_screenshot(
            #     "policy_iteration_value_gamma0_975.pdf")

            # # Wait for a key press
            # value_function_drawer.wait_for_key_press()

        results[paramVal] = count / repetitions
        print("-------------------------------------------------")
    dump(results, f"../save/Q3/{saveName}")
    input()
