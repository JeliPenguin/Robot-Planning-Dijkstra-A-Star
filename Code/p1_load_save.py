from joblib import load


def showStats(alg):
    print("-"*100)
    comparedAlg = [alg, "bfs", "dfs", alg+"T", "bfsT", "dfsT"]
    metrics = ["total_cell_visted", "total_travel_cost"]
    summary(comparedAlg, metrics)
    # for alg in algorithmNames:
    #     for cAlg in comparedAlg:
    #         print(f"{alg} vs {cAlg} comparison:")
    #         compare(alg, cAlg, "total_cell_visted")
    #         compare(alg, cAlg, "total_travel_cost")
    #         print("-"*100+"\n")
    print("-"*100)


def compareAD():
    metrics = ["total_cell_visted", "total_travel_cost"]
    for m in metrics:
        compare("dijkT", "astarT", m)


def summary(algs, metrics):
    for m in metrics:
        print("\nEvaluating "+m)
        for a in algs:
            path = f"../save/{a}/"
            costs = load(path+m)
            print(f"{a}: {sum(costs)}")


def compare(alg1, alg2, metric):
    print("\nEvaluating: "+metric)
    path1 = f"../save/{alg1}/"
    cost1 = load(path1+metric)
    path2 = f"../save/{alg2}/"
    cost2 = load(path2+metric)
    print(metric+" sums:")
    print(f"{alg1} sum: ", round(sum(cost1), 2))
    print(f"{alg2} sum: ", round(sum(cost2), 2))
    print("\n")
    for i in range(len(cost1)):
        t1 = round(cost1[i], 2)
        t2 = round(cost2[i], 2)
        if t1 != t2:
            if t1 > t2:
                maxAlg = alg1
            elif t2 > t1:
                maxAlg = alg2

            print(f"{maxAlg} has greater {metric} of: {max(t1,t2)} for bin {i+1}")


# algorithmNames = ["dijk", "dijkT", "astar"]
# algorithmName = "astar"
# showStats(algorithmName)
compareAD()
