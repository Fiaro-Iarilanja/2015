from collections import deque
from neo4j import GraphDatabase
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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
    history=[]
    #Recherche de l'index de so dans les sommets
    so_index=next((i for i, node in enumerate(g["S"]) if node["value"] == so), None)
    f.append(so)
    g["S"][so_index]["color"]="gris"
    history.append({node["value"]:node["color"] for node in g["S"]})
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
                history.append({node["value"]:node["color"] for node in g["S"]})
        #Suppression de l'élément le plus vieux dans f
        f.popleft()
        g["S"][sk_index]["color"]="noir"
        history.append({node["value"]:node["color"] for node in g["S"]})
        print(sk," => ",g["S"][sk_index]["color"])
        print("============================================")
    return pi,history

pi,history=BFS(G,nodes[0]["value"])
print("\n\nResultats (pi): ")

for node in G["S"]:
    print(node["value"]," : ",pi[node["value"]], ", couleur: ", node["color"])

#Construction du graphe networkx à partir des mêmes sommets/arêtes
G_nx = nx.DiGraph()
G_nx.add_nodes_from([node["value"] for node in G["S"]])
G_nx.add_edges_from(G["A"])
 
#Layout fixe (seed) pour que les sommets ne bougent pas d'une frame à l'autre
pos = nx.spring_layout(G_nx, seed=42)
 
#Correspondance couleur "métier" -> couleur matplotlib
color_map = {"blanc":"white", "gris":"#f4a261", "noir":"#264653"}
 
fig, ax = plt.subplots(figsize=(7,6))
 
def update(frame):
    ax.clear()
    snapshot = history[frame]
    colors = [color_map[snapshot[n]] for n in G_nx.nodes()]
    nx.draw(
        G_nx, pos, ax=ax, with_labels=True,
        node_color=colors, edgecolors="black", linewidths=1.5,
        node_size=900, font_size=12, font_weight="bold",
        arrows=True, arrowsize=15
    )
    ax.set_title(f"BFS - étape {frame+1}/{len(history)}")
 
ani = animation.FuncAnimation(
    fig, update, frames=len(history), interval=800, repeat=False
)
 
plt.show()


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