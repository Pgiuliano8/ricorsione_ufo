import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        self._view.txt_result1.clean()
        year = self._view.ddyear.value
        if year is None:
            self._view.create_alert("Scegliere un anno")
            return
        shape = self._view.ddshape.value
        if shape is None:
            self._view.create_alert("Scegliere una forma")
            return
        self._model.buildGraph(year, shape)
        self._view.btn_path.disabled = False
        nNodi, nArchi = self._model.getGraphDetails()
        self._view.txt_result1.controls.append(ft.Text(f"Numero di nodi: {nNodi}"
                                                       f"\n\nNumero di archi: {nArchi}"
                                                       f"\n\nI 5 archi di peso maggiore sono:\n"))
        archi = self._model.getBestEdges()
        for a in archi:
            self._view.txt_result1.controls.append(ft.Text(f"{a[0]} -> {a[1]} | weight: {a[2]['weight']}\n"))

        self._view.update_page()


    def handle_path(self, e):
        self._view.txt_result2.clean()
        bestPath, bestScore = self._model.cammino_ottimo()
        self._view.txt_result2.controls.append(ft.Text(f"Il cammino ottimo ha peso {bestScore}\n"
                                                       f"E' composto dai nodi:\n"))
        for p in bestPath:
            self._view.txt_result2.controls.append(ft.Text(f"{p}\n"))

        self._view.update_page()




    def fill_ddyear(self):
        years = self._model.getYears()
        for y in years:
            self._view.ddyear.options.append(ft.dropdown.Option(y))

    def fill_ddshape(self, e):
        year = self._view.ddyear.value
        shapes = self._model.getShapes(int(year))
        for s in shapes:
            self._view.ddshape.options.append(ft.dropdown.Option(s))
        self._view.update_page()