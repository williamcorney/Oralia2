import sys

from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QListWidget, QListWidgetItem,QAbstractItemView,QSpinBox
from PyQt6.QtGui import QPixmap, QFont

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Oralia")
        self.setGeometry(500, 300, 1060, 400)
        self.setup_gui_variables()
        self.setup_buttons()
        self.setup_labels()
        self.setup_list_widgets()
        self.setup_octave_toggle()

    def setup_gui_variables (self):

        self.labels = {}
        self.buttons = {}
        self.listwidgets = {}
        self.theory_subtype_list =[]
    def setup_labels(self):

        self.labels['keys'] = QLabel(self)
        self.labels['keys'].setPixmap(QPixmap("/Users/williamcorney/PycharmProjects/Oralia/Images/keys.png"))
        self.labels['keys'].setGeometry(0, 150, 1060, 155)
        self.labels['scale'] = QLabel("", self)
        self.labels['scale'].setGeometry(0, 300, 850, 50)
        self.labels['scale'].setFont(QFont("Arial", 36))
        self.labels['scale2'] = QLabel("", self)
        self.labels['scale2'].setGeometry(0, 350, 850, 50)
        self.labels['scale2'].setFont(QFont("Arial", 14))
        self.labels['scalefingering'] = QLabel("", self)
        self.labels['scalefingering'].setGeometry(900, 350, 500, 50)
        self.labels['scalefingering'].setFont(QFont("Arial", 12))
        self.labels['note'] = QLabel("", self)
        self.labels['note'].setGeometry(900, 300, 300, 50)
        self.labels['note'].setFont(QFont("Arial", 24))
        self.labels['score'] = QLabel("1", self)
        self.labels['score'].setGeometry(600, 0, 300, 100)
        self.labels['score'].setFont(QFont("Arial", 24))

        for note in range(48, 101): self.labels[note] = QLabel(self)

    def setup_buttons(self):
        self.buttons['go'] = QPushButton("GO!", self)
        self.buttons['go'].setFont(QFont('Arial', 24))
        self.buttons['go'].setGeometry(950, 0, 50, 50)
        self.buttons['go'].setStyleSheet("background-color: green; color: white;")
        self.buttons['go'].clicked.connect(self.go_button_clicked)
        self.buttons['toggle'] = QPushButton('1', self)
        self.buttons['toggle'].setFont(QFont('Arial', 24))
        self.buttons['toggle'].setGeometry(800, 0, 40, 40)
        self.buttons['toggle'].setCheckable(True)
        self.buttons['toggle'].clicked.connect(self.octave_toggle)

    def setup_list_widgets(self):

        self.listwidgets['theory_type'] = QListWidget(self)
        self.listwidgets['theory_type'].addItems(["Notes","Scales", "Triads", "Sevenths", "Modes"])
        self.listwidgets['theory_type'].setGeometry(0, 0, 150, 125)
        self.listwidgets['theory_type'].itemSelectionChanged.connect(self.theorychanged)
        self.listwidgets['theory_type'].setCurrentRow(1)
        self.listwidgets['theory_subtype'] = QListWidget(self)
        self.listwidgets['theory_subtype'].setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.listwidgets['theory_subtype'].setGeometry(150, 0, 150, 125)
        self.listwidgets['subtheorysubtype'] = QListWidget(self)
        self.listwidgets['subtheorysubtype'].setGeometry(300, 0, 150, 125)
        self.listwidgets['subtheorysubtype'].setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.listwidgets['theory_type'].clicked.connect(self.theory_type_clicked)

        self.listwidgets['theory_subtype'].itemSelectionChanged.connect(self.theorysubtypechanged)

    def setup_octave_toggle (self):

        self.buttons['toggle'] = QPushButton('1', self)
        self.buttons['toggle'].setFont(QFont('Arial', 24))
        self.buttons['toggle'].setGeometry(800, 0, 40, 40)
        self.buttons['toggle'].setCheckable(True)
        self.buttons['toggle'].clicked.connect(self.octave_toggle)

    def octave_toggle(self):
        #  THIS DOESNT BELONG HERE.  JUST DUMPING TEMPORARILY
        self.scalehistory.clear()
        self.fiveormore.clear()
        #  THIS DOESNT BELONG HERE.  JUST DUMPING TEMPORARILY

        if self.buttons['toggle'].isChecked():
            self.buttons['toggle'].setText('2')
        else:
            self.buttons['toggle'].setText('1')
        self.go_button_clicked()
    def update_current_item(self):
            self.current_item = self.listwidgets['theory_type'].currentItem().text()

    def theorychanged (self):
        self.theorymode = (self.listwidgets['theory_type'].selectedItems()[0].text())

    def theorysubtypechanged(self):
        self.theory_subtype = self.listwidgets['theory_subtype'].selectedItems()
        self.theory_subtype_list = [item.text() for item in self.theory_subtype]

        match self.theorymode:
            case "Scales":
                pass
            case "Triads":
                self.listwidgets['subtheorysubtype'].clear()
                self.listwidgets['subtheorysubtype'].addItems(["Root", "First", "Second"])
            case "Sevenths":
                self.listwidgets['subtheorysubtype'].clear()
                self.listwidgets['subtheorysubtype'].addItems(["Root", "First", "Second", "Third"])

    def theory_type_clicked(self):
        self.listwidgets['subtheorysubtype'].clear()
        self.listwidgets['theory_subtype'].clear()
        match self.listwidgets['theory_type'].currentItem().text():

            case "Notes":
                self.listwidgets['theory_subtype'].addItems(["Naturals","Sharps","Flats","Any"])
            case "Scales":
                self.listwidgets['theory_subtype'].addItems(["Major", "Minor", "Melodic Minor", "Harmonic Minor"])
            case "Triads":
                self.listwidgets['theory_subtype'].addItems(["Major", "Minor"])
            case "Sevenths":
                self.listwidgets['theory_subtype'].addItems(["Maj7", "Min7", "7", "Dim7", "m7f5"])
            case "Modes":
                self.listwidgets['theory_subtype'].addItems(
                    ["Ionian", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Aeolian", "Locrian"])

