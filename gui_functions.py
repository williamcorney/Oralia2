from gui_setup import MainWindow
from PyQt6.QtWidgets import QListWidgetItem
from PyQt6.QtGui import QPixmap, QFont
import random, copy, json
import pygame
import os
import time
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class gui_functions (MainWindow):

    def __init__(self):
        super().__init__()
        self.setup_function_variables()
        pygame.mixer.init(frequency=88200)
    def setup_function_variables(self):

        self.selectedscale = {}
        self.current_scale = "None"
        self.incorrect_note_count = 0
        self.scalehistory = {}
        self.fiveormore = []
        with open('./midi.json', 'r') as file:  self.Theory2 = json.load(file)

    def note_handler(self, mididata):
        if self.theorymode == "Scales" or self.theorymode == "Modes":
            if mididata.type == "note_on":
                if mididata.note in self.goodnotes:
                    if mididata.note == self.goodnotes[0]:
                        self.add_note_to_screen(mididata.note, "green")
                        #self.labels['scale2'].setText(f"{self.goodnotes}")
                        self.goodnotes.pop(0)  # Remove the first item
                        #self.labels['scale2'].setText(f"{self.goodnotes}")

                        if len(self.goodnotes) == 0:
                            self.scale_archive(self.current_scale)
                            self.go_button_clicked()
                            print(self.check_values())
                            self.labels['fiveormore'].setText(str(self.calculate_difference(self.fiveormore)))
                    else:
                        self.add_note_to_screen(mididata.note, "green")
                else:
                    if self.incorrect_note_count > 0:
                        self.reset_scale()
                    print(f"after reset : {self.goodnotes}")
                    self.add_note_to_screen(mididata.note, "red")
                    self.incorrect_note_count += 1

            if mididata.type == "note_off":
                self.remove_note_from_screen(mididata.note)

                #self.labels['scale2'].setText(f"{self.goodnotes}")

        if self.theorymode == "Triads" or self.theorymode == "Sevenths":

            if mididata.type == "note_on":
                if mididata.note in self.goodnotes:


                    self.add_note_to_screen(mididata.note, "green")

                    self.labels['scale2'].setText(f"{self.goodnotes}")
                    self.goodnotes.remove(mididata.note)
                    self.labels['scale2'].setText(f"{self.goodnotes}")

                    if len(self.goodnotes) == 0:
                        self.go_button_clicked()


                else:

                    if self.incorrect_note_count > 5:
                        self.reset_scale()

                    self.add_note_to_screen(mididata.note, "red")
                    self.incorrect_note_count += 1

            if mididata.type == "note_off":
                self.remove_note_from_screen(mididata.note)

                self.labels['scale2'].setText(f"{self.goodnotes}")


    def theory_type_clicked(self):
        self.listwidgets['subtheorysubtype'].clear()
        self.listwidgets['theory_subtype'].clear()
        match self.listwidgets['theory_type'].currentItem().text():

            case "Scales": self.listwidgets['theory_subtype'].addItems(["Major", "Natural Minor", "Melodic Minor", "Harmonic Minor"])
            case "Triads": self.listwidgets['theory_subtype'].addItems(["Major", "Minor"])
            case "Sevenths": self.listwidgets['theory_subtype'].addItems(["Maj7", "Min7", "7", "Dim7","m7f5"])
            case "Modes": self.listwidgets['theory_subtype'].addItems(["Ionian", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Aeolian","Locrian"])

    def theory_subtype_clicked(self):
        self.listwidgets['subtheorysubtype'].clear()

        match self.listwidgets['theory_type'].currentItem().text():
            case "Triads": self.listwidgets['subtheorysubtype'].addItems(["Root", "First", "Second"])
            case "Sevenths": self.listwidgets['subtheorysubtype'].addItems(["Root", "First", "Second", "Third"])

    def reset_scale(self):
        if hasattr(self, 'deepnotes') and self.deepnotes:
            self.goodnotes = copy.deepcopy(self.deepnotes)
            #self.labels['scale2'] .setText(f"{self.goodnotes}")

    def add_note_to_screen(self,note,color):
        self.xcord = self.Theory2["NoteCoordinates"][note % 12] + ((note // 12) - 4) * 239
        self.labels[note].setPixmap(QPixmap("./Images/key_" + color + self.Theory2["NoteFilenames"][note %12]))

        self.labels[note].setGeometry(self.xcord, 128, 100, 200)
        self.labels[note].show()

    def remove_note_from_screen(self,note):
        self.labels[note].hide()

    def midi_note_scale_generator(self, notes, octaves=1, base_note=60, repeat_middle=False, include_descending=True):
        adjusted_notes = [note + base_note for note in notes]
        extended_notes = adjusted_notes[:]

        for octave in range(1, octaves):
            extended_notes.extend([note + 12 * octave for note in adjusted_notes[1:]])

        if include_descending:
            if repeat_middle:
                reversed_notes = extended_notes[::-1]
            else:
                reversed_notes = extended_notes[:-1][::-1]
            extended_notes.extend(reversed_notes)

        return extended_notes

    def label_update (self, item, text):
        self.item = item

        self.item.setText(text)

        pass

    def get_finger_changes(self,notes):

            result = []
            add_next = True  # Flag to add the first note

            for note in notes:
                if add_next:
                    result.append(note)
                    add_next = False  # Reset the flag after adding the first note
                if note == 1:
                    add_next = True  # Set the flag to add the next note after '1'

            return result

    def play_sound (self, sound_file):

        sound = pygame.mixer.Sound(f"sounds/{sound_file}.mp3")
        sound.set_volume(0.2)  # Sets the volume to 10%
        sound.play()

    def scale_archive(self, scale, value=1):
        if scale in (self.scalehistory):
            self.scalehistory[scale] += value
        else:
            self.scalehistory[scale] = value
        return self.scalehistory



    def go_button_clicked(self):

        self.goodnotes = []

        self.number = 0

        match self.listwidgets['theory_type'].currentItem().text():
            case 'Scales':
                self.scales_clicked()
            case 'Triads':
                self.triads_clicked()
            case 'Sevenths':
                self.sevenths_clicked()
            case 'Modes':
                self.modes_clicked()

    def scales_clicked(self):
        self.theorymode = "Scales"
        #self.labels['scale2'].clear()
        scaletypesselected = [item.text() for item in self.listwidgets['theory_subtype'].selectedItems()]
        if not scaletypesselected:
            self.labels['scale2'].setText("You need to select at least one sub type")
            return
        if not hasattr(self, 'previous_scale'):
            self.previous_scale = None
        self.note_midi_list = self.Theory2["Enharmonic"]
        number = 0
        randomnotestr = str(random.randint(0, 11))
        randomnoteint = int(randomnotestr)
        randomnoteletter = self.Theory2["Enharmonic"][randomnoteint]
        randomtype = random.choice(scaletypesselected)
        while self.current_scale == self.previous_scale:
            number += 1
            randomnotestr = str(random.randint(0, 11))
            randomnoteint = int(randomnotestr)
            randomnoteletter = self.Theory2["Enharmonic"][randomnoteint]
            randomtype = random.choice(scaletypesselected)
            self.current_scale = f"{randomnoteletter} {randomtype}"
        number = 0
        # randomnotestr = str(random.randint(0, 11))
        # randomnoteint = int(randomnotestr)
        # randomnoteletter = self.Theory2["Enharmonic"][randomnoteint]
        # randomtype = random.choice(scaletypesselected)
        self.goodnotes = (self.Theory2["Scales"][randomtype][randomnotestr])
        self.goodnotes = (
            self.midi_note_scale_generator(self.goodnotes, octaves=int(self.buttons['toggle'].text()), base_note=60))
        #self.labels['scale2'].setText(f"{self.goodnotes}")

        self.labels['scale'].setText(f"{randomnoteletter} {randomtype}")
        self.deepnotes = copy.deepcopy(self.goodnotes)
        self.current_scale = f"{randomnoteletter} {randomtype}"
        self.play_sound(self.current_scale)
        self.previous_scale = self.current_scale
        self.labels['scalefingering'].setText(
            str(self.Theory2['Fingering'][randomnoteint][self.current_scale]["Right"]))

    def triads_clicked(self):
        try:

            self.theorymode = "Triads"
            self.labels['scale2'].clear()
            scaletypesselected = [item.text() for item in self.listwidgets['theory_subtype'].selectedItems()]
            inversionselected = [item.text() for item in self.listwidgets['subtheorysubtype'].selectedItems()]

            if not scaletypesselected or not inversionselected:
                self.labels['scale2'].setText("You need to select at least one sub type")
                return

            randomnotestr = str(random.randint(0, 11))
            randomnoteint = int(randomnotestr)
            randomnoteletter = self.Theory2["Enharmonic"][randomnoteint]
            randomtype = random.choice(scaletypesselected)
            randominversion = random.choice(inversionselected)
            self.current_scale = f"{randomnoteletter} {randomtype}"

            self.goodnotes = copy.deepcopy(self.Theory2['Triads'][randomnoteletter + " " + randomtype][randominversion])
            self.goodnotes = (
                self.midi_note_scale_generator(self.goodnotes, octaves=1, base_note=60, include_descending=False))

            self.deepnotes = copy.deepcopy(self.goodnotes)
            self.labels['scale'].setText("")
            self.labels['scale2'].setText("")
            if randomtype == "Minor":
                self.play_sound(f"{randomnoteletter} Natural {randomtype}")
            else:
                self.play_sound(f"{randomnoteletter} {randomtype}")

            self.labels['scale'].setText(self.current_scale + " " + randominversion)
            self.labels['scale2'].setText(f"{self.goodnotes}")
            self.play_sound(randominversion)



        except Exception as e:
            self.labels['scale2'].setText(f"An error occurred: {e}")

    def sevenths_clicked(self):
        try:

            self.theorymode = "Sevenths"
            self.labels['scale2'].clear()
            scaletypesselected = [item.text() for item in self.listwidgets['theory_subtype'].selectedItems()]
            inversionselected = [item.text() for item in self.listwidgets['subtheorysubtype'].selectedItems()]

            if not scaletypesselected or not inversionselected:
                self.labels['scale2'].setText("You need to select at least one sub type")
                return

            randomnotestr = str(random.randint(0, 11))
            randomnoteint = int(randomnotestr)
            randomnoteletter = self.Theory2["Enharmonic"][randomnoteint]
            randomtype = random.choice(scaletypesselected)
            randominversion = random.choice(inversionselected)
            self.current_scale = f"{randomnoteletter} {randomtype}"

            self.goodnotes = copy.deepcopy(
                self.Theory2['Sevenths'][0][randomnoteletter + " " + randomtype][randominversion])
            self.goodnotes = (self.midi_note_scale_generator(self.goodnotes, octaves=int(self.buttons['toggle'].text()),
                                                             base_note=60, include_descending=False))
            self.labels['scale'].setText(self.current_scale + " " + randominversion)
            self.labels['scale2'].setText(f"{self.goodnotes}")
            self.deepnotes = copy.deepcopy(self.goodnotes)
            # self.play_sound(randomnoteletter)
            # self.play_sound(randomtype)
        except Exception as e:
            self.labels['scale2'].setText(f"An error occurred: {e}")

    def modes_clicked(self):
        try:
            self.theorymode = "Modes"
            scaletypesselected = [item.text() for item in self.listwidgets['theory_subtype'].selectedItems()]
            if not scaletypesselected:
                self.label['scale2'].setText("You need to select at least one sub type")
                return

            randomnotestr = str(random.randint(0, 11))
            randomnoteint = int(randomnotestr)

            randomnoteletter = self.Theory2["Enharmonic"][randomnoteint]

            randomtype = random.choice(scaletypesselected)
            self.current_scale = f"{randomnoteletter} {randomtype}"

            self.goodnotes = copy.deepcopy(self.Theory2['Modes'][0][randomnoteletter][randomtype])
            self.goodnotes = (self.midi_note_scale_generator(self.goodnotes, octaves=int(self.buttons['toggle'].text()),
                                                             base_note=60))
            self.labels['scale'].setText(self.current_scale)
            self.labels['scale2'].setText(f"{self.goodnotes}")
            self.deepnotes = copy.deepcopy(self.goodnotes)
            self.play_sound(randomnoteletter)
            self.play_sound(randomtype)
        except Exception as e:
            self.labels['scale2'].setText(f"An error occurred: {e}")

    def check_values(self, threshold=2):
        for key, value in self.scalehistory.items():
            if value >= threshold and key not in self.fiveormore:
                self.fiveormore.append(key)
        return self.fiveormore

    def calculate_difference(self,input_list):
        list_length = len(input_list)
        return 11 - list_length
