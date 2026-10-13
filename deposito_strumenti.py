import csv
from asyncio import exceptions
from operator import attrgetter


class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self.nome = nome
        self.responsabile = responsabile
        self.strumenti=[]
        self.contatore=1


    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""

        with open(file_path,encoding="utf-8") as file:
            lettore=csv.DictReader(file,
            fieldnames=["codice", "tipo", "marca", "anno_acquisto", "valore"])
            for riga in lettore:
                self.strumenti.append(riga)


        print("File caricato con successo")

        if self.strumenti:
            numeri = [int(s["codice"][1:]) for s in self.strumenti]
            self.contatore = max(numeri) + 1








    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        codice=f"S{self.contatore:03d}"
        nuovo_strumento={"codice":codice,
                   "tipo":tipo.capitalize(),
                   "marca":marca.capitalize(),
                   "anno_acquisto":anno_acquisto,
                   "valore":valore}

        self.strumenti.append(nuovo_strumento)

        strumento=(
        f"\nCodice: {nuovo_strumento['codice']}\n"
        f"Nome: {nuovo_strumento['tipo']}\n"
        f"Marca: {nuovo_strumento['marca']}\n"
        f"Anno: {nuovo_strumento['anno_acquisto']}\n"
        f"Prezzo: {nuovo_strumento['valore']:.2f} €"
        )


        return strumento




    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        strumenti_ordinati=sorted(self.strumenti,key=lambda s: s["marca"]
    )
        return strumenti_ordinati


    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        # TODO

    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        # TODO
