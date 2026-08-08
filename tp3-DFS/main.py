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

def DFS(g,so):
    p=deque()
    pi={node["value"]:None for node in g["S"]}
    p.append(so)
    so_index=next((i for i, node in enumerate(g["S"]) if node["value"] == so), None)
    g["S"][so_index]["color"]="gris"
    while len(p)!=0:
        si = p[len(p)-1]
        si_index=next((i for i, node in enumerate(g["S"]) if node["value"] == si), None)
        blanc=False
        for sj in succ[si]:
            sj_index=next((i for i, node in enumerate(g["S"]) if node["value"] == sj), None)
            if g["S"][sj_index]["color"]=="blanc":
                p.append(sj)
                g["S"][sj_index]["color"]="gris"
                pi[sj]=si
                blanc=True
        if(not blanc):       
            p.pop()
            g["S"][si_index]["color"]="noir"
    return pi

pi = DFS(G,'a')

for node in G["S"]:
    print(node["value"],":",pi[node["value"]])