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

    def piu_venduti(self):
        tutti=[]
        for nodo in self._grafo.nodes():
            tutti=(nodo, self._grafo.degree(nodo, weight='weight'))
        ordinati=sorted(tutti, key=lambda x: x[1], reverse=True)
        return ordinati[:5] #tuple

