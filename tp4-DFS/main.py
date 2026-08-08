from collections import deque

nodes=[]

for alpha in ['a','b','c','d','e','f','g','h']:
    nodes.append({"value":alpha,"color":"blanc"})

G={
    "S":nodes,
    "A":{('a','b'),('a','g'),
         ('b','c'),('b','e'),
         ('b','f'),('c','d'),
         ('c','e'),('d','c'),
         ('e','b'),('e','d'),
         ('e','h'),('f','a'),
         ('f','h'),('g','f'),
         ('h','e')
    }
}

succ={node["value"]:[] for node in G["S"]}
for couple in G["A"]:
    succ[couple[0]].append(couple[1])

pi={node["value"]:None for node in G["S"]}

def DFS(g,so):
    p=deque()
    p.append(so)
    so_index=next((i for i, node in enumerate(g["S"]) if node["value"] == so), None)
    g["S"][so_index]["color"]="gris"
    for sj in succ[so]:
        sj_index=next((i for i, node in enumerate(g["S"]) if node["value"] == sj), None)
        if g["S"][sj_index]["color"]=="blanc":
            pi[sj]=so
            DFS(g,sj)
    g["S"][so_index]["color"]="noir"
    return pi

pi = DFS(G,'a')

for node in G["S"]:
    print(node["value"],":",pi[node["value"]])