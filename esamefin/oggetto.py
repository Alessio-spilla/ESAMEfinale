import datetime
from dataclasses import dataclass
#importo datetime per salvare dataN
#from  model.Track import Track
@dataclass
class Driver:
    driverId: int
    driverRef: str
    number: int
    code: str
    forename: str
    surname: str
    dob: datetime
    nationality: str
    url: str
    Tracklist: list[Track] = field(default_factory=list)
    risultati: dict = field(default_factory=dict)
    quantity:int=0
    #track era un altro oggetto per cui lo importavo
    #creavo lista vuota di track che riempivo in dao

    def __hash__(self):
        return hash(self.driverId)
    #Serve perché i piloti saranno nodi del grafo.
    # NetworkX deve poterli mettere dentro un grafo, quindi devono essere “hashabili”.

    def __eq__(self, other):
        return self.driverId == other.driverId
    #Vuol dire: due piloti sono uguali se hanno lo stesso driverId.

    def __str__(self):
        return f"{self.driverRef} ({self.driverId} - DoF: {self.dob})"
    #stampa Nome (id - DoF: dataN)

    def __hash__(self):
        return hash((self.GeneID, self.Function))

def __eq__(self, other):
    return self.GeneID == other.GeneID and self.Function == other.Function
