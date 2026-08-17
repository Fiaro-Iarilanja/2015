import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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
    history=[]
    so_index = getIndex(g,so)
    g["S"][so_index]["color"]="gris"
    history.append({node["value"]:{"color":node["color"],"dist":d[node["value"]]} for node in g["S"]})
    while Gris:=encoreDuGris(g):
        si = min(Gris,key=lambda s:d[s])
        si_index=getIndex(g,si)
        for sj in succ[si]:
            sj_index=getIndex(g,sj)
            if g["S"][sj_index]["color"]=="blanc" or g["S"][sj_index]["color"]=="gris":
                relacher((si,sj),pi,d,cout)
                if g["S"][sj_index]["color"]=="blanc":
                    g["S"][sj_index]["color"]="gris"
                history.append({node["value"]:{"color":node["color"],"dist":d[node["value"]]} for node in g["S"]})
        g["S"][si_index]["color"]="noir"
        history.append({node["value"]:{"color":node["color"],"dist":d[node["value"]]} for node in g["S"]})
    return pi,d,history

pi, d,history=Dijkstra(G,cout,'a')

for node in G["S"]:
    print(node["value"],":",pi[node["value"]],d[node["value"]])

G_nx = nx.DiGraph()
G_nx.add_nodes_from([node["value"] for node in G["S"]])
G_nx.add_edges_from(G["A"])
 
pos = nx.spring_layout(G_nx, seed=7)
 
color_map = {"blanc":"white", "gris":"#f4a261", "noir":"#264653"}
 
def format_label(v, dist):
    d_str = "inf" if dist == float('inf') else str(dist)
    return f"{v} ({d_str})"
 
fig, ax = plt.subplots(figsize=(7,6))
 
def update(frame):
    ax.clear()
    snapshot = history[frame]
    colors = [color_map[snapshot[n]["color"]] for n in G_nx.nodes()]
    labels = {n: format_label(n, snapshot[n]["dist"]) for n in G_nx.nodes()}
    nx.draw(
        G_nx, pos, ax=ax, labels=labels,
        node_color=colors, edgecolors="black", linewidths=1.5,
        node_size=1600, font_size=9, font_weight="bold",
        arrows=True, arrowsize=15
    )
    nx.draw_networkx_edge_labels(G_nx, pos, edge_labels=cout, ax=ax, font_size=9)
    ax.set_title(f"Dijkstra - étape {frame+1}/{len(history)}")
 
ani = animation.FuncAnimation(
    fig, update, frames=len(history), interval=900, repeat=False
)
 
plt.show()
 