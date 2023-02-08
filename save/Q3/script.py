from joblib import dump, load

r1 = load("gammaSave")
r2 = load("gammaSaveNew")

new = {}

for a, b in r1.items():
    new[a] = b

for a, b in r2.items():
    new[a] = b

dump(new, "gammaSave")
print(new)
