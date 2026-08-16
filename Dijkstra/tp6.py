nodes=[]

for alpha in ['a','b','c','d','e']:
    nodes.append({"value":alpha,"color":"blanc"})

G={
    "S":nodes,
    "A":{('a','b'),('a','e'),
         ('b','c'),('b','e'),
         ('c','d'),('d','a'),
         ('d','c'),('e','b'),
         ('e','c'),('e','d')
    }
}

cout = {
    ('a','b'):3,('a','e'):5,
    ('b','c'):6,('b','e'):2,
    ('c','d'):2,('d','a'):3,
    ('d','c'):7,('e','b'):1,
    ('e','c'):4,('e','d'):6
}

def relacher(arc, pi, d, cout):
    si, sj = arc

    if d[sj] > d[si] + cout[(si, sj)]:
        d[sj] = d[si] + cout[(si, sj)]
        pi[sj] = si

    """
    if d[sj] < d[si] * cout[(si,sj)]:
        d[sj] = d[si] * cout[(si,sj)]
        pi[sj]=si
    """

def encoreDuGris(g):
    Gris = {node["value"] for node in g["S"] if node["color"]=="gris"}
    return Gris if len(Gris)!=0 else None

def getIndex(g,s):
    return next(i for i, node in enumerate(g["S"]) if node["value"] == s)

def Dijkstra(g,cout,so):
    d={node["value"]:float('inf') for node in g["S"]}
    pi={node["value"]:None for node in g["S"]}
    succ={node["value"]:{b for (a,b) in g["A"] if a==node["value"]} for node in g["S"]}
    d[so]=0
    so_index = getIndex(g,so)
    g["S"][so_index]["color"]="gris"
    
    while Gris:=encoreDuGris(g):
        si = min(Gris,key=lambda s:d[s])
        si_index=getIndex(g,si)
        for sj in succ[si]:
            sj_index=getIndex(g,sj)
            if g["S"][sj_index]["color"]=="blanc" or g["S"][sj_index]["color"]=="gris":
                relacher((si,sj),pi,d,cout)
                if g["S"][sj_index]["color"]=="blanc":
                    g["S"][sj_index]["color"]="gris"
        g["S"][si_index]["color"]="noir"
    return pi,d

pi, d=Dijkstra(G,cout,'a')

for node in G["S"]:
    print(node["value"],":",pi[node["value"]],d[node["value"]])