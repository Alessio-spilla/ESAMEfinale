import flet as ft
#importare sempre serve per la componente grafica
class Controller:
    def fillDDYear(self):
        years = self._model.getAllYears()
        # prendo la lista anni da model
        for y in years:
            self._view._ddAnno1.options.append(ft.dropdown.Option(y))
            self._view._ddAnno2.options.append(ft.dropdown.Option(y))
        self._view.update_page()
        # tramite questo metodo riempio una tendina
        # per ogni anno appendo sia in ddanno1 che è la prima tendina sia nella 2
        # aggiorno la pagina



    # SEMPRE EFFETTUARE CONTROLLI PRIMA DI CREARE GRAFO
    if self._view.dd_min_ch.value is None:
        self._view.create_alert("Selezionare un valore per Chromosoma min")
        return
    else:
        ch_min = int(self._view.dd_min_ch.value)
    if self._view.dd_max_ch.value is None:
        self._view.create_alert("Selezionare un valore per Chromosoma max")
        return
    else:
        ch_max = int(self._view.dd_max_ch.value)
    if ch_min > ch_max:
        self._view.create_alert("Attenzione: deve essere Chromosoma min <= Chromosoma max")
        return

    # controlli da fare in crea grafo nel caso di tendina

    try:
        latitude = float(self._view.txt_latitude.value)
        longitude = float(self._view.txt_longitude.value)
    except ValueError:
        self._view.create_alert("Latitude e longitude devono essere numeri")
        return

    #QUESTI NEL CASO DI VALORI INSERITI A MANO

    #funzione per creare grafo
    def handleCreaGrafo(self, e):
        self._model.buildGraph(
            self._view._ddAnno1.value,
            self._view._ddAnno2.value
        )

        Nnodes, Nedges = self._model.getGraphDetails()
        #prendo numero nodi e numero archi del grafo
        self._view._txt_result.controls.clear()
        #svuoto i risultati stampati di prima

        self._view._txt_result.controls.append(
            ft.Text(
                f"Grafo correttamente creato. "
                f"Il grafo contiene {Nnodes} nodi e {Nedges} archi."
            )
        )
        #appendo i nuovi risultati
        self._view.update_page()
        #aggiorno la pagina

    #stampiano dettagli self e button
    def handleDettagli(self, e):
        top3 = self._model.getTop3Archi()
        #richiamo funzione model

        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(
            ft.Text("Archi di peso maggiore:")
        )

        for arco in top3:
            self._view._txt_result.controls.append(
                ft.Text(
                    f"{arco[0]} -> {arco[1]} "
                    f"(peso: {arco[2]['weight']})"
                )
            )
            #stampo i primi 3 archi di peso maggiore con collegamento tra i due nodi e il peso

        numero, largest, details = self._model.getConnessaInfo()
        #prendo le componenti connesse il numero, la più grande e i dettagli della più grande

        self._view._txt_result.controls.append(
            ft.Text(f"Il grafo contiene {numero} componenti connesse.")
        )

        self._view._txt_result.controls.append(
            ft.Text(
                f"La componente connessa maggiore ha dimensione pari a {len(largest)}."
            )
        )

        self._view._txt_result.controls.append(
            ft.Text("Componente connessa in ordine decrescente di grado dei nodi.")
        )
        for actor in sorted(largest, key=lambda x: x.name):
            self._view.txt_result.controls.append(
                ft.Text(f"{actor.name}")
            )
            #stampare componente connessa

        for d in details:
            self._view._txt_result.controls.append(
                ft.Text(f"{d[0]} - grado: {d[1]}")
            )

        self._view.update_page()
        #stampo tutto



    #================
    #Grafo orientato

    def handleCreaGrafo(self, e):


        bestartist, best = self._model.getBestArtist()

        self._view._txt_result.controls.append(
            ft.Text(f"Artista più influente: {bestartist}, con influenza: {best}")
        )

        topEdges = self._model.getTop5Edges()

        self._view._txt_result.controls.append(ft.Text("Top 5 archi:"))

        for u, v, data in topEdges:
            self._view._txt_result.controls.append(
                ft.Text(f"{u.Name} -> {v.Name} : {data['weight']}")
            )

        self._view.update_page()


    def handle_dettagli(self, e):
        result = self._model.getConnessaInfo()
        for n,grado in result:
            testo=""
            for c in n:
                testo+=f" {c.GeneID}"

            self._view.txt_result1.controls.append(ft.Text(f'{testo}'))
            self._view.txt_result1.controls.append(ft.Text(f'{grado}'))
        self._view.update_page()


self._view.txt_result.controls.append(ft.Text(f"Start date: {self._view._dp1.value.date()}"))
#per stampare data
top10=self._model.getTop10Artist()
for i, arco in enumerate(top10, start=1):
    a1, a2, peso = arco

    self._view._txt_result.controls.append(
        ft.Text(f"{i}.) {a1.Name} - {a2.Name}: peso {peso}")
    )






