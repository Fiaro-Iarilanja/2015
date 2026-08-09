from tp4 import DFSnum
from tp4 import DFSrec

nodes=[]

for alpha in ['a','b','c','d','e','f','g','h','i']:
    nodes.append({"value":alpha,"color":"blanc"})

G={
    "S":nodes,
    "A":{('a','b'),('a','d'),
         ('b','a'),('c','a'),
         ('c','h'),('d','b'),
         ('d','c'),('d','g'),
         ('f','g'),('f','i'),
         ('g','h'),('h','g'),
         ('h','e'),('i','e'),
         ('i','f'),('i','h')
    }
}

pi  = {node["value"]: None for node in G["S"]}

def sortNum(num):
    return dict(sorted(num.items(), key=lambda item: item[1], reverse=True))

def SCC(g):
    scc = []
    num=DFSnum(g)
    order = sortNum(num)

    Gt = {
        "S": g["S"],
        "A": {(b, a) for (a, b) in g["A"]}
    }
    for node in Gt["S"]:
        node["color"] = "blanc"
    for si in order:
        si_index = next(i for i, node in enumerate(Gt["S"]) if node["value"] == si)
        if Gt["S"][si_index]["color"] == "blanc":
            Blanc = {node["value"] for node in Gt["S"] if node["color"] == "blanc"}
            DFSrec(Gt, si)
            nouveau_noir = {node["value"] for node in Gt["S"] if node["color"] == "noir"}
            scc.append(Blanc & nouveau_noir)

    return scc

print("SCC: ")

scc=SCC(G)

for s in scc:
    print(s)