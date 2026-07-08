#from database.DB_connect import DBConnect collegare
#from model.driver import Driver
#from model.arco import Arco SE DEVO CREARE OGGETTI DA RISULTATI
#restituisce lista [] anni
class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = ("""SELECT DISTINCT year 
                         FROM seasons s 
                         ORDER BY year""")
        #in generale testo le query prima su dbeaver
        #dinstinct evita i doppioni  order by ordine crescente
        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])
            #results.append(Oggetto(row ecc

        #row = cursor.fetchone()
        #return row["min_lat"], row["max_lat"], row["min_lng"], row["max_lng"]
        #cosi faccio una singola tupla

        cursor.close()
        conn.close()
        return results


    # SELECT *
    # FROM races
    # LIMIT 10; mi serve per navigare e vedere su dbeaver

    # I nodi sono costituiti da tutti i PILOTI query =
    # """select distinct d.* allora nella query la prima sarà cosi
    # """ SERVONO PER SCRIVERE SU PIù RIGHE I CARATTERI VANNO BENE MAIUSCOLI O MINUSCOLI
    # ` lo usa perché POSITION PUò DARE FASTIDIO
    # NELLA QUERY %s e %s dice che i valori si inseriscono poi in menù a tendina
    # prende i due input da bottoni
    # se devo provare su dbeaver solo numeri veri non %s
    @staticmethod
    def getAllNodes(year1, year2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct d.*
                        from drivers d, results r, races ra
                        WHERE d.driverId = r.driverId AND r.raceId = ra.raceId
                        and ra.year between %s and %s 
                        and r.`position` is not null
                        order by d.driverId """
        # d.* posso farlo se nomi database combaciano lettera per lettera con mia classe

        cursor.execute(query, (year1, year2))
        #(genere,) scrivevo cosi se inserivo solo un elemento di input

        for row in cursor:
            results.append(Driver(**row))
            # faccio Driver(**row) perche classe driver ha gli stessi nomi dei campi
            # per cui avrò una lista di driver

        cursor.close()
        conn.close()
        return results





    # NELLA TRACCIA AVEVA DETTO C'è UN ARCO SOLO SE CON CONDIZIONI
    # CREO ARCHI CON PESO CHE AUMENTA OGNI VOLTA CHE SONO STATI INSIEME DUE PILOTI
    # r1.driverID> r2.driverID evita doppioni
    # IS not null arrivano al traguardo
    # group by diventa un unico gruppo a cui poi aumenta il peso dell'arco
    # desc ordinamento decrescente

    @staticmethod
    def getAllEdges(year1, year2, idMapDriver):
        conn = DBConnect.get_connection()
        # idMapDriver è un dizionario che ci permette di prendere
        # oggetto da id in questo caso da idDriver prendiamo oggetto driver completo
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select r1.driverId as d1, r2.driverId as d2 , count(*) as peso SENNO COUNT(distinct parametro)
                    from results r1, results r2, races r
                    WHERE r.raceId = r1.raceId and r.raceId = r2.raceId 
                    and r1.constructorId = r2.constructorId 
                    and r1.driverId > r2.driverId non prendo coppie duplicate perche raggruppo per coppia 
                    and r1.position is not null 
                    and r2.position is not null 
                    and r.year between %s and %s
                    group by r1.driverId , r2.driverId 
                    order by peso desc """
        #PER ESEMPIO GAREA DIVERSA !=

        cursor.execute(query, (year1, year2))

        for row in cursor:
            results.append(Arco(idMapDriver[row["d1"]], idMapDriver[row["d2"]], row["peso"]))
            # creo arco tra driver1,driver2, con peso

        cursor.close()
        conn.close()
        return results




    #===============
    @staticmethod
    def getCustomerArtistCounts(genere):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select i.CustomerId, art.ArtistId, count(*) as ntracks
                        from invoice i, invoiceline i2, track t, genre g, artist art,album a
                        where i.InvoiceId  = i2.InvoiceId 
                        and t.TrackId = i2.TrackId 
                        and t.AlbumId = a.AlbumId
                        and g.GenreId = t.GenreId
                        and art.ArtistId = a.ArtistId 
                        and g.Name = %s
                        group by i.CustomerId, art.ArtistId
                        having N >= %s"""
        cursor.execute(query, (genere,))

        for row in cursor:
            results.append((row["CustomerId"], row["ArtistId"], row["ntracks"]))

        cursor.close()
        conn.close()
        return results
    #conto quanti acquisti fa customer di artista per quel genere

sum( cast(replace(replace(m.worlwide_gross_income, '$', ''),',', '') as unsigned)) as weight
and m.worlwide_gross_income like '$%' condizione e anche >
#per trasformare denaro in peso



@staticmethod
    def getTracksForAlbum(album):
        #gli passo un album e lo popolo con i suoi tracks
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select t.*
                from track t
                where t.AlbumId = %s
                order by t.Name
                """

        cursor.execute(query, (album.AlbumId,))

        for row in cursor:
            results.append(Track(**row))
        album.Tracks = results

        cursor.close()
        conn.close()
#nell'oggetto album ho Tracks:list[Track]
#per cui aggiungo li e non ritorno nulla perche ho gia aggiunto



DATE(o.order_date)
#IN QUESTO CASO PRENDO SOLO DATA E NON ORA

SELECT DISTINCT year(s.datetime) as anno
                 FROM sighting s
                 ORDER BY  anno desc
#FACCIO YEAR PERCHE DATA ERA TIPO Y-M-G ORARIO ED ESTRAGGO SOLO Y
# MA ANCHE MONTH DAY HOUR MINUTE SECOND


@staticmethod
def getAllOQuantity(order1):
    conn = DBConnect.get_connection()

    cursor = conn.cursor(dictionary=True)
    query = """
        select sum(oi.quantity) as quantity
        from order_items oi
        where oi.order_id = %s
    """

    cursor.execute(query, (order1,))

    row = cursor.fetchone()

    if row["quantity"] is None:
        result = 0
    else:
        result = row["quantity"]

    cursor.close()
    conn.close()
    return result
#IN QUESTO MODO RITORNO UNA QUANTITà NON UNA LISTA



@staticmethod
def getRisultatiForConstructor(constructor, year1, year2):
    conn = DBConnect.get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT ra.year AS year,
               ra.raceId AS raceId,
               r.driverId AS driverId,
               r.position AS position
        FROM results r, races ra
        WHERE r.raceId = ra.raceId
        AND r.constructorId = %s
        AND ra.year BETWEEN %s AND %s
        AND r.position IS NOT NULL
    """

    cursor.execute(query, (constructor.constructorId, year1, year2))

    for row in cursor:
        anno = row["year"]

        if anno not in constructor.risultati:
            constructor.risultati[anno] = []

        constructor.risultati[anno].append(
            Risultato(
                row["raceId"],
                row["driverId"],
                row["position"]
            )
        )

    cursor.close()
    conn.close()