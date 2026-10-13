import csv
from asyncio import exceptions
from operator import attrgetter

class Strumento:
    def __init__(self, codice, tipo, marca, anno_acquisto, valore):
        self.codice = codice
        self.tipo = tipo
        self.marca = marca
        self.anno_acquisto = anno_acquisto
        self.valore = valore

    def __str__(self):
        return (
            f"Codice: {self.codice}, "
            f"Tipo: {self.tipo}, "
            f"Marca: {self.marca}, "
            f"Anno: {self.anno_acquisto}, "
            f"Valore: {self.valore:.2f} €"
        )

class Prestito:
    def __init__(self, codice, data, strumento, cognome_allievo):
        self.codice = codice
        self.data = data

        self.strumento = strumento
        self.cognome_allievo = cognome_allievo

    def __str__(self):
        return (
            f"Codice prestito: {self.codice}, "
            f"Data: {self.data}, "
            f"Strumento: {self.strumento.codice}, "
            f"Allievo: {self.cognome_allievo}"
        )


class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self.nome = nome
        self.responsabile = responsabile
        self.strumenti=[]
        self.prestiti = []
        self.contatore_strumenti = 1
        self.contatore_prestiti = 1


    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""

        with open(file_path,encoding="utf-8") as file:
            lettore=csv.reader(file)

            for riga in lettore:
                # Salta le righe vuote
                if not riga:
                    continue

                # Assegna i cinque campi alle rispettive variabili
                codice, tipo, marca, anno, valore = riga

                # Crea un oggetto convertendo anno e valore in numeri
                strumento = Strumento(
                    codice,
                    tipo,
                    marca,
                    int(anno),
                    float(valore)
                )

                # Inserisce l'oggetto nella lista del deposito
                self.strumenti.append(strumento)

            # Aggiorna il contatore usando il codice più alto presente
            # nel deposito, così il prossimo codice non viene duplicato
            if self.strumenti:
                numeri = [
                    int(s.codice[1:]) for s in self.strumenti
                ]
                self.contatore_strumenti = max(numeri) + 1

        print("File caricato con successo")










    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""

        # Genera il codice progressivo dello strumento
        codice=f"S{self.contatore_strumenti}"

        # Crea il nuovo oggetto Strumento con i dati ricevuti
        nuovo_strumento = Strumento(
            codice,
            tipo.capitalize(),
            marca.capitalize(),
            anno_acquisto,
            valore
        )

        # Inserisce il nuovo strumento nella lista del deposito
        self.strumenti.append(nuovo_strumento)

        # Incrementa il contatore per il prossimo strumento
        self.contatore_strumenti += 1

        # Restituisce l'oggetto creato, non una stringa
        # La stampa utilizzerà automaticamente il metodo __str__
        return nuovo_strumento








    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""

        # sorted crea una nuova lista ordinata e non modifica
        # l'ordine della lista originale self.strumenti
        # attrgetter estrae l'attributo marca da ogni oggetto
        strumenti_ordinati = sorted(self.strumenti,key=attrgetter("marca"))

        # Restituisce la lista ordinata
        return strumenti_ordinati


    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""

        # Cerca lo strumento richiesto all'interno del deposito
        strumento_trovato = None

        for strumento in self.strumenti:
            if strumento.codice == id_strumento:
                strumento_trovato = strumento
                break

        # Se lo strumento non esiste, segnala un errore
        if strumento_trovato is None:
            raise Exception("Strumento non presente nel deposito")

        # Controlla che lo strumento non sia già in prestito
        for prestito in self.prestiti:
            if prestito.strumento.codice == id_strumento:
                raise Exception("Lo strumento è già in prestito")

        # Genera il codice del nuovo prestito
        codice = f"P{self.contatore_prestiti}"

        # Crea l'oggetto Prestito associandolo allo strumento trovato
        nuovo_prestito = Prestito(
            codice,
            data,
            strumento_trovato,
            cognome_allievo
        )

        # Registra il prestito nella lista
        self.prestiti.append(nuovo_prestito)

        # Incrementa il contatore per il prossimo prestito
        self.contatore_prestiti += 1

        # Restituisce l'oggetto Prestito creato
        return nuovo_prestito

    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""

        # Cerca il prestito tramite il suo codice
        for prestito in self.prestiti:
            if prestito.codice == id_prestito:
                # Rimuove il prestito dalla lista:
                # lo strumento torna così disponibile
                self.prestiti.remove(prestito)
                return

        # Se nessun prestito corrisponde al codice, segnala un errore
        raise Exception("Prestito non trovato")

