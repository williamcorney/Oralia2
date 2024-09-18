import sys

from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QListWidget, QListWidgetItem,QAbstractItemView
from PyQt6.QtGui import QPixmap, QFont

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        pass

    def setup_gui(self):
        self.setWindowTitle("Oralia")
        self.setGeometry(500, 300, 1060, 400)

    def setup_buttons(self):
        font = QFont()
        font.setPointSize(24)
        self.gobutton = QPushButton("GO!", self)
        self.gobutton.setFont(font)
        self.gobutton.setGeometry(950, 10, 50, 50)
        self.gobutton.clicked.connect(self.go_button_clicked)
        self.gobutton.setStyleSheet("background-color: green;color: white;")

    def setup_labels(self):
        self.labels = {}

        self.scalelabel = QLabel("", self)
        self.scalelabel.setGeometry(0, 300, 850, 50)
        self.scalelabel.setFont(QFont("Arial", 36))
        self.scalelabel2 = QLabel("", self)
        self.scalelabel2.setGeometry(0, 350, 850, 50)
        self.scalelabel2.setFont(QFont("Arial", 14))
        self.scalefingering = QLabel("", self)
        self.scalefingering.setGeometry(900, 350, 500, 50)
        self.scalefingering.setFont(QFont("Arial", 12))
        self.notelabel = QLabel("", self)
        self.notelabel.setGeometry(900, 300, 300, 50)
        self.notelabel.setFont(QFont("Arial", 24))

        self.labels['keys'] = QLabel(self)
        self.labels['keys'].setPixmap(QPixmap("/Users/williamcorney/PycharmProjects/Oralia/Images/keys.png"))
        self.labels['keys'].setGeometry(0, 150, 1060, 155)
        for note in range(48, 101): self.labels[note] = QLabel(self)
    def setup_listwidgets(self):
        self.theory_type = QListWidget(self)
        self.theory_subtype = QListWidget(self)
        self.subtheorysubtype = QListWidget(self)
        self.list_widget4 = QListWidget(self)

        self.theory_type.addItems(["Scales", "Triads", "Sevenths", "Modes"])
        self.theory_type.setCurrentRow(0)
        self.theory_type_clicked()
        self.theory_subtype.setCurrentRow(0)
        self.theory_type.clicked.connect(self.theory_type_clicked)
        self.theory_subtype.clicked.connect(self.theory_subtype_clicked)
        self.theory_type.setGeometry(0, 00, 150, 125)
        self.theory_subtype.setGeometry(150, 0, 150, 125)
        self.subtheorysubtype.setGeometry(300, 0, 150, 125)
        self.list_widget4.setGeometry(450, 0, 150, 125)
        self.subtheorysubtype.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.theory_subtype.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)



