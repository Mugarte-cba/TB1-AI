import graphviz as gv

class DisjointSet:
    def __init__(self, n):
        self.id = [-1]*n

    def find(self, a):
        if self.id[a] >= 0:
            grandpa = self.find(self.id[a])
            self.id[a] = grandpa
            return grandpa

        return a

    def union(self, a, b):
        parentA = self.find(a)
        parentB = self.find(b)
        if parentA == parentB:
            return

        if -self.id[parentA] < -self.id[parentB]:
            self.id[parentB] += self.id[parentA]
            self.id[parentA] = parentB
        else:
            self.id[parentA] += self.id[parentB]
            self.id[parentB] = parentA

import heapq

def kruskal(G):
    n = len(G)
    Gprima = [[] for _ in range(n)]
    ds = DisjointSet(n)
    edges = []
    for u in range(n):
        for v, w in G[u]:
            heapq.heappush(edges, (w, u, v))

    numEdges = 0
    while numEdges < n-1:
        w, u, v = heapq.heappop(edges)
        if ds.find(u) != ds.find(v):
            ds.union(u, v)
            Gprima[u].append((v, w))
            Gprima[v].append((u, w))
            numEdges += 1

    return Gprima

def drawAL(G):
    dot = gv.Graph(comment='', strict=True)
    n = len(G)
    names=["Magdalena","San_Isidro","Cercado_de_Lima","Breña","Miraflores","San_Miguel"]
    for u in range(n):
        dot.node(str(u), names[u])

    for u in range(n):
        for v, w in G[u]:
            dot.edge(str(u), str(v), label=str(w))

    dot.graph_attr['rankdir'] = 'BT'
    return dot
#0=Magdalena
#1=San_Isidro
#2=Cercado_de_Lima
#3=Breña
#4=Miraflores
#5=San_Miguel
G = [
    [(1,2451), (2,713), (3,1018), (4,1631)],
    [(0,2451),(2,1745), (3,1524), (4,831)],
    [(0,713), (1,1745), (3,355), (4,920)],
    [(0,1018), (1,1524), (2,355), (4,700)],
    [(0,1631), (1,831), (2,920), (3,700)]
    ]
G2= [
    [(1,130), (2,160), (3,210), (4,402)],
    [(0,125),(2,190), (3,150), (4,201)],
    [(0,135), (1,186), (3,340), (4,320)],
    [(0,145), (1,195), (2,231), (4,154)],
    [(0,178), (1,245), (2,235), (3,322)]
    ]
drawAL(G)