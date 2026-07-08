#self._controller.fillDDYear()
#certe volte bisogna aggiungere elementi come questo
#guardare sempre il self._txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
def create_alert(self, message):
    dlg = ft.AlertDialog(title=ft.Text(message))
    self._page.dialog = dlg
    dlg.open = True
    self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller


    def update_page(self):
        self._page.update()