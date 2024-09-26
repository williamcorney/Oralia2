import mido,os
from PyQt6.QtWidgets import QApplication
from gui_functions import gui_functions

class MainApp(gui_functions):
    def __init__(self):
        super().__init__()


app = QApplication([])
window = MainApp()
window.show()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with mido.open_input(callback=window.note_handler) as inport: app.exec()



