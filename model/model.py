import copy

from database.DAO import DAO
import networkx as nx
class Model:
    def __init__(self):
        self.grafo=nx.DiGraph()
        self.idmap ={}
        self.percorso=[]
        self.anno=0
        self.tmin=None


    def creagrafo(self,anno):
        self.grafo.clear()
        nodi=DAO.nodi(anno)
        for stati in nodi:
            self.grafo.add_node(stati)
            self.idmap[stati.id]=stati

        for n1 in self.grafo.nodes:
            for n2 in self.grafo.nodes:
                if n1.id!=n2.id:
                    archi =DAO.arco(n1,n2,anno)
                    if len(archi) >=1:
                        if self.grafo.has_edge(n1,n2):
                            continue
                        else:
                            self.grafo.add_edge(n1,n2)

    def predecessori(self,id):
        final=[]
        for i in self.grafo.predecessors(self.idmap[id]):
            final.append(i)
        return final

    def successori(self,id):
        final=[]
        for i in self.grafo.successors(self.idmap[id]):
            final.append(i)
        return final

    def raggiungibili(self,id):
        grafo = nx.dfs_tree(self.grafo,self.idmap[id])
        fine=[]
        for i in grafo.nodes:
            if i.id!=id:
                fine.append(i)
        return fine

    def path(self,id,anno):
        self.percorso=[]
        self.anno=anno

        for i in self.grafo.successors(self.idmap[id]):
            self.ricorsione([self.idmap[id]])

        return self.percorso

    def ricorsione(self,parziale):
        if len(parziale)>len(self.percorso):
            self.percorso=copy.deepcopy(parziale)
        for s in self.grafo.successors(parziale[-1]):
            if s not in parziale and self.controllo(parziale,s):
                parziale.append(s)
                self.ricorsione(parziale)
                parziale.pop()

    def controllo(self,parziale,aggiungere):
        self.tmin=DAO.tempo(parziale[-1],self.anno)
        t2=DAO.verifica(aggiungere,self.anno,self.tmin)
        if str(self.tmin)<str(t2):
            return True
        return False


    def getanniAvvist(self):
        return DAO.getannieavv()

    def getnodi(self):
        return len(self.grafo.nodes)

    def getarchi(self):
        return len(self.grafo.edges)

