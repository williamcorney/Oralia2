import mido

from PyQt6.QtWidgets import QApplication
from Functions import AppFunctions

class MainApp(AppFunctions):
    def __init__(self):
        super().__init__()

        self.setup_gui()
        self.setup_buttons()
        self.setup_labels()
        self.setup_listwidgets()
        #self.goodnotes = [70]

        self.theorymode = "Scales"

        self.scales_clicked()


    def midi_callback(self, message):
        self.note_handler(message)


app = QApplication([])
window = MainApp()
window.show()

with mido.open_input( callback=window.midi_callback) as inport: app.exec()



