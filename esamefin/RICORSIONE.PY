#NEL MODEL
import copy

def __init__(self):
    self._graph = nx.Graph()
    self._idMap = {}
    self._optListPiloti = []
    self._minDistGiorni = None

def getListaPilotiOttima(self, k):
    self._optListPiloti = []
    self._minDistGiorni = None

    components = list(nx.connected_components(self._graph))

    if len(components) < k:
        return None, 0

    parziale = []
    self._ricorsione(components, k, parziale, 0)

    return self._optListPiloti, self._minDistGiorni


def _ricorsione(self, components, k, parziale, indexComponente):
    if len(parziale) == k:
        date_nascita = [p.dob for p in parziale]
        differenza = (max(date_nascita) - min(date_nascita)).days

        if self._minDistGiorni is None or differenza < self._minDistGiorni:
            self._minDistGiorni = differenza
            self._optListPiloti = copy.deepcopy(parziale)

        return

    if indexComponente >= len(components):
        return

    if len(components) - indexComponente < k - len(parziale):
        return

    componente = components[indexComponente]

    for pilota in componente:
        parziale.append(pilota)
        self._ricorsione(components, k, parziale, indexComponente + 1)
        parziale.pop()

    self._ricorsione(components, k, parziale, indexComponente + 1)



#CONTROLLER
def handleCerca(self, e):
    if self._view._txtInK.value is None or self._view._txtInK.value == "":
        self._view.create_alert("Inserire un valore per K")
        return

    try:
        k = int(self._view._txtInK.value)
    except ValueError:
        self._view.create_alert("K deve essere un numero intero")
        return

    if k <= 0:
        self._view.create_alert("K deve essere maggiore di zero")
        return

    listPilotiOttima, minDistEta = self._model.getListaPilotiOttima(k)

    self._view.txt_result.controls.clear()

    if listPilotiOttima is None:
        self._view.txt_result.controls.append(
            ft.Text(
                f"Non ci sono abbastanza componenti connesse per trovare {k} piloti."
            )
        )
        self._view.update_page()
        return

    self._view.txt_result.controls.append(
        ft.Text("Lista di piloti con differenza di età minima:")
    )

    for p in listPilotiOttima:
        self._view.txt_result.controls.append(
            ft.Text(str(p))
        )

    self._view.txt_result.controls.append(
        ft.Text(f"Differenza minima di età: {minDistEta} giorni")
    )

    pilota_piu_anziano = min(listPilotiOttima, key=lambda x: x.dob)
    pilota_piu_giovane = max(listPilotiOttima, key=lambda x: x.dob)

    self._view.txt_result.controls.append(
        ft.Text(f"Pilota più anziano: {pilota_piu_anziano}")
    )

    self._view.txt_result.controls.append(
        ft.Text(f"Pilota più giovane: {pilota_piu_giovane}")
    )

    self._view.update_page()

""". L'utente seleziona da un menù a tendina un artista di partenza tra quelli presenti nel grafo costruito al punto 1.
  Artist
 PlaylistTrack
 
 Track
 Album
b. L'utente inserisce in un apposito TextField un valore intero positivo N.
c. Premendo il pulsante "Trova gruppo artisti", l'applicazione deve determinare, mediante
algoritmo ricorsivo, un insieme di artisti che soddisfi i seguenti vincoli:
• il gruppo deve contenere esattamente N artisti;
• il primo artista del gruppo deve essere quello scelto dall'utente;
• ogni artista aggiunto dopo il primo deve essere adiacente ad almeno uno degli artisti già
presenti nel gruppo;
• non possono comparire nel gruppo due artisti collegati da un arco di peso 1;
• tra tutte le soluzioni ammissibili, occorre trovare quella che massimizza la somma del
numero totale di brani degli artisti selezionati.
d. L'applicazione visualizza:
• la lista degli artisti selezionati, ordinata alfabeticamente;
• per ciascun artista, il numero di brani e il numero di playlist distinte in cui compare;
• il numero totale di artisti selezionati;
• il numero complessivo di brani della soluzione ottima."""












"""PUNTO 2
Dato il grafo del punto precedente, si inseriscano nei dropdown “Start Product” ed “End Product” tutti i nodi presenti nel grafo, e si implementi un algoritmo ricorsivo che identifichi un cammino ottimo tale per cui:
- Il cammino parti dal nodo identificato come Start Product e termini nel nodo identificato come End Product;
- La lunghezza del cammino sia pari a Lun, valore numerico fornito dall’utente nel campo “Lunghezza
cammino”;
- Il cammino attraversi gli archi rispettando i versi;
- Un nodo non può essere attraversato più volte;
- La somma dei pesi degli archi deve essere massima.
     
Identificato il percorso, se ne stampino i nodi e la somma dei pesi.
03FYZ – Tecniche di programmazione
Nella realizzazione del codice, si lavori a partire dalle classi e dal database contenuti nel progetto di base. È ovviamente permesso aggiungere o modificare classi e metodi."""

el Model aggiungi metodo per dare i nodi alla tendina
def getNodes(self):
    return list(self._graph.nodes())

def getCamminoOttimo(self, startId, endId, lun):
    start = self._idMap[int(startId)]
    end = self._idMap[int(endId)]

    self._bestPath = None
    self._bestWeight = -1

    parziale = [start]

    self._ricorsione(start, end, lun, parziale, 0)

    return self._bestPath, self._bestWeight

def _ricorsione(self, current, end, lun, parziale, pesoAttuale):

    if len(parziale) == lun + 1:
        if current == end:
            if pesoAttuale > self._bestWeight:
                self._bestWeight = pesoAttuale
                self._bestPath = parziale.copy()
        return

    for vicino in self._graph.successors(current):
        if vicino not in parziale:
            pesoArco = self._graph[current][vicino]["weight"]

            parziale.append(vicino)
            self._ricorsione(
                vicino,
                end,
                lun,
                parziale,
                pesoAttuale + pesoArco
            )
            parziale.pop()

def fillDDProducts(self):
    self._view._ddProdStart.options.clear()
    self._view._ddProdEnd.options.clear()

    for p in self._model.getNodes():
        self._view._ddProdStart.options.append(
            ft.dropdown.Option(key=str(p.product_id), text=str(p))
        )
        self._view._ddProdEnd.options.append(
            ft.dropdown.Option(key=str(p.product_id), text=str(p))
        )

    self._view.update_page()

self.fillDDProducts()

def handleCercaCammino(self, e):
    if self._view._ddProdStart.value is None:
        self._view.create_alert("Selezionare un prodotto di partenza")
        return

    if self._view._ddProdEnd.value is None:
        self._view.create_alert("Selezionare un prodotto di arrivo")
        return

    if self._view._txtInLun.value is None or self._view._txtInLun.value == "":
        self._view.create_alert("Inserire la lunghezza del cammino")
        return

    try:
        lun = int(self._view._txtInLun.value)
    except ValueError:
        self._view.create_alert("La lunghezza deve essere un numero intero")
        return

    if lun <= 0:
        self._view.create_alert("La lunghezza deve essere maggiore di zero")
        return

    path, peso = self._model.getCamminoOttimo(
        self._view._ddProdStart.value,
        self._view._ddProdEnd.value,
        lun
    )

    self._view.txt_result.controls.clear()

    if path is None:
        self._view.txt_result.controls.append(
            ft.Text("Nessun cammino trovato.")
        )
    else:
        self._view.txt_result.controls.append(
            ft.Text(f"Cammino ottimo trovato. Peso totale: {peso}")
        )

        for p in path:
            self._view.txt_result.controls.append(
                ft.Text(str(p))
            )

    self._view.update_page()



    """a. L'utente seleziona da un menù a tendina un album di partenza tra quelli presenti nel grafo costruito al punto 1.
b. Premendo il pulsante "Trova selezione", l'applicazione deve determinare, mediante algoritmo ricorsivo, un insieme di album che soddisfi i seguenti vincoli:
 
 
• Il totale degli album deve essere pari ad N, valore intero fornito dall’utente tramite apposito textField;
• ogni album selezionato deve appartenere a una componente connessa diversa rispetto agli altri album selezionati;
• il primo album della selezione deve essere l'album scelto dall'utente;
c. Tra tutte le selezioni ammissibili, l'applicazione deve individuare quella che massimizza il numero complessivo di brani, calcolato come somma delle cardinalità delle liste di brani associate agli
album selezionati.
d. L'applicazione visualizza:
• la lista (ordinata per titolo) degli album selezionati;
• per ciascun album, l’ID del genere ed il numero di brani dell'album;
• il numero totale di album selezionati;
• il numero complessivo di brani ottenuto dalla selezione.
Nella realizzazione del codice, si lavori a partire dalle classi e dal database contenuti nel progetto di base. È ovviamente permesso aggiungere o modificare classi e metodi."""

def __init__(self):
    self._graph = nx.Graph()
    self.bestSelection = []
    self.max_tracks = 0

def getAllAlbums(self):
    return list(self._graph.nodes)

def getBestSelection(self, starting_album, N):
    self.bestSelection = []
    self.max_tracks = 0

    if starting_album not in self._graph.nodes:
        return [], 0

    components = list(nx.connected_components(self._graph))

    starting_component = self._getConnectedComponent(starting_album)

    comp_rimanenti = components.copy()
    comp_rimanenti.remove(starting_component)

    parziale = [starting_album]

    self._ricorsione(parziale, N, comp_rimanenti)

    return self.bestSelection, self.max_tracks

def _ricorsione(self, parziale, N, comp_rimanenti):

    if len(parziale) == N:
        total_tracks = self._getTotalTracks(parziale)

        if total_tracks > self.max_tracks:
            self.max_tracks = total_tracks
            self.bestSelection = parziale.copy()

        return

    if len(comp_rimanenti) == 0:
        return

    if N - len(parziale) > len(comp_rimanenti):
        return

    nextComp = comp_rimanenti[0]

    # Caso 1: salto questa componente
    self._ricorsione(parziale, N, comp_rimanenti[1:])

    # Caso 2: prendo il miglior album di questa componente
    best_album = self._getAlbumWithMostTracks(nextComp)

    if best_album is not None:
        parziale.append(best_album)
        self._ricorsione(parziale, N, comp_rimanenti[1:])
        parziale.pop()

def _getConnectedComponent(self, album):
    components = list(nx.connected_components(self._graph))

    for component in components:
        if album in component:
            return component

    return None
def _getTotalTracks(self, albums):
    total = 0

    for album in albums:
        total += len(album.Tracks)

    return total

def _getAlbumWithMostTracks(self, albums):
    best_album = None
    max_tracks = -1

    for album in albums:
        num_tracks = len(album.Tracks)

        if num_tracks > max_tracks:
            max_tracks = num_tracks
            best_album = album

    return best_album
def fillDDAlbums(self):
    self._view._ddAlbum.options.clear()

    for album in self._model.getAllAlbums():
        self._view._ddAlbum.options.append(
            ft.dropdown.Option(
                key=str(album.AlbumId),
                text=album.Title,
                data=album,
                on_click=self._choiceAlbum
            )
        )

    self._view.update_page()

def _choiceAlbum(self, e):
    self._AlbumValue = e.control.data

def handleSelezione(self, e):
    self._view._txt_result.controls.clear()

    Nnodes, Nedges = self._model.getGraphDetails()
    if Nnodes == 0:
        self._view.create_alert("Creare prima il grafo")
        return

    if self._AlbumValue is None:
        self._view.create_alert("Selezionare un album")
        return

    try:
        N = int(self._view._txtInN.value)
    except ValueError:
        self._view.create_alert("Inserire un numero intero")
        return

    if N <= 0:
        self._view.create_alert("N deve essere positivo")
        return

    best_selection, total_tracks = self._model.getBestSelection(self._AlbumValue, N)

    if len(best_selection) == 0:
        self._view._txt_result.controls.append(
            ft.Text("Nessuna selezione trovata.")
        )
        self._view.update_page()
        return

    best_selection.sort(key=lambda a: a.Title)

    self._view._txt_result.controls.append(
        ft.Text("Album selezionati:")
    )

    for album in best_selection:
        genere = album.Generi[0] if len(album.Generi) > 0 else "N/A"

        self._view._txt_result.controls.append(
            ft.Text(
                f"{album.Title} - genere {genere} - {len(album.Tracks)} brani"
            )
        )

    self._view._txt_result.controls.append(
        ft.Text(f"Numero totale album selezionati: {len(best_selection)}")
    )

    self._view._txt_result.controls.append(
        ft.Text(f"Numero complessivo di brani: {total_tracks}")
    )

    self._view.update_page()



"""a. Facendo click sul pulsante “Cerca percorso”, individuare il percorso più lungo dato il grafo costruito al punto 1.
b. Trovare un cammino semplice di lunghezza massima tale che ogni nodo successivo abbia un età strettamente decrescente."""
def getCamminoPiuLungo(self):
    self._bestPath = []

    for actor in self._graph.nodes():
        parziale = [actor]
        self._ricorsione(parziale)

    return self._bestPath


def _ricorsione(self, parziale):
    ultimo = parziale[-1]

    if len(parziale) > len(self._bestPath):
        self._bestPath = parziale.copy()

    for vicino in self._graph.neighbors(ultimo):
        if vicino not in parziale and vicino.age < ultimo.age:
            parziale.append(vicino)
            self._ricorsione(parziale)
            parziale.pop()
def handleCammino(self, e):
    Nnodes, Nedges = self._model.getGraphDetails()

    if Nnodes == 0:
        self._view.create_alert("Creare prima il grafo")
        return

    cammino = self._model.getCamminoPiuLungo()

    self._view.txt_result.controls.clear()

    if len(cammino) == 0:
        self._view.txt_result.controls.append(
            ft.Text("Nessun cammino trovato.")
        )
    else:
        self._view.txt_result.controls.append(
            ft.Text(f"Cammino più lungo trovato: {len(cammino)} attori")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Lunghezza in archi: {len(cammino) - 1}")
        )

        for i, actor in enumerate(cammino, start=1):
            self._view.txt_result.controls.append(
                ft.Text(f"{i}.) {actor.name} - età: {actor.age}")
            )

    self._view.update_page()