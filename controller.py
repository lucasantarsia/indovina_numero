from view import View
from model import Model
import flet as ft


class Controller(object):
    def __init__(self, view: View):
        self._view = view
        self._model = Model()

    def handleNuova(self, e):
        """Metodo che viene chiamato quando si clicca sul bottone 'Nuova Partita'"""

        """Controllo prima di tutto che sia stato inserito un livello di difficoltà. 
        In caso negativo non posso iniziare la partita"""
        if self._view._ddDifficolta.value == None:
            self._view._lvOut.controls.clear()
            self._view._lvOut.controls.append(ft.Text("Impossibile iniziare una nuova partita!\n"
                                                      "Scegliere prima un livello di difficoltà", color="red"))
            self._view.update()
            return

        """Resetto tutti i valori e i comandi per iniziare una nuova partita"""
        self._view._txtTentativo.disabled = False
        self._view._btnNuova.disabled = True
        self._view._btnProva.disabled = False
        self._view._btnAbbandona.disabled = False
        self._view._ddDifficolta.disabled = True
        self._view._pb.value = 0

        self._model.inizializza(self._view._ddDifficolta.value)

        self._view._lvOut.controls.clear()
        self._view._lvOut.controls.append(ft.Text("Indovina il numero", color="green"))
        self._view._lvOut.controls.append(ft.Text(f"(Segreto: {self._model.segreto})", color="blue"))  # --> se voglio sapere subito il segreto

        self._view._txtNmax.value = self._model.NMax
        self._view._txtMmax.value = self._model.MMax
        self._view._txtMrim.value = self._model.Mrim

        self._view.update()

    def handleProva(self, e):
        """Questo metodo viene chiamato quando si clicca sul bottone 'Prova'"""

        tentativo = self._view._txtTentativo.value
        self._view._txtTentativo.value = ""

        """Provo a vedere se il tentativo è un intero, se non lo è genero un'eccezione (ValueError)"""
        try:
            intTentativo = int(tentativo)
        except ValueError:
            self._view._lvOut.controls.append(ft.Text("Il tentativo deve essere un numero intero", color="red"))
            self._view.update()
            return

        """Se il tentativo fa parte della lista dei tentativi già fatti devo comunicarlo e non vale come tentativo.
        In caso contrario devo aggiungere il tentativo alla lista"""
        if self._model.tentativiFatti.__contains__(intTentativo):
            self._view._lvOut.controls.append(ft.Text("Questo tentativo è già stato inserito, riprovare", color="red"))
            self._view.update()
            return
        else:
            self._model.tentativiFatti.append(intTentativo)

        """Determino il valore della progressbar che indica il progresso dei tentativi"""
        self._view._pb.value = ((self.getMmax() - self.getMrim()) + 1) / self.getMmax()

        mRim, result = self._model.indovina(intTentativo)

        """Aggiorno il numero di tentativi rimasti e il valore si vedrà nel textfield txtMrim"""
        self._view._txtMrim.value = mRim
        self._view.update()

        """Se result = 0 vuol dire che ho vinto a prescindere da quanti tentativi rimangono"""
        if result == 0:
            self._view._lvOut.controls.append(ft.Text("Hai vinto!"))
            self._view._btnProva.disabled = True
            self._view._txtTentativo.disabled = True
            self._view._btnNuova.disabled = False
            self._view._btnAbbandona.disabled = True
            self._view._ddDifficolta.disabled = False
            self._view._ddDifficolta.value = None
            self._view.update()
            return

        """Una volta verificato che result è diverso da 0, 
        se mRim = 0 vuol dire che il numero di tentativi è 0 e quindi ho perso"""
        if mRim == 0:
            self._view._lvOut.controls.append(ft.Text("Hai perso! Il segreto era " + str(self._model.segreto)))
            self._view._btnProva.disabled = True
            self._view._txtTentativo.disabled = True
            self._view._btnNuova.disabled = False
            self._view._btnAbbandona.disabled = True
            self._view._ddDifficolta.disabled = False
            self._view._ddDifficolta.value = None
            self._view.update()
            return

        """Se result = -1 vuol dire che il segreto è piu piccolo e indico anche l'intervallo aggiornato in cui si trova.
        Lo stesso faccio se result = 1"""
        if result == -1:
            self._view._lvOut.controls.append(ft.Text(f"Il segreto è piu piccolo. Si trova nell'intervallo tra "
                                                      f"{self._model.intervallo[0]} e {self._model.intervallo[len(self._model.intervallo)-1]}"))
            self._view.update()
            return
        elif result == 1:
            self._view._lvOut.controls.append(ft.Text(f"Il segreto è piu grande. Si trova nell'intervallo tra "
                                                      f"{self._model.intervallo[0]} e {self._model.intervallo[len(self._model.intervallo)-1]}"))
            self._view.update()
            return

    def handleAbbandona(self, e):
        """Questo metodo viene chiamato quando clicco sul bottone 'Abbandona'"""

        self._view._lvOut.controls.clear()
        self._view._lvOut.controls.append(ft.Text("Hai abbandonato la partita", color="red"))
        self._view._txtNmax.value = None
        self._view._txtMmax.value = None
        self._view._txtMrim.value = None
        self._view._ddDifficolta.value = None
        self._view._btnProva.disabled = True
        self._view._txtTentativo.disabled = True
        self._view._btnNuova.disabled = False
        self._view._btnAbbandona.disabled = True
        self._view._ddDifficolta.disabled = False
        self._view._pb.value = 0

        self._view.update()

    def getNmax(self):
        return self._model.NMax

    def getMmax(self):
        return self._model.MMax

    def getMrim(self):
        return self._model.Mrim
