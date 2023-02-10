from joblib import load, dump
from matplotlib import pyplot as plt
import math


def showStat():
    # parameters = "thetasSave"
    parameters = "gammaSave"
    # parameters = "mpespiSave"
    res = load(f"../save/Q3/{parameters}")
    print(res)
    y = []
    x = []

    for a, b in res.items():
        y.append(a)
        x.append(b)

    plt.plot(y, x)
    plt.xlabel("Gamma")
    # plt.xscale("log")
    plt.ylabel("Number of times Policy Evaluator is ran")
    plt.show()


# p = load("policy")
# print(p)

showStat()
