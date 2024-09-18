from Gui import MainWindow
from PyQt6.QtWidgets import QListWidgetItem
from PyQt6.QtGui import QPixmap, QFont
import random, copy, json
import pygame

class AppFunctions (MainWindow):

    def __init__(self):
        super().__init__()
        self.setup_function_variables()
        pygame.mixer.init()
    def setup_function_variables(self):

        self.selectedscale = {}
        self.incorrect_note_count = 0


        self.BASE_PATH = "./Images/key_"
        self.NOTE_FILENAMES = ["_left.png", "_top.png", "_mid.png", "_top.png", "_right.png", "_left.png", "_top.png",
                               "_mid.png", "_top.png", "_mid.png", "_top.png", "_right.png", "_left.png"]
        self.NOTE_COORDINATES = [1, 26, 35, 60, 69, 103, 129, 138, 162, 172, 196, 206, 240]
        self.note_to_midi = {
            'C': 0, 'Db': 1, 'D': 2, 'Eb': 3, 'E': 4, 'F': 5, 'Gb': 6,
            'G': 7, 'Ab': 8, 'A': 9, 'Bb': 10, 'B': 11
        }
        self.notesdict = {
            0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E',
            5: 'F', 6: 'F#', 7: 'G', 8: 'G#', 9: 'A',
            10: 'A#', 11: 'B'
        }

        with open('/Users/williamcorney/Desktop/midi.json', 'r') as file:  self.Theory2 = json.load(file)

    def note_handler(self, mididata):

        if mididata.type == "note_on":
            self.notelabel.setText(self.notesdict[int(mididata.note %12)])
            if mididata.note == self.goodnotes[0]:


                self.add_note_to_screen(mididata.note, "green")

                self.scalelabel2.setText(f"{self.goodnotes}")
                self.goodnotes.pop(0)  # Remove the first item
                if len(self.goodnotes) == 0: self.go_button_clicked()

            else:

                if self.incorrect_note_count > 1: self.reset_button_clicked()
                self.add_note_to_screen(mididata.note, "red")
                self.incorrect_note_count += 1


        if mididata.type == "note_off":
            self.remove_note_from_screen(mididata.note)

            self.scalelabel2.setText(f"{self.goodnotes}")



    def go_button_clicked(self):

        self.scales_clicked()


    def theory_type_clicked(self):
        self.subtheorysubtype.clear()
        self.theory_subtype.clear()
        match self.theory_type.currentItem().text():

            case "Scales":
                self.theory_subtype.addItems(["Major", "Natural Minor", "Melodic Minor", "Harmonic Minor"])
            case "Triads":
                self.theory_subtype.addItems(["Major", "Minor"])
            case "Sevenths":
                self.theory_subtype.addItems(["Maj7", "Min7", "7", "Dim7","m7f5"])
            case "Modes":
                self.theory_subtype.addItems(["Ionian", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Aeolian","Locrian"])


    def theory_subtype_clicked(self):
        self.subtheorysubtype.clear()

        match self.theory_type.currentItem().text():
            case "Triads":
                self.subtheorysubtype.addItems(["Root", "First", "Second"])

            case "Sevenths":
                self.subtheorysubtype.addItems(["Root", "First", "Second", "Third"])

    def scales_clicked(self):
        self.theorymode = "Scales"

        randomscale =  random.randint(0, 11)
        # print (randomscale)
        # print (self.midi_note_scale_generator(self.Theory2["Scales"]["Major"][str(randomscale)]))
        scale =  ((self.Theory2['Chromatic'][int(randomscale)]))
        self.goodnotes = (self.midi_note_scale_generator(self.Theory2["Scales"]["Major"][str(randomscale)]))
        # self.selectedscale[(self.Theory2['Chromatic'][int(randomscale)])] = self.midi_note_scale_generator((self.Theory2['Scales']['Major'][str(randomscale)]))
        # print(self.selectedscale)
        self.scalelabel.setText(scale)
        self.deepnotes = copy.deepcopy(self.goodnotes)
        pass

    def triads_clicked(self):
        pass

    def sevenths_clicked(self):
        pass
    def modes_clicked(self):
        pass

    def reset_button_clicked(self):
        if hasattr(self, 'deepnotes') and self.deepnotes:

            self.goodnotes = copy.deepcopy(self.deepnotes)
            self.scalelabel2.setText(f"{self.goodnotes}")
        else:
            print("deepnotes does not exist or is empty")
    def add_note_to_screen(self,note,color):
        self.xcord = self.NOTE_COORDINATES[note % 12] + ((note // 12) - 4) * 239
        self.labels[note].setPixmap(QPixmap(self.BASE_PATH + color + self.NOTE_FILENAMES[note % 12]))
        self.labels[note].setGeometry(self.xcord, 128, 100, 200)
        self.labels[note].show()

    def remove_note_from_screen(self,note):
        self.labels[note].hide()

    def midi_note_scale_generator(self,notes, octaves=1, base_note=60, repeat_middle=False):

        adjusted_notes = [note + base_note for note in notes]
        extended_notes = adjusted_notes[:]
        for octave in range(1, octaves): extended_notes.extend([note + 12 * octave for note in adjusted_notes[1:]])
        middle_note = extended_notes[-1]
        if repeat_middle:
            reversed_notes = extended_notes[::-1]
        else:
            reversed_notes = extended_notes[:-1][::-1]
        extended_notes.extend(reversed_notes)
        return extended_notes