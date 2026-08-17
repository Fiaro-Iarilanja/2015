G = {
    "S": {'a','b','c','d','e','f'},
    "A": { ('a','b'),('a','c'),
           ('b','d'),('d','a'),
           ('c','e'),('e','f'),
           ('d','e')
        }
}

color={node:"blanc" for node in G["S"]}

cout={
    ('a','b'):1,('a','c'):1,
    ('b','d'):4,('d','a'):2,
    ('c','e'):1,('e','f'):1,
    ('d','e'):-4
}

succ={a:[] for a in G["S"]}

for (a,b) in G["A"]:
    succ[a].append(b)

def relacher(arc, pi, d, cout):
    si, sj = arc

    if d[sj] > d[si] + cout[(si, sj)]:
        d[sj] = d[si] + cout[(si, sj)]
        pi[sj] = si

def Bellman_Ford(g,cout,so):
    d={node:float('inf') for node in g["S"]}
    pi={node:None for node in g["S"]}
    d[so]=0

    for k in range(1,len(g["S"])-1):
        for (si,sj) in g["A"]:
            relacher((si,sj),pi,d,cout)

    for (si,sj) in g["A"]:
        if(d[sj]>d[si]+cout[(si,sj)]):
            print("Le graphe contient un circuit absorbant")

    return pi,d

pi,d=Bellman_Ford(G,cout,'a')

for n in G["S"]:
    print(n,pi[n],d[n])