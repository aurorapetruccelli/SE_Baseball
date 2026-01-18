import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.team= []
        self.dizionario_team = {}

        self.team_salario=[]
        self.coppie_team =[]
        self.K = 3

        self.G = nx.Graph()


    def crea_grafo(self,year):
        self.team = DAO.get_team_year(year)
        for team in self.team:
            self.dizionario_team[team.id]=team

        self.team_salario = DAO.get_team_salario(year)
        dizionario = {}
        for team_salario in self.team_salario:
            dizionario[team_salario[0]]=team_salario[1]


        self.coppie_team = DAO.get_coppie_team(year)
        for tuple in self.coppie_team:
            salario1 = int(dizionario[tuple[0]])
            salario2 = int(dizionario[tuple[1]])
            somma = salario1 + salario2
            self.G.add_edge(tuple[0],tuple[1],weight=somma)

        return self.G

    def stampa_team(self,year):
        self.team = DAO.get_team_year(year)
        num_squadre = 0
        lista_squadre = []
        for team in self.team:
            num_squadre = num_squadre + 1
            lista_squadre.append((team.team_code,team.name,team.id))

        print(lista_squadre)
        return lista_squadre, num_squadre


    def get_year(self):
        return DAO.get_year()


    def get_vicini(self,nodo):
        componente_connessa = []
        for vicino in self.G.neighbors(nodo):
            componente_connessa.append(vicino)
        result = []
        for componente in componente_connessa:
            code_componente = self.dizionario_team[componente].team_code
            name_componente = self.dizionario_team[componente].name
            peso_arco = self.G[nodo][componente]["weight"]
            result.append((componente,code_componente,name_componente,peso_arco))


        return sorted(result, key=lambda x: x[3], reverse=True)


    def ricerca(self,nodo):
        self.cammino_migliore = []
        self.peso_migliore = 0
        self.ricorsione([nodo],[],0,float('inf'))

        result = []
        for cammino in self.cammino_migliore:
            nodo1 = self.dizionario_team[cammino[0]].team_code
            nodo1_nome = self.dizionario_team[cammino[0]].name
            nodo2 = self.dizionario_team[cammino[1]].team_code
            nodo2_nome = self.dizionario_team[cammino[1]].name
            result.append((nodo1,nodo1_nome,nodo2,nodo2_nome,cammino[2]))

        print(result)
        return result, self.peso_migliore



    def ricorsione(self, partial_nodes,partial_edges, peso, ultimo_peso):
        # voglio considerare solo i primi tre nodi ( =self.K)
        # e voglio trovare il cammino con peso max
        ultimo_nodo = partial_nodes[-1]

        if peso>self.peso_migliore:
            self.peso_migliore = peso
            self.cammino_migliore = partial_edges.copy()

        counter =  0
        neigh = []
        vicini = self.get_vicini(ultimo_nodo)
        for v in vicini:
            if v[0] in partial_nodes:
                continue

            if v[3]<=ultimo_peso: # il minore uguale serve a trovare un cammino con peso decrescente
                neigh.append((v[0],v[3]))
                counter = counter + 1
                if counter == self.K:
                    break

        for n in neigh:
            partial_nodes.append(n[0])
            partial_edges.append((ultimo_nodo,n[0],n[1]))
            self.ricorsione(partial_nodes, partial_edges,peso+n[1],n[1])
            partial_nodes.pop()
            partial_edges.pop()
