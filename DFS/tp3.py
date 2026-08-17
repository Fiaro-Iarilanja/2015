from collections import deque
from neo4j import GraphDatabase
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation


USERNAME="neo4j"
PASSWORD="passwdBFS"
URL="neo4j://127.0.0.1:7687"

try:
    driver = GraphDatabase.driver(URL,auth=(USERNAME,PASSWORD))
    driver.verify_connectivity()
    print("Connected")
except Exception as e:
    print("Error while connecting: ",e)

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
    history=[]
    so_index=next((i for i, node in enumerate(g["S"]) if node["value"] == so), None)
    g["S"][so_index]["color"]="gris"
    history.append({node["value"]:node["color"] for node in g["S"]})
    while len(p)!=0:
        si = p[len(p)-1]
        si_index=next((i for i, node in enumerate(g["S"]) if node["value"] == si), None)
        blanc=False
        for sj in succ[si]:
            sj_index=next((i for i, node in enumerate(g["S"]) if node["value"] == sj), None)
            if g["S"][sj_index]["color"]=="blanc":
                p.append(sj)
                g["S"][sj_index]["color"]="gris"
                history.append({node["value"]:node["color"] for node in g["S"]})
                pi[sj]=si
                blanc=True
        if(not blanc):       
            p.pop()
            g["S"][si_index]["color"]="noir"
            history.append({node["value"]:node["color"] for node in g["S"]})
    return pi,history

pi,history = DFS(G,'a')

for node in G["S"]:
    print(node["value"],":",pi[node["value"]])

G_nx = nx.DiGraph()
G_nx.add_nodes_from([node["value"] for node in G["S"]])
G_nx.add_edges_from(G["A"])
 
pos = nx.spring_layout(G_nx, seed=42)
 
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