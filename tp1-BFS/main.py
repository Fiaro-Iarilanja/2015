from collections import deque

nodes=[]

for alpha in ['a','b','c','d','e','f','g','h','i']:
    nodes.append({"value":alpha,"color":"blanc"})
G={
    "S":nodes,
    "A":{('a','b'),('b','c'),
         ('c','d'),('c','f'),
         ('b','e'),('a','g'),
         ('g','h'),('h','i')}
}


succ={node["value"]:[] for node in G["S"]}
for couple in G["A"]:
    succ[couple[0]].append(couple[1])

def BFS(g,so):
    f=deque()
    pi = {node["value"]: None for node in g["S"]}

    f.append(so["value"])
    while len(f)!=0:
        sk = f[0]
        sk_index = next((i for i, node in enumerate(nodes) if node["value"] == sk), None)
        for si in succ[sk]:
            si_index = next((i for i, node in enumerate(nodes) if node["value"] == si), None)
            if G["S"][si_index]["color"]=="blanc":
                f.append(si)
                G["S"][si_index]["color"]="gris"
                pi[si]=G["S"][sk_index]["value"]
        f.popleft();
        G["S"][sk_index]["color"]="noir"
    return pi

pi=BFS(G,nodes[0])

for node in G["S"]:
    print(node["value"]," : ",pi[node["value"]])