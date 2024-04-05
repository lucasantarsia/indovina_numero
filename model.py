import random


class Model(object):
    def __init__(self):
        """
        NMax: fondo scala (cerchiamo un numero tra 1 e ?)
        Mmax: numero massimo di tentativi
        Mrim: numero tentativi rimasti
        segreto: numero segreto da indovinare
        tentativiFatti: lista con tutti i tentativi fatti (si aggiorna)
        intervallo: lista di dei numeri di cui fa parte il numero segreto (si aggiorna)
        """
        self._NMax = None
        self._Mmax = None
        self._Mrim = self._Mmax
        self._segreto = None
        self._tentativiFatti = []
        self._intervallo = []

    @property
    def segreto(self):
        return self._segreto

    @property
    def NMax(self):
        return self._NMax

    @property
    def MMax(self):
        return self._Mmax

    @property
    def Mrim(self):
        return self._Mrim

    @property
    def tentativiFatti(self):
        return self._tentativiFatti

    @property
    def intervallo(self):
        return self._intervallo

    def inizializza(self, difficolta):
        """Metodo che chiameremo quando iniziamo una nuova partita"""

        """Per ogni livello ci sono Nmax e Mmax differenti"""
        if difficolta == "Facile":
            self._NMax = 50
            self._Mmax = 5
        if difficolta == "Medio":
            self._NMax = 100
            self._Mmax = 6
        if difficolta == "Difficile":
            self._NMax = 200
            self._Mmax = 7

        """Il numero segreto viene scelto in maniera casuale"""
        self._segreto = random.randint(1, self._NMax)

        """All'inizio della partita i tentativi rimanenti sono uguali al numero massimo di tentativi"""
        self._Mrim = self._Mmax

        """All'inizio la lista dei tentativi fatti è vuota"""
        self._tentativiFatti = []

        """La lista intervallo è costituita da tutti i tentativi possibili, in questo caso la lista iniziale
        sarà formata da tutti i numeri che vanno da 1 a Nmax"""
        self._intervallo = []
        for i in range(1, self._NMax+1):
            self._intervallo.append(i)

    def indovina(self, tentativo):
        """Metodo che chiameremo quando vogliamo provare a indovinare il numero segreto"""

        """Se il numero di tentativi rimanenti sono nulli allora restutisco subito Mrim, altrimenti lo decremento """
        if self._Mrim == 0:  # se ho 0 vite esco subito, ho perso
            return self._Mrim, None  # restituisco le vite rimaste e None
        else:
            self._Mrim = self._Mrim - 1

        """Confronto il valore del tentativo con quello del numero segreto e restituisco Mrim 
        e in base ai casi 0, 1 o -1"""
        if tentativo == self._segreto:
            return self._Mrim, 0
        elif tentativo > self._segreto:
            """Se il tentativo non è uguale al num segreto (in questo caso tentativo > segreto) devo aggiornare la lista intervallo,
            che sarà formata dall' intervallo che contiene il num segreto"""
            intervalloGiusto = []
            for i in self._intervallo:
                if i < tentativo:
                    intervalloGiusto.append(i)
            self._intervallo = intervalloGiusto
            return self._Mrim, -1
        else:
            """Lo stesso di quanto scritto sopra (in questo caso tentativo < segreto)"""
            intervalloGiusto = []
            for i in self._intervallo:
                if i > tentativo:
                    intervalloGiusto.append(i)
            self._intervallo = intervalloGiusto
            return self._Mrim, 1
