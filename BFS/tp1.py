from collections import deque
from neo4j import GraphDatabase

nodes=[]

USERNAME="neo4j"
PASSWORD="passwdBFS"
URL="neo4j://127.0.0.1:7687"

try:
    driver = GraphDatabase.driver(URL,auth=(USERNAME,PASSWORD))
    driver.verify_connectivity()
    print("Connected")
except Exception as e:
    print("Error while connecting: ",e)

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
    so_index=next((i for i, node in enumerate(g["S"]) if node["value"] == so), None)
    f.append(so)
    g["S"][so_index]["color"]="gris"
    while len(f)!=0:
        sk = f[0]
        #Recherche de l'index de sk dans les sommets
        sk_index = next((i for i, node in enumerate(g["S"]) if node["value"] == sk), None)
        print("Node en cours: ",sk," = ",g["S"][sk_index]["color"])
        print("Successeurs: ", succ[sk])
        for si in succ[sk]:
            #Recherche de l'index de si dans les sommets
            si_index = next((i for i, node in enumerate(g["S"]) if node["value"] == si), None)
            #Verification du couleur de si
            if g["S"][si_index]["color"]=="blanc":
                f.append(si)
                print(si," = ",g["S"][si_index]["color"])
                g["S"][si_index]["color"]="gris"
                print(si," => ",g["S"][si_index]["color"])
                pi[si]=g["S"][sk_index]["value"]
        #Suppression de l'élément le plus vieux dans f
        f.popleft()
        g["S"][sk_index]["color"]="noir"
        print(sk," => ",g["S"][sk_index]["color"])
        print("============================================")
    return pi

pi=BFS(G,nodes[0]["value"])
print("\n\nResultats (pi): ")

for node in G["S"]:
    print(node["value"]," : ",pi[node["value"]], ", couleur: ", node["color"])

def create_node(tx,value):
    tx.run(
        f"MERGE (s:Node {{value:$sValue}})",sValue=value
    )

def create_relationship(tx,start,end):
    tx.run(
        f"MATCH (s:Node {{value:$sValue}})"
        f"MERGE(s)-[:TO]->(e:Node {{value:$eValue}})" ,
        sValue=start,
        eValue=end
    )

def create_graph(g):
    with driver.session(database="neo4j") as session:
        session.run("MATCH (n) DETACH DELETE n")
        for node in g["S"]:
            session.execute_write(create_node,node["value"])
            for successor in succ[node["value"]]:
                session.execute_write(create_relationship,node["value"],successor)



try:
    create_graph(G)
    print("Graphe créé")
except Exception as e:
    print("Creation du graphe échouée: ",e)

driver.close()