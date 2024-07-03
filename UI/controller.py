import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_hello(self, e):
        name = self._view.txt_name.value
        if name is None or name == "":
            self._view.create_alert("Inserire il nome")
            return
        self._view.txt_result.controls.append(ft.Text(f"Hello, {name}!"))
        self._view.update_page()

    def avvistamenti(self,e):
        if self._view.ddyear.value is None:
            self._view.create_alert('Iserire anno')
            return

        self._view.txt_result.clean()
        self._model.creagrafo(int(self._view.ddyear.value))
        self._view.txt_result.controls.append(ft.Text(f'Grafo creato'))
        self._view.txt_result.controls.append(ft.Text(f'Nodi: {self._model.getnodi()}, archi: {self._model.getarchi()}'))
        self._view.btntest.disabled=False
        self._view.percorso.disabled=False
        self.fillstati()

        self._view.update_page()

    def fillstati(self):
        s=[]
        for i in self._model.grafo.nodes:
            s.append(i)
        s.sort(key=lambda x:x.id)
        for i in s:
            self._view.ddstato.options.append(ft.dropdown.Option(key=i.id,text=i))


    def filanni(self):
        anni = self._model.getanniAvvist()
        for anno,numero in anni:
            self._view.ddyear.options.append(ft.dropdown.Option(key=anno,text=f'{anno}-->{numero}'))

    def analizz(self,e):
        if self._view.ddstato.value is None:
            self._view.create_alert('Inserire stato')
            return
        self._view.txt_result.clean()

        precedenti = self._model.predecessori(str(self._view.ddstato.value))

        self._view.txt_result.controls.append(ft.Text(f'Predecessori:', size=20,color='green'))

        for i in precedenti:
            self._view.txt_result.controls.append(ft.Text(f'{i}'))

        succ = self._model.successori(self._view.ddstato.value)
        self._view.txt_result.controls.append(ft.Text(f'Successori:', size=20,color='green'))
        for i in succ:
            self._view.txt_result.controls.append(ft.Text(f'{i}'))

        self._view.update_page()

    def seq(self,e):
        if self._view.ddstato.value is None:
            self._view.create_alert('Inserire stato')
            return
        if self._view.ddyear.value is None:
            self._view.create_alert('Iserire anno')
            return
        self._view.txt_result.clean()
        percorso=self._model.path(self._view.ddstato.value,int(self._view.ddyear.value))
        for i in percorso:
            self._view.txt_result.controls.append(ft.Text(f'{i}'))
        self._view.update_page()


