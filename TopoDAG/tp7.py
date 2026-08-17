G = {
    "S": {'a','b','c','d','e','f','g','h'},
    "A": { ('b','a'),('b','g'),
           ('c','b'),('d','c'),
           ('d','e'),('d','f'),
           ('e','f'),('f','b'),
           ('f','c'),('g','a'),
           ('g','h'),('h','a')
        }
}

color={node:"blanc" for node in G["S"]}

cout={
    ('b','a'):9,('b','g'):3,
    ('c','b'):4,('d','c'):8,
    ('d','e'):3,('d','f'):4,
    ('e','f'):4,('f','b'):1,
    ('f','c'):2,('g','a'):2,
    ('g','h'):4,('h','a'):1
}

succ={a:[] for a in G["S"]}

for (a,b) in G["A"]:
    succ[a].append(b)

def relacher(arc, pi, d, cout):
    si, sj = arc

    if d[sj] > d[si] + cout[(si, sj)]:
        d[sj] = d[si] + cout[(si, sj)]
        pi[sj] = si

BLANC, GRIS, NOIR = 0, 1, 2

def sortNode(g):
    adj = succ
    couleur = {s: BLANC for s in g["S"]}
    pi = {s: None for s in g["S"]}
    date_debut = {}
    date_fin = {}
    ordre = []
    temps = [0]

    def visiter(u):
        couleur[u] = GRIS
        temps[0] += 1
        date_debut[u] = temps[0]

        for v in adj[u]:
            if couleur[v] == BLANC:
                pi[v] = u
                visiter(v)
            elif couleur[v] == GRIS:
                raise ValueError(f"Cycle detected (edge {u} -> {v}), no topological sort exists")

        couleur[u] = NOIR
        temps[0] += 1
        date_fin[u] = temps[0]
        ordre.append(u)

    for s in g["S"]:
        if couleur[s] == BLANC:
            visiter(s)

    ordre.reverse()
    return ordre

def TopoDAG(g,cout,so):
    d={node:float('inf') for node in g["S"]}
    pi={node:None for node in g["S"]}
    d[so]=0
    S=sortNode(g)
    for si in S:
        for sj in succ[si]:
            relacher((si,sj),pi,d,cout)
    return pi,d

pi,d=TopoDAG(G,cout,'d')

for n in G["S"]:
    print(n,pi[n],d[n])