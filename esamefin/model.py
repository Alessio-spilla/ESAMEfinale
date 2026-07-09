import copy
#serve poi per trovare la soluzione migliore

import networkx as nx
#serve per il grafo

from database.DAO import DAO


#CREAZIONE GRAFO SEMPLICE NON PESATO CON nx.Graph()
class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMapDrivers = {}
        #dizionario vuoto per trasformare id in oggetto
        self._drivers = []
        #lista di piloti vuota

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)
    #restituisce numero nodi e archi

    def getAllYears(self):
        return DAO.getAllYears()



    def buildGraph(self, country1):
        self._graph.clear()
        self._customers = DAO.getAllNodes(country1)

        for c in self._customers:
            self._idMap[c.CustomerId] = c
        # dizionario che associa id ad artista

        self._graph.add_nodes_from(self._customers)
        # aggiungo nodi

        customer_artist_list = DAO.getCustomerArtist(country1)
        # prendo conteggio di quanti acquisti fa customer per artista

        customerMap = defaultdict(set)
        # dizionario
        #dizionario con valore un set cosi aumento velocita
        for customer_id, artist_id in customer_artist_list:
            customerMap[customer_id].add(artist_id)

        for c1, c2 in itertools.combinations(self._customers, 2):
            artisti_c1 = customerMap[c1.CustomerId]
            #ESTRAGGO DA UN DIZIONARIO ANCHE COME .get(c1.CustomerId,0)
            #COSI SE NON C'è VALORE VA A 0
            artisti_c2 = customerMap[c2.CustomerId]

            if artisti_c1 & artisti_c2:
                peso = c1.Fatturato + c2.Fatturato

                if c1.Fatturato > c2.Fatturato:
                    self._graph.add_edge(c1, c2, weight=peso)

                elif c2.Fatturato > c1.Fatturato:
                    self._graph.add_edge(c2, c1, weight=peso)

                else:
                    self._graph.add_edge(c1, c2, weight=peso)
                    self._graph.add_edge(c2, c1, weight=peso)




    #metodo per creare grafo
    def buildGraph(self, year1, year2):
        self._graph.clear()
        #pulisco grafo ogni volta che chiamo funzione in modo che

        self._drivers = DAO.getAllNodes(year1, year2)
        #chiedo al dao i nodi
        for d in self._drivers:
            self._idMapDrivers[d.driverId] = d
        #creo dizionario id ---> driver

        self._graph.add_nodes_from(self._drivers)
        #aggiungo al grafo tutti i nodi come piloti

        self._edges = DAO.getAllEdges(year1, year2, self._idMapDrivers)
        #chiedo al DAO tutti gli archi

        for e in self._edges:
            self._graph.add_edge( self._idMap[e[0]], self._idMap[e[1]], weight=e[2]
            )
        #aggiungo al grafo tutti gli archi









    def getTop3Archi(self):
        return sorted(
            self._graph.edges(data=True),
            key=lambda x: x[2]["weight"],
            reverse=True
        )[:3]
    #(data=true) oltre archi include anche attributi in questo caso il peso
    #ordinati per peso decrescente dal maggiore al minore
    # [:3] i primi 3


    #STESSO DI PRIMA MA CON CONDIZIONI PER ORDINAMENTO ALFABETICAMENTE
    def getTop10Archi(self):
        result = []

        for a1, a2, data in self._graph.edges(data=True):
            if a1.Name <= a2.Name:
                primo = a1
                secondo = a2
            else:
                primo = a2
                secondo = a1

            result.append((primo, secondo, data["weight"]))

        result.sort(key=lambda x: (-x[2], x[0].Name, x[1].Name))
        return result[:10]


    #Componente connessa è un gruppo di nodi del grafo collegati tra loro
    #DETAILS RESTITUISCE GRADO DI CIASCUN NODO NELLA COMPONENTE PIUù GRANDE
    def getConnessaInfo(self):
        components = list(nx.connected_components(self._graph))
        #nx.weakly_connected_components(self._graph) questo per grafi orientati
        #nx mi da la lista di tutti i componenti connessi

        largest = max(components, key=len)
        #prendo il componente con più nodi

        subgraph = self._graph.subgraph(largest).copy()
        #sottografo= prendo nodi e archi della componente maggiore
        #album_ordinati = sorted(largest, key=lambda a: a.Title.lower())
        #ordinati in ordine alfabetico
        orderedNodes = sorted(
            subgraph.nodes(),
            key=lambda n: self._graph.degree(n),
            reverse=True
        )
        #ordino i nodi della componente maggiore da quello più cllegato a quello meno collegato

        details = [(n, self._graph.degree(n)) for n in orderedNodes]
        #preparo lista di nodi con il loro grado=numero di collegamenti
        return len(components), largest, details

    def getTop5Componenti(self):
        components = list(nx.connected_components(self._graph))
        components.sort(key=lambda c: len(c), reverse=True)

        result = []

        for comp in components[:5]:
            nodi_ordinati = sorted(comp, key=lambda n: n.Name.lower())
            result.append((len(comp), nodi_ordinati))

        return result





#====================
#GRAFO ORIENTATO
#====================
import networkx as nx
from database.DAO import DAO
from collections import defaultdict
#raggruppare o contare senza controllare se la chiave esiste
import itertools
#creare tutte le coppie possibili da una lista

class Model:
        self._graph = nx.DiGraph()
        self._idMap = {}
#DiGraph per grafo orientato
#idMap per collegare id a oggetto

    def buildGraph(self, genere):
        self._graph.clear()
        self._artist = DAO.getAllArtistbyGenre(genere)

        for a in self._artist:
            self._idMap[a.ArtistID] = a
        #dizionario che associa id ad artista

        self._graph.add_nodes_from(self._artist)
        #aggiungo nodi

        custom_artist_list = DAO.getCustomerArtistCounts(genere)
        #prendo conteggio di quanti acquisti fa customer per artista

        customerMap = defaultdict(dict)
        #dizionario

        for customer_id, artist_id, ntracks in custom_artist_list:
            customerMap[customer_id][artist_id] = ntracks
            #dizionario che ha all'interno un altro dizionario
            # customermap={ customerid:{artistaid:numeroacquisti}}

        artist_popularity = defaultdict(int)
        #dizionario numero totale acquisti di un artista per quel genere

        for customer, artists in customerMap.items():
            for artist_id, ntracks in artists.items():
                artist_popularity[artist_id] += ntracks

        for customer_id, artists in customerMap.items():
            for a, b in itertools.combinations(artists.keys(), 2):
                #prendi gli artisti di un cliente e crea tutte le coppie possibili di 2 artisti

                pop_a = artist_popularity[a]
                pop_b = artist_popularity[b]

                weight = pop_a + pop_b

                if pop_a < pop_b:
                    self._graph.add_edge(self._idMap[a], self._idMap[b], weight=weight)
                elif pop_a > pop_b:
                    self._graph.add_edge(self._idMap[b], self._idMap[a], weight=weight)
                else:
                    self._graph.add_edge(self._idMap[a], self._idMap[b], weight=weight)
                    self._graph.add_edge(self._idMap[b], self._idMap[a], weight=weight)
                #creo archi in base alla popolarità




    #OGGETTO PIù INFLUENTE
    def getBestArtist(self):
        bestArtist = None
        bestScore = None
        #inizializzo variabili

        for v in self._graph.nodes():
            #per nodo in nodi

            outWeight = 0
            for _, _, data in self._graph.out_edges(v, data=True):
                outWeight += data["weight"]
            # uso _, perche non mi interessano mi interessa solo data che
            # è il dizionario di attributi
            #freccia uscente

            inWeight = 0
            for _, _, data in self._graph.in_edges(v, data=True):
                inWeight += data["weight"]

            score = outWeight - inWeight

            if bestScore is None or score > bestScore:
                bestScore = score
                bestArtist = v

        return bestArtist.Name, bestScore





  #INVECE DI CHIAMARE SHAREGENRE
for a1, a2 in itertools.combinations(self._artists, 2):
    ids1 = set(p.PlaylistId for p in a1.Playlists)
    ids2 = set(p.PlaylistId for p in a2.Playlists)

    common = ids1 & ids2

    if common:
        peso = len(common)
        self._graph.add_edge(a1, a2, weight=peso)



customerMap = defaultdict(set)
# dizionario

for customer_id, artist_id in customer_artist_list:
    customerMap[customer_id].add(artist_id)
    #in questo modo creo dizionario e dentro posso mettere più artisti non duplicati
for c1, c2 in itertools.combinations(self._customers, 2):
    artisti_c1 = customerMap[c1.CustomerId]
    artisti_c2 = customerMap[c2.CustomerId]
    #v1 = venditeMap.get(p1.product_id, 0) in questo modo se 0 non crasha
    #for i in range(len(lista)):
   # for j in range(i + 1, len(lista)):

    if artisti_c1 & artisti_c2:
        peso = c1.Fatturato + c2.Fatturato

        if c1.Fatturato > c2.Fatturato:
            self._graph.add_edge(c1, c2, weight=peso)

        elif c2.Fatturato > c1.Fatturato:
            self._graph.add_edge(c2, c1, weight=peso)

        else:
            self._graph.add_edge(c1, c2, weight=peso)
            self._graph.add_edge(c2, c1, weight=peso)
#questa è l'intersezione di due set vedo se hanno componenti in comune allora


for album1, album2 in itertools.combinations(albums, 2):
    if self._shareGenre(album1, album2):
        self._graph.add_edge(album1, album2)
    #PRENDE DALLA LISTA SENZA RIPETIZIONI UNA COPPIA E LE CONFRONTA
def _shareGenre(self, album1, album2):
    genres1 = set(track.GenreId for track in album1.Tracks if track.GenreId is not None)
    genres2 = set(track.GenereId for track in album2.Tracks if track.GenreId is not None)

    return bool(genres1 & genres2)

#CREA SET CON ATTRIBUTO DA CONFRONTARE E POI FA INTERSEZIONE


    def getConnessaInfo(self):
        components = list(nx.connected_components(self._graph))
        largest = max(components, key=len)
        result = []
        for a in list(largest):
            num_t=len(a.Tracks)
            result.append((num_t, a.Title))
        result.sort(key=lambda x: x[1])
        return len(components), largest,result
    #questa mi da



#massimo grado
#self._graph.degree trova il grado      NODO CON GRADO MAGGIORE= NUMERO DI ARCHI POSSO FARLO SIA PER ORIENTATI CHE NON
# SE LO FACCIO PER ORIENTAATI COME GIU (SOMMA USCENTI+ ENTRANTI SENNO IN OUT DEGREE
def getArtistWithMaxDegree(self):
    Nnodes, Nedges = self.getGraphDetails()
    if Nnodes == 0:
        return None, 0
    best_artist = None
    best_degree = -1

    for artist, degree in self._graph.degree():
        if degree > best_degree:
            best_degree = degree
            best_artist = artist

    return best_artist, best_degree
#self._graph.degree() restituisce coppie:
#(nodo, grado)
#5 NODI CON MAGGIOR NUMERO DI ARCHI SUCENTI         GRADO MAGGIORE
def getTop5OutDegree(self):
    result = []

    for n in self._graph.nodes():
        num_archi_uscenti = self._graph.out_degree(n)

        peso_totale = 0
        for _, _, data in self._graph.out_edges(n, data=True):
            peso_totale += data["weight"]

        result.append((n, num_archi_uscenti, peso_totale))

    result.sort(key=lambda x: x[1], reverse=True)

    return result[:5]







if Nnodes == 0:
    return None, 0
#CONTROLLO DA FARE SEMPRE NEL CASO IN CUI DEVO STAMPARE INFORMAZIONI SEPARATAMENTE AL GRAFO

#artista con somma più alta CONSIDERANDO NODI VICINI SOMMA DEL PESO
#NODO CON SOMMA  MAGGIORE DEI PESI ARCHI CHE COLLEGANO AI NODI VICINI
def getArtistWithMaxWeightSum(self):
    Nnodes, Nedges = self.getGraphDetails()
    if Nnodes == 0:
        return None, 0
    best_sum = -1
    best_artist = None
    for artist in self._graph.nodes:
        total = 0

        for neighbor in self._graph.neighbors(artist):
            total += self._graph[artist][neighbor]["weight"]
            #SOMMO PESI ARCO TRA MIO NODO E NODO VICINO
            #FACCIO COSI PER TUTTI I NODI VICINI
        #neighbors

        if total > best_sum:
            best_sum = total
            best_artist = artist
    return best_artist, best_sum
#5 NODI CON SOMMA MAGGIORE DEI PESI ARCHI CHE COLLEHANO AI NODI VICINI
def getTop5WeightSum(self):
    result = []

    for artist in self._graph.nodes:
        total = 0

        for neighbor in self._graph.neighbors(artist):
            total += self._graph[artist][neighbor]["weight"]

        grado = self._graph.degree(artist)

        result.append((artist, grado, total))

    result.sort(key=lambda x: x[2], reverse=True)

    return result[:5]

#COMANDO CHE PRENDE DIZIONARIO E LO TRASFORMA IN LISTA DI TUPLE
top5 = sorted(
    prodotti_peso.items(),
    key=lambda x: x[1],
    reverse=True
)[:5]


# grafo non diretto
nx.Graph()
self._graph.degree(n)

# grafo diretto
nx.DiGraph()
self._graph.in_degree(n)
self._graph.out_degree(n)
self._graph.degree(n)


#PRESO UN NODO CERCO IL PESO MASSIMO DI UNO DEGLI ARCHI
def getPesoMassimoIncidente(self, nodo):
    max_peso = 0

    for _, _, data in self._graph.edges(nodo, data=True):
        if data["weight"] > max_peso:
            max_peso = data["weight"]

    return max_peso

#IN QUESTO CASO DETAILS RESTITUISCE COMPONENTE MAGGIORE
#ORDINATA PER NODI CON PESO ARCHI MAGGIORE
def getConnessaInfo(self):
    components = list(nx.connected_components(self._graph))

    largest = max(components, key=len)

    subgraph = self._graph.subgraph(largest).copy()
    #PRENDO COMPONENTE CONNESSA MAGGIORE E ORDINO I NODI IN BASE A QUALE HA PESO ARCO MASSIMO

    orderedNodes = sorted(
        subgraph.nodes(),
        key=lambda n: self.getPesoMassimoIncidente(n),
        reverse=True
    )

    details = [(n, self.getPesoMassimoIncidente(n)) for n in orderedNodes]

    return len(components), largest, details

data1 = datetime.strptime(datadainseriredaoggetto, "%Y-%m-%d %H:%M:%S")
                          #TRASFORMO DATA IN NUMERO SOTTRAIBILE solo nel caso in cui datainserireoggetto sia stringa e non gia datetime
                          se faccio sottraggo due datetime posso fare .years .days o altro ottengo intero


lista1 = [1, 2, 3]
lista2 = [3, 4, 5]

comuni = set(lista1) & set(lista2)

if len(comuni) > 0:
    print("Hanno almeno un elemento in comune")
    #PER VEDERE SE LISTE HANNO ELEMENTI IN COMUNE TRASFORMO IN SET E INTERSEZIONE



    def getConnessaInfo(self):
        components = list(nx.connected_components(self._graph))
        # nx.weakly_connected_components(self._graph) questo per grafi orientati
        result=[]
        for componente in components:
            if len(componente) > 1:
                result.append((componente, len(componente)))
        result.sort(key=lambda x: x[1], reverse=True)

        # preparo lista di nodi con il loro grado=numero di collegamenti
        return result


if peso1 is None or peso2 is None:
    continue
