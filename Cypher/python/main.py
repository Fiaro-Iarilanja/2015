import random
from neo4j import GraphDatabase


def generer_graphe_aleatoire(nb_noeuds, prefixe, proba_arete=0.15):
    noeuds = [f"{prefixe}{i}" for i in range(nb_noeuds)]
    aretes = set()
    for i in range(nb_noeuds):
        for j in range(i + 1, nb_noeuds):
            if random.random() < proba_arete:
                aretes.add((noeuds[i], noeuds[j]))
    return noeuds, aretes


def construire_liste_adjacence(noeuds, aretes):
    adj = {n: [] for n in noeuds}
    for (u, v) in aretes:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def composantes_connexes(noeuds, aretes):
    adj = construire_liste_adjacence(noeuds, aretes)
    couleur = {n: "blanc" for n in noeuds}
    composantes = []

    for depart in noeuds:
        if couleur[depart] == "blanc":
            composante = []
            file_attente = [depart]
            couleur[depart] = "gris"
            while file_attente:
                u = file_attente.pop(0)
                composante.append(u)
                for v in adj[u]:
                    if couleur[v] == "blanc":
                        couleur[v] = "gris"
                        file_attente.append(v)
                couleur[u] = "noir"
            composantes.append(composante)

    return composantes


def noeuds_atteignables(depart, noeuds, aretes):
    adj = construire_liste_adjacence(noeuds, aretes)
    couleur = {n: "blanc" for n in noeuds}
    file_attente = [depart]
    couleur[depart] = "gris"
    atteints = {depart}
    while file_attente:
        u = file_attente.pop(0)
        for v in adj[u]:
            if couleur[v] == "blanc":
                couleur[v] = "gris"
                atteints.add(v)
                file_attente.append(v)
        couleur[u] = "noir"
    return atteints


def connecter_composantes(composantes, aretes):
    for i in range(len(composantes) - 1):
        u = random.choice(composantes[i])
        v = random.choice(composantes[i + 1])
        aretes.add((u, v))
    return aretes


def rendre_connexe(noeuds, aretes):
    composantes = composantes_connexes(noeuds, aretes)
    if len(composantes) > 1:
        aretes = connecter_composantes(composantes, aretes)
    return aretes



def connecter_deux_graphes(noeuds1, noeuds2, aretes_globales):
    u = random.choice(noeuds1)
    v = random.choice(noeuds2)
    aretes_globales.add((u, v))
    return aretes_globales


def est_connexe(noeuds, aretes):
    return len(composantes_connexes(noeuds, aretes)) == 1


def verifier_tous_les_noeuds(noeuds, aretes):
    for depart in noeuds:
        atteints = noeuds_atteignables(depart, noeuds, aretes)
        if len(atteints) != len(noeuds):
            manquants = set(noeuds) - atteints
            print(f"  ! Depuis {depart}, noeuds NON atteignables : {manquants}")
            return False
    return True


def vider_base(driver):
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")


def creer_noeuds(driver, noeuds, label):
    with driver.session() as session:
        for n in noeuds:
            session.run(
                f"MERGE (n:{label} {{nom: $nom}})",
                nom=n
            )


def creer_aretes(driver, aretes):
    with driver.session() as session:
        for (u, v) in aretes:
            session.run(
                """
                MATCH (a {nom: $u}), (b {nom: $v})
                MERGE (a)-[:RELIE]->(b)
                MERGE (b)-[:RELIE]->(a)
                """,
                u=u, v=v
            )



if __name__ == "__main__":
    random.seed()  

    NB_NOEUDS_G1 = 30
    NB_NOEUDS_G2 = 30

    noeuds1, aretes1 = generer_graphe_aleatoire(NB_NOEUDS_G1, prefixe="cNoeud", proba_arete=0.15)
    print("G1 - composantes avant correction :", composantes_connexes(noeuds1, aretes1))
    aretes1 = rendre_connexe(noeuds1, aretes1)
    print("G1 connexe ?", est_connexe(noeuds1, aretes1))

    noeuds2, aretes2 = generer_graphe_aleatoire(NB_NOEUDS_G2, prefixe="Noeud", proba_arete=0.1)
    print("G2 - composantes avant correction :", composantes_connexes(noeuds2, aretes2))
    aretes2 = rendre_connexe(noeuds2, aretes2)
    print("G2 connexe ?", est_connexe(noeuds2, aretes2))

    noeuds_total = noeuds1 + noeuds2
    aretes_total = aretes1 | aretes2
    aretes_total = connecter_deux_graphes(noeuds1, noeuds2, aretes_total)

    print("\nGraphe global (G1 + G2) connexe ?", est_connexe(noeuds_total, aretes_total))
    print("Vérification noeud par noeud (tout noeud -> tout noeud) :",
          verifier_tous_les_noeuds(noeuds_total, aretes_total))

    try:
        driver = GraphDatabase.driver(
            "neo4j://127.0.0.1:7687", auth=("neo4j", "neo4j@password")
        )
        driver.verify_connectivity()
        print("Connected")
    except Exception as e:
        print("Erreur de connection:",e)
        exit(-1)
        
    vider_base(driver)
    creer_noeuds(driver, noeuds1, label="cNoeud")
    creer_noeuds(driver, noeuds2, label="Noeud")
    creer_aretes(driver, aretes_total)
    driver.close()

    print("\nGraphe envoyé dans Neo4j.")
    print("MATCH (n:cNoeud) RETURN n  -> noeuds du graphe 1 (connexe dès le départ)")
    print("MATCH (n:Noeud) RETURN n   -> noeuds du graphe 2")