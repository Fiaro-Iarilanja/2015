from collections import deque
from neo4j  import GraphDatabase

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

for alpha in ['a','b','c','d','e','f','g','h','i']:
    nodes.append({"value":alpha,"color":"blanc"})

G={
    "S":nodes,
    "A":{('a','b'),('b','c'),
         ('c','d'),('c','f'),
         ('b','e'),('a','g'),
         ('g','h'),('h','i')}
}

succ={node["value"]:[] for node in G["S"]}
for couple in G["A"]:
    succ[couple[0]].append(couple[1]) 

def plusCourtChemin(so,sj,pi):
    if so == sj:
        print(so, end=" ")
    elif pi[sj] == None:
        print(f"Il n'y a pas de chemin de {so} jusque {sj}")
    else:
        plusCourtChemin(so,pi[sj],pi)
        print(f"=> {sj}",end=" ")

def calculDistance(g,so):
    f=deque()
    pi = { node["value"]:None for node in g["S"] }
    d = { node["value"]:float('inf') for node in g["S"] }

    f.append(so)
    d[so] = 0
    while len(f)!=0:
        sk=f[0]
        sk_index = next((i for i, node in enumerate(g["S"]) if node["value"] == sk), None)
        for si in succ[sk]:
            si_index = next((i for i, node in enumerate(nodes) if node["value"] == si), None)
            if g["S"][si_index]["color"]=="blanc":
                f.append(si)
                g["S"][si_index]["color"]="gris"
                d[si]=d[sk]+1
                pi[si]=sk
        f.popleft()
        g["S"][sk_index]["color"]="noir"

    print("Plus court chemin de a vers i:",end=" ")
    plusCourtChemin('a','i',pi)
    print("")
    return d

d = calculDistance(G,'a')

for node in G["S"]:
    print(node["value"],":",d[node["value"]])

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