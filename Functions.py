from Gui import MainWindow
from PyQt6.QtWidgets import QListWidgetItem
from PyQt6.QtGui import QPixmap, QFont
import random, copy, json
import pygame
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class AppFunctions (MainWindow):

    def __init__(self):
        super().__init__()
        self.setup_function_variables()
        pygame.mixer.init()
    def setup_function_variables(self):

        self.selectedscale = {}
        self.incorrect_note_count = 0

        with open('./midi.json', 'r') as file:  self.Theory2 = json.load(file)

    def note_handler(self, mididata):

        if mididata.type == "note_on":

            print (self.octavespinbox.value())

            #self.notelabel.setText(self.Theory2["Chromatic"][(mididata.note %12)])
            # print (self.Theory2["Chromatic"])
            if mididata.note == self.goodnotes[0]:


                self.add_note_to_screen(mididata.note, "green")

                self.scalelabel2.setText(f"{self.goodnotes}")
                self.goodnotes.pop(0)  # Remove the first item
                if len(self.goodnotes) == 0: self.go_button_clicked()

            else:

                if self.incorrect_note_count > 1:
                    self.reset_button_clicked()

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
        scaletypesselected = [item.text() for item in self.theory_subtype.selectedItems()]
        if not scaletypesselected:
            self.scalelabel2.setText("You need to select at least one sub type")
            return
        if not hasattr(self, 'previous_scale'):
            self.previous_scale = None
        self.note_midi_list = self.Theory2["Enharmonic"]

        while True:
            randomnotestr = str(random.randint(0, 11))
            randomnoteint = int(randomnotestr)
            randomnoteletter = self.Theory2["Enharmonic"][randomnoteint]
            randomtype = random.choice(scaletypesselected)
            self.current_scale = f"{randomnoteletter} {randomtype}"
            if self.current_scale != self.previous_scale:
                break


        randomnotestr = str(random.randint(0,11))
        randomnoteint = int(randomnotestr)
        randomnoteletter= self.Theory2["Enharmonic"][randomnoteint]
        randomtype = random.choice(scaletypesselected)
        #print (f"Random note: {randomnotestr}")


        self.goodnotes =  (self.Theory2["Scales"][randomtype][randomnotestr])
        self.goodnotes =  (self.midi_note_scale_generator(self.goodnotes, octaves =self.octavespinbox.value()))
        self.scalelabel.setText(f"{randomnoteletter} {randomtype}")
        self.deepnotes = copy.deepcopy(self.goodnotes)
        self.current_scale = f"{randomnoteletter} {randomtype}"
        sound1 = pygame.mixer.Sound(f"sounds/{self.current_scale}.mp3")
        sound1.set_volume(0.1)  # Sets the volume to 50%
        sound1.play()
        self.previous_scale = self.current_scale
        self.scalefingering.setText(str(self.Theory2['Fingering'][randomnoteint][self.current_scale]["Right"]))

    def triads_clicked(self):
        pass

    def sevenths_clicked(self):
        pass
    def modes_clicked(self):
        pass

    def reset_button_clicked(self):
        print('trigger2')
        if hasattr(self, 'deepnotes') and self.deepnotes:
            print ('trigger2')
            self.goodnotes = copy.deepcopy(self.deepnotes)
            self.scalelabel2.setText(f"{self.goodnotes}")

    def add_note_to_screen(self,note,color):
        self.xcord = self.Theory2["NoteCoordinates"][note % 12] + ((note // 12) - 4) * 239
        self.labels[note].setPixmap(QPixmap("./Images/key_" + color + self.Theory2["NoteFilenames"][note %12]))



        self.labels[note].setGeometry(self.xcord, 128, 100, 200)
        self.labels[note].show()

    def remove_note_from_screen(self,note):
        self.labels[note].hide()

    def midi_note_scale_generator(self,notes, octaves=1, base_note=60, repeat_middle=False,harmonic_minor=False):

        adjusted_notes = [note + base_note for note in notes]
        extended_notes = adjusted_notes[:]
        for octave in range(1, octaves): extended_notes.extend([note + 12 * octave for note in adjusted_notes[1:]])
        middle_note = extended_notes[-1]
        if repeat_middle:
            reversed_notes = extended_notes[::-1]
        else:
            reversed_notes = extended_notes[:-1][::-1]
        extended_notes.extend(reversed_notes)
        print (reversed_notes)
        return extended_notes
