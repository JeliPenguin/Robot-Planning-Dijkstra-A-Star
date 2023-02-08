from joblib import load
from matplotlib import pyplot as plt
import math

def showStat():
    parameters = "thetasSave"
    # parameters = "mpespiSave"
    res = load(f"../save/Q3/{parameters}")
    y = []
    x = []

    print(res)
    for a, b in res.items():
        y.append(a)
        x.append(b)

    plt.plot(y, x)
    plt.xlabel("Thetas")
    plt.xscale("log")
    plt.ylabel("Number of times Policy Evaluator is ran")
    plt.show()


p = load("policy")
print(p)