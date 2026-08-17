class UnionFind:
    def __init__(self, sommets):
        self.parent = {s: s for s in sommets}
        self.rang = {s: 0 for s in sommets}
 
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
 
    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
 
        # Union par rang
        if self.rang[rx] < self.rang[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rang[rx] == self.rang[ry]:
            self.rang[rx] += 1
        return True
 
 
def kruskal(S, A):
    uf = UnionFind(S)
    arbre = []
    poids_total = 0
 
    aretes_triees = sorted(A, key=lambda e: e[2])
 
    for u, v, poids in aretes_triees:
        if uf.union(u, v):
            arbre.append((u, v, poids))
            poids_total += poids
            if len(arbre) == len(list(S)) - 1:
                break
 
    return arbre, poids_total
 
 
if __name__ == "__main__":
    S = {"A", "B", "C", "D", "E", "F"}
 
    A = {
        ("A", "B", 4),
        ("A", "F", 2),
        ("B", "C", 6),
        ("B", "F", 5),
        ("C", "D", 3),
        ("C", "F", 1),
        ("D", "E", 2),
        ("E", "F", 4),
    }
 
    arbre, poids_total = kruskal(S, A)
 
    print("Arêtes de l'ACPM :")
    for u, v, poids in arbre:
        print(f"  {u} - {v} (poids {poids})")
    print(f"Poids total de l'arbre : {poids_total}")