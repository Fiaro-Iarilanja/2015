from collections import deque

nodes = []
for alpha in ['a','b','c','d','e','f','g','h']:
    nodes.append({"value": alpha, "color": "blanc"})

G = {
    "S": nodes,
    "A": {('a','b'),('a','g'),
          ('b','c'),('b','e'),
          ('b','f'),('c','d'),
          ('c','e'),('d','c'),
          ('e','b'),('e','d'),
          ('e','h'),('f','a'),
          ('f','h'),('g','f'),
          ('h','e')
    }
}

succ = {node["value"]: [] for node in G["S"]}
for couple in G["A"]:
    succ[couple[0]].append(couple[1])

pi  = {node["value"]: None for node in G["S"]}
num = {node["value"]: None for node in G["S"]}

cpt = 1

def DFSnum(g):
    global cpt
    cpt = 1
    for node in g["S"]:
        node["color"] = "blanc"
    for si in g["S"]:
        if si["color"] == "blanc":
            DFS(g, si["value"])
    return pi

def DFS(g, so):
    global cpt
    so_index = next(i for i, node in enumerate(g["S"]) if node["value"] == so)
    g["S"][so_index]["color"] = "gris"
    for sj in succ[so]:
        sj_index = next(i for i, node in enumerate(g["S"]) if node["value"] == sj)
        if g["S"][sj_index]["color"] == "gris":
            print(sj, " circuit")
        elif g["S"][sj_index]["color"] == "blanc":
            pi[sj] = so
            DFS(g, sj)
    g["S"][so_index]["color"] = "noir"
    num[so] = cpt
    cpt += 1
    return pi

DFSnum(G)

for node in G["S"]:
    print(node["value"], ":", pi[node["value"]], " cpt: ", num[node["value"]])