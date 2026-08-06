from collections import deque

nodes=[]

#Initialisation des sommets
for alpha in ['a','b','c','d','e','f','g','h','i']:
    nodes.append({"value":alpha,"color":"blanc"})

#Initialisation du graphe avec les sommets et les arêtes
G={
    "S":nodes,
    "A":{('a','b'),('b','c'),
         ('c','d'),('c','f'),
         ('b','e'),('a','g'),
         ('g','h'),('h','i')}
}

#Parcours des arêtes pour la définition des successeurs
succ={node["value"]:[] for node in G["S"]}
for couple in G["A"]:
    succ[couple[0]].append(couple[1]) # par exemple, pour ('a','b'): succ['a'].append('b')


def BFS(g,so):
    #Création de la file f
    f=deque()
    #Initialisation de pi
    pi = {node["value"]: None for node in g["S"]}
    #Recherche de l'index de so dans les sommets
    so_index=next((i for i, node in enumerate(nodes) if node["value"] == so), None)
    f.append(so)
    G["S"][so_index]["color"]="gris"
    while len(f)!=0:
        sk = f[0]
        #Recherche de l'index de sk dans les sommets
        sk_index = next((i for i, node in enumerate(nodes) if node["value"] == sk), None)
        print("Node en cours: ",sk," = ",G["S"][sk_index]["color"])
        print("Successeurs: ", succ[sk])
        for si in succ[sk]:
            #Recherche de l'index de si dans les sommets
            si_index = next((i for i, node in enumerate(nodes) if node["value"] == si), None)
            #Verification du couleur de si
            if G["S"][si_index]["color"]=="blanc":
                f.append(si)
                print(si," = ",G["S"][si_index]["color"])
                G["S"][si_index]["color"]="gris"
                print(si," => ",G["S"][si_index]["color"])
                pi[si]=G["S"][sk_index]["value"]
        #Suppression de l'élément le plus vieux dans f
        f.popleft();
        G["S"][sk_index]["color"]="noir"
        print(sk," => ",G["S"][sk_index]["color"])
        print("============================================")
    return pi

pi=BFS(G,nodes[0]["value"])
print("\n\nResultats (pi): ")

for node in G["S"]:
    print(node["value"]," : ",pi[node["value"]], ", couleur: ", node["color"])