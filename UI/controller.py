import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        try:
            year = int(self._view.dd_anno.value)
        except ValueError:
            self._view.show_alert("Inserire anno valido")
            return
        self._model.crea_grafo(year)



    def handle_dettagli(self, e):
        """ Handler per gestire i dettagli """""
        nodo = int(self._view.dd_squadra.value)
        team = self._model.get_vicini(nodo)

        self._view.txt_risultato.controls.clear()
        for t in team:
            self._view.txt_risultato.controls.append(ft.Text(f"{t[1]} ({t[2]}) - peso {t[3]}"))

        self._view.update()


    def handle_percorso(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del percorso """""
        nodo = int(self._view.dd_squadra.value)
        cammino,peso = self._model.ricerca(nodo)

        self._view.txt_risultato.controls.clear()
        for cam in cammino:
            self._view.txt_risultato.controls.append(ft.Text(f"{cam[0]} ({cam[1]}) --> {cam[2]} ({cam[3]}) (peso : {cam[4]})"))

        self._view.txt_risultato.controls.append(ft.Text(f"peso totale: {peso}"))
        self._view.update()


    def year(self):
        return self._model.get_year()

    def change_year(self,e):
        year = int(self._view.dd_anno.value)

        team,num_team = self._model.stampa_team(year)
        self._view.txt_out_squadre.controls.clear()
        self._view.txt_out_squadre.controls.append(ft.Text(f"Numero squadre {num_team}"))
        for t in team:
            self._view.txt_out_squadre.controls.append(ft.Text(f"{t[0]} ({t[1]})"))
            option=ft.dropdown.Option(text=f"{t[0]}({t[1]})",key=t[2])
            self._view.dd_squadra.options.append(option)

        self._view.update()
