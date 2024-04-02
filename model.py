import random


class Model(object):
    def __init__(self):
        self._NMax = 100  # fondo scala (cerchiamo un numero tra 0 e 100)
        self._Mmax = 6  # numero massimo di tentativi
        self._Mrim = self._Mmax
        self._segreto = None


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

    def inizializza(self):  # --> metodo che chiameremo quando iniziamo una nuova partita
        self._segreto = random.randint(1, self._NMax)
        self._Mrim = self._Mmax

    def indovina(self, tentativo):

        if self._Mrim == 0:  # se ho 0 vite esco subito, ho perso
            return self._Mrim, None  # restituisco le vite rimaste e None
        else:
            self._Mrim = self._Mrim - 1

        if tentativo == self._segreto:
            return self._Mrim, 0
        elif tentativo > self._segreto:
            return self._Mrim, -1
        else:
            return self._Mrim, 1