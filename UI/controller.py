import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._categoria = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        if self._categoria is None:
            self._view.txt_result.controls.append(ft.Text("Seleziona una categoria per procedere!", color="red"))
            self._view.update_page()
            return
        if self._view._dp1 is None or self._view._dp2 is None:
            self._view.txt_result.controls.append(ft.Text("Seleziona le date per procedere!", color="red"))
            self._view.update_page()

        self._model.buildGraph(int(self._categoria.category_id), self._view._dp1.value, self._view._dp2.value)
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato correttamente! Ha {self._model.num_nodi()} nodi e {self._model.num_archi()} archi!"))

        self._view.update_page()
        return

    def handleBestProdotti(self, e):
        venduti = self._model.piu_venduti()
        self._view.txt_result.controls.append(ft.Text(f"Prodotti più venduti: "))
        for t in venduti:
            self._view.txt_result.controls.append(ft.Text(str(t[0])))

        self._view.update_page()
        return

    def handleCercaCammino(self, e):
        pass



    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)

    def fillCategorie(self):
        self._view._ddcategory.options.clear()
        aeroporti = self._model.getCategorie()
        for n in aeroporti:
            self._view._ddcategory.options.append(
                ft.dropdown.Option(key=n.category_name, data=n, on_click=self.getCategoria)
            )
        self._view.update_page()

    def getCategoria(self, e):
        selected_key = e.control.data
        self._categoria= selected_key
        return