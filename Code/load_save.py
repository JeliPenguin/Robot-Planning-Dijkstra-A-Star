from joblib import load


algs = ["dfs", "bfs", "dijk", "dijkT", "astar"]
alg = algs[2]
path = f"../save/{alg}/"
total_cell_visted = load(path+"total_cell_visted")
total_travel_cost = load(path+"total_travel_cost")

print("Total cell visited: ", total_cell_visted)
print("Total travel cost: ", total_travel_cost)
