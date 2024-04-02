from view import View
from model import Model
import flet as ft


class Controller(object):
    def __init__(self, view: View):
        self._view = view
        self._model = Model()

    def handleNuova(self, e):
        self._view._txtMrim.value = self.getMmax()  # resettiamo i tentativi rimanenti
        self._view._btnProva.disabled = False
        self._view._txtTentativo.disabled = False
        self._view._lvOut.controls.clear()
        self._view._lvOut.controls.append(ft.Text("Indovina il numero", color="green"))
        self._model.inizializza()
        # self._view._lvOut.controls.append(ft.Text(f"Segreto: {self._model.segreto}", color="blue")) --> se voglio sapere subito il segreto
        self._view.update()

    def handleProva(self, e):
        tentativo = self._view._txtTentativo.value
        self._view._txtTentativo.value = ""

        try:
            intTentativo = int(tentativo)
        except ValueError:
            self._view._lvOut.controls.append(ft.Text("Il tentativo deve essere un numero intero", color="red"))
            self._view.update()
            return

        mRim, result = self._model.indovina(intTentativo)

        self._view._txtMrim.value = mRim
        self._view.update()

        if result == 0:
            self._view._lvOut.controls.append(ft.Text("Hai vinto!"))
            self._view._btnProva.disabled = True
            self._view.update()
            return

        if mRim == 0:
            self._view._btnProva.disabled = True
            self._view._txtTentativo.disabled = True
            self._view._lvOut.controls.append(ft.Text("Hai perso! Il segreto era " + str(self._model.segreto)))
            self._view.update()
            return

        if result == -1:
            self._view._lvOut.controls.append(ft.Text("Il segreto è piu piccolo"))
            self._view.update()
            return
        elif result == 1:
            self._view._lvOut.controls.append(ft.Text("Il segreto è piu grande"))
            self._view.update()
            return



    def getNmax(self):
        return self._model.NMax

    def getMmax(self):
        return self._model.MMax

    def getMrim(self):
        return self._model.Mrim
