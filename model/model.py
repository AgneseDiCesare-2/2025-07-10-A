import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo=nx.DiGraph() #grafo diretto e pesato
        self._idMap={}

    def getDateRange(self):
        return DAO.getDateRange()

    def getCategorie(self):
        return DAO.getCategorie()

    def buildGraph(self, categoria, data1, data2):
        self._idMap = {}
        self._grafo.clear()

        nodi=DAO.getAllNodi(categoria)
        for nodo in nodi:
            self._idMap[nodo.product_id]=nodo
        self._grafo.add_nodes_from(nodi)

        #archi
        tutte_coppie=DAO.getAllCoppie(data1, data2, categoria)
        for coppia in tutte_coppie:
            #(id1, num1, id2, num2)
            if coppia[0] in self._idMap.keys() and coppia[2] in self._idMap.keys(): #non dovrebbe essere necessario ma meglio controllare
                nodo1=self._idMap[coppia[0]]
                nodo2=self._idMap[coppia[2]]

                #arco uscente dal nodo maggiore
                if coppia[1]>coppia[3]:
                    self._grafo.add_edge(nodo1, nodo2, weight=coppia[0]+coppia[3])

                elif coppia[1]<coppia[3]:
                    self._grafo.add_edge(nodo2, nodo1, weight=coppia[0] + coppia[3])

                else: #coppie uguali: inserisco entrambi gli archi
                    self._grafo.add_edge(nodo1, nodo2, weight=coppia[0] + coppia[3])
                    self._grafo.add_edge(nodo2, nodo1, weight=coppia[0] + coppia[3])
        return

    def num_nodi(self):
        return len(self._grafo.nodes)

    def num_archi(self):
        return len(self._grafo.edges)

    def get_nodi(self, id):
        return DAO.getAllNodi(id)

    def piu_venduti(self):
        tutti=[]
        for nodo in self._grafo.nodes():
            tutti.append((self._grafo.out_degree(nodo, weight='weight') - self._grafo.in_degree(nodo, weight='weight'), nodo))
        ordinati=sorted(tutti, key=lambda x: x[0], reverse=True)
        return ordinati[:5] #tuple

    def bestCammino(self, nodo1, nodo2, lun):
        self._bestSol=[]
        self._max=0

        self._ricorsione([nodo1], nodo2, lun)

        return self._bestSol

    def _ricorsione(self, parziale, nodo2, lun):
        #condizione terminale
        if parziale[-1]==nodo2:
            if self._getScore(parziale)>self._max:
                self._max=self._getScore(parziale)
                self._bestSol=copy.deepcopy(parziale)

        if len(parziale)==lun:
            return

        else:
            for nodo in nx.neighbors(self._grafo, parziale[-1]):
                if nodo not in parziale:
                    parziale.append(nodo)
                    self._ricorsione(parziale, nodo2, len)

                    parziale.pop()

    def _getScore(self, parziale):
        somma=0
        for n in range(len(parziale)-1):
            here=parziale[n]
            succ=parziale[n+1]
            somma+=self._grafo[here][succ]["weight"]
        return somma

