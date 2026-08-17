from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation

nodes = []
for alpha in ['a','b','c','d','e','f','g','h']:
    nodes.append({"value": alpha, "color": "blanc"})

G = {
    "S": nodes,
    "A": {('a','b'),('a','g'),
          ('b','c'),('b','e'),
          ('b','f'),('c','d'),
          ('c','e'),('d','c'),
          ('e','b'),('e','d'),
          ('e','h'),('f','a'),
          ('f','h'),('g','f'),
          ('h','e')
    }
}

pi  = {node["value"]: None for node in G["S"]}
steps = []

def snapshot(g):
    steps.append({node["value"]: node["color"] for node in g["S"]})

def DFSnum(g):
    global cpt
    global num
    num = {node["value"]: None for node in G["S"]}
    cpt = 1
    for node in g["S"]:
        node["color"] = "blanc"
    snapshot(g)
    for si in g["S"]:
        if si["color"] == "blanc":
            DFSrec(g, si["value"])
    return num

def DFSrec(g, so):
    global cpt
    succ = {node["value"]: [] for node in g["S"]}
    for couple in g["A"]:
        succ[couple[0]].append(couple[1])
    so_index = next(i for i, node in enumerate(g["S"]) if node["value"] == so)
    g["S"][so_index]["color"] = "gris"
    snapshot(g)
    for sj in succ[so]:
        sj_index = next(i for i, node in enumerate(g["S"]) if node["value"] == sj)
        if g["S"][sj_index]["color"] == "gris":
            print(sj, " circuit")
        elif g["S"][sj_index]["color"] == "blanc":
            pi[sj] = so
            DFSrec(g, sj)
    g["S"][so_index]["color"] = "noir"
    snapshot(g)
    num[so] = cpt
    cpt += 1

num = DFSnum(G)

for node in G["S"]:
    print(node["value"], ":", pi[node["value"]], " cpt: ", num[node["value"]])

nxG = nx.DiGraph()
nxG.add_nodes_from(node["value"] for node in G["S"])
nxG.add_edges_from(G["A"])

pos = nx.spring_layout(nxG, seed=42)

color_map = {"blanc": "white", "gris": "tab:gray", "noir": "black"}
font_color_map = {"blanc": "black", "gris": "black", "noir": "white"}

fig, ax = plt.subplots(figsize=(8, 6))

def update(frame):
    ax.clear()
    state = steps[frame]
    node_colors = [color_map[state[n]] for n in nxG.nodes()]
    nx.draw_networkx_nodes(nxG, pos, ax=ax, node_color=node_colors, edgecolors="black", node_size=900)
    nx.draw_networkx_edges(nxG, pos, ax=ax, arrows=True, arrowsize=15, connectionstyle="arc3,rad=0.08")
    for state_name, font_color in font_color_map.items():
        labels = {n: n for n in nxG.nodes() if state[n] == state_name}
        nx.draw_networkx_labels(nxG, pos, labels=labels, font_color=font_color, ax=ax)
    ax.set_title(f"Etape {frame + 1}/{len(steps)}")
    ax.axis("off")

ani = animation.FuncAnimation(fig, update, frames=len(steps), interval=800, repeat=False)
plt.show()