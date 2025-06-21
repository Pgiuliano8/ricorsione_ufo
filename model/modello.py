import copy

from database.DAO import DAO
import networkx as nx

class Model:

    def __init__(self):
        self._graph = nx.DiGraph()

        self.bestPath = []
        self.bestScore = 0

    def buildGraph(self, year, shape):
        nodes = DAO.getNodes(year, shape)
        self._graph.add_nodes_from(nodes)
        for u in nodes:
            for v in nodes:
                if u!=v and u.state==v.state:
                    if u.longitude < v.longitude:
                        self._graph.add_edge(u, v, weight=v.longitude - u.longitude)
                    elif u.longitude > v.longitude:
                        self._graph.add_edge(v, u, weight=u.longitude - v.longitude)

    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getBestEdges(self):
        edges = sorted(self._graph.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)
        return edges[0:5]


    def getYears(self):
        return DAO.getYears()

    def getShapes(self, anno):
        return DAO.getShapes(anno)

    def cammino_ottimo(self):
        self.bestPath = []
        self.bestScore = 0

        for n in self._graph.nodes():
            parziale = [n]
            self.ricorsione(parziale)
            parziale.pop()
        return self.bestPath, self.bestScore

    def ricorsione(self, parziale):
        rimanenti = self.calcola_rimanenti(parziale)

        if len(rimanenti) == 0:
            if self.calcola_score(parziale) > self.bestScore:
                self.bestScore = self.calcola_score(parziale)
                self.bestPath = copy.deepcopy(parziale)
        else:
            for r in rimanenti:
                parziale.append(r)
                self.ricorsione(parziale)
                parziale.pop()

    def calcola_rimanenti(self, parziale):
        rimanenti = []
        neighbors = self._graph.neighbors(parziale[-1])
        for n in neighbors:
            if len(parziale) > 3 and n.duration > parziale[-1].duration:
                rimanenti.append(n)
            elif n.duration > parziale[-1].duration and self.isAcceptable(parziale, n):
                rimanenti.append(n)
        return rimanenti

    def isAcceptable(self, parziale, n):
        i = 0
        for p in parziale:
            if p.datetime.month == n.datetime.month:
                i+=1
        if i > 3:
            return False
        return True

    def calcola_score(self, parziale):
        score = 100*len(parziale)
        for i in range(0, len(parziale)-1):
            if parziale[i].datetime.month == parziale[i+1].datetime.month:
                score += 200
        return score






