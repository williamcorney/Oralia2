from gui_setup import MainWindow
from PyQt6.QtWidgets import QListWidgetItem
from PyQt6.QtGui import QPixmap, QFont
import random, copy, json,pygame,os,time,pickle
os.chdir(os.path.dirname(os.path.abspath(__file__)))
class gui_functions (MainWindow):

    def __init__(self):
        super().__init__()
        self.setup_function_variables()
        pygame.mixer.init()
    def setup_function_variables(self):
        self.score = 0
        self.previous_scale = None
        self.selectedscale = {}
        self.current_scale = "None"
        self.incorrect_note_count = 0
        self.scalehistory = {}
        self.fiveormore = []
        with open('data.pkl', 'rb') as file: self.Theory2 = pickle.load(file)
        self.note_midi_list = self.Theory2["Enharmonic"]
        self.pressed_notes = []

    def note_handler(self, mididata):



        if mididata.type == "note_on":

            match self.theorymode:

                case "Notes":
                    print ('Not yet defined')

                case "Scales":
                    if mididata.note == self.goodnotes[0]:
                        self.add_note_to_screen(mididata.note,"green")
                        self.goodnotes.pop(0)
                        if len(self.goodnotes) == 0:
                            self.score_increase()
                            self.go_button_clicked()
                    else:
                        self.add_note_to_screen(mididata.note, "red")
                        self.score_decrease()
                        self.reset_scale()

                case "Triads":
                    if mididata.note in self.goodnotes:
                        self.add_note_to_screen(mididata.note,"green")
                        self.pressed_notes.append(mididata.note)
                    else:
                        self.add_note_to_screen(mididata.note, "red")
                    if len(self.pressed_notes) >= 3:
                         self.go_button_clicked()

                case "Sevenths":
                    if mididata.note in self.goodnotes:
                        self.add_note_to_screen(mididata.note, "green")
                        self.pressed_notes.append(mididata.note)
                    else:
                        self.add_note_to_screen(mididata.note, "red")
                        self.play_sound("02")
                    if len(self.pressed_notes) >= 4:
                        self.go_button_clicked()

                case "Modes":
                    if mididata.note == self.goodnotes[0]:
                        self.add_note_to_screen(mididata.note, "green")
                        self.goodnotes.pop(0)
                        if len(self.goodnotes) == 0:
                            self.go_button_clicked()
                    else:
                        self.add_note_to_screen(mididata.note, "red")
                        self.reset_scale()


        if mididata.type == "note_off":
            match self.theorymode:

                case "Notes":
                    print('Not yet defined')

                case "Scales":
                    self.remove_note_from_screen(mididata.note)
                case "Triads":
                    self.remove_note_from_screen(mididata.note)
                    self.pressed_notes.remove(mididata.note)
                case "Sevenths":
                    self.remove_note_from_screen(mididata.note)
                    self.pressed_notes.remove(mididata.note)
                case "Modes":
                    self.remove_note_from_screen(mididata.note)



    def reset_scale(self):
        if hasattr(self, 'deepnotes') and self.deepnotes:
            self.goodnotes = copy.deepcopy(self.deepnotes)


    def add_note_to_screen(self,note,color):
        self.xcord = self.Theory2["NoteCoordinates"][note % 12] + ((note // 12) - 4) * 239
        self.labels[note].setPixmap(QPixmap("./Images/key_" + color + self.Theory2["NoteFilenames"][note % 12]))
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

    def play_sound (self, sound_file):

        sound = pygame.mixer.Sound(f"sounds/{sound_file}.mp3")
        sound.set_volume(0.2)  # Sets the volume to 10%
        sound.play()
    def scale_archive(self, scale, value=1):
        if scale in (self.scalehistory): self.scalehistory[scale] += value
        else: self.scalehistory[scale] = value
        return self.scalehistory

    def go_button_clicked(self):
        #  depending the scale mode fetch the respective theory and set self.goodnotes
        self.get_theory()

    def get_theory(self):

        match self.theorymode:

            case "Scales":

                if not self.theory_subtype_list:
                    self.labels['scale2'].setText("You need to select a scale type")
                    return
                self.labels['scale2'].setText("")

                self.random_values()
                while self.current_scale == self.previous_scale:
                    self.random_values()
                self.goodnotes = ( self.midi_note_scale_generator( (self.Theory2["Scales"][self.type][self.int]), octaves=int(self.buttons['toggle'].text()), base_note=60))
                self.deepnotes = copy.deepcopy(self.goodnotes)
                self.previous_scale = self.current_scale
                self.labels['scale'].setText(self.current_scale)
                self.labels['scalefingering'].setText(str(self.Theory2['Fingering'][self.int][self.current_scale]["Right"]))

            case "Triads":
                self.scaletypesselected = [item.text() for item in self.listwidgets['theory_subtype'].selectedItems()]
                if not self.scaletypesselected:
                    self.labels['scale2'].setText("You need to select a scale type")
                    return
                self.invselected = [item.text() for item in self.listwidgets['subtheorysubtype'].selectedItems()]
                if not self.invselected:
                    self.labels['scale2'].setText("You need to select an inversion")
                    return
                self.labels['scale2'].setText("")
                self.random_values()
                while self.current_scale == self.previous_scale:
                    self.random_values()
                self.goodnotes = self.midi_note_scale_generator(
                    self.Theory2["Triads"][self.current_scale][self.inv],
                    octaves=int(self.buttons['toggle'].text()),
                    base_note=60, include_descending=False
                )
                self.current_scale = f"{self.current_scale} {self.inv}"
                self.deepnotes = copy.deepcopy(self.goodnotes)
                self.previous_scale = self.current_scale
                self.labels['scale'].setText(self.current_scale)

            case "Sevenths":
                self.scaletypesselected = [item.text() for item in self.listwidgets['theory_subtype'].selectedItems()]
                if not self.scaletypesselected:
                    self.labels['scale2'].setText("You need to select a scale type")
                    return
                self.invselected = [item.text() for item in self.listwidgets['subtheorysubtype'].selectedItems()]
                if not self.invselected:
                    self.labels['scale2'].setText("You need to select an inversion")
                    return

                self.labels['scale2'].setText("")
                self.random_values()
                while self.current_scale == self.previous_scale:
                    self.random_values()
                self.goodnotes = self.midi_note_scale_generator(
                    self.Theory2["Sevenths"][self.current_scale][self.inv],
                    octaves=int(self.buttons['toggle'].text()),
                    base_note=60, include_descending=False
                )
                self.current_scale = f"{self.current_scale} {self.inv}"
                self.deepnotes = copy.deepcopy(self.goodnotes)
                self.previous_scale = self.current_scale
                self.labels['scale'].setText(self.current_scale)
                self.play_sound(self.letter)
                self.play_sound(self.type)
            case "Modes":
                if not self.theory_subtype_list:
                    self.labels['scale2'].setText("You need to select a scale type")
                    return
                self.labels['scale2'].setText("")
                self.random_values()
                while self.current_scale == self.previous_scale:
                    self.random_values()
                self.goodnotes = (self.midi_note_scale_generator((self.Theory2["Modes"][self.letter][self.type]),
                                                                 octaves=int(self.buttons['toggle'].text()), base_note=60))
                self.deepnotes = copy.deepcopy(self.goodnotes)
                self.previous_scale = self.current_scale
                self.labels['scale'].setText(self.current_scale)

                print (self.goodnotes)




    def random_values (self):

        match self.theorymode:

            case "Scales":
                self.int = random.randint(0, 11)
                self.letter = self.Theory2["Enharmonic"][self.int]
                self.type = random.choice(self.theory_subtype_list)
                self.current_scale = f"{self.letter} {self.type}"

            case "Triads":

                self.int = random.randint(0, 11)
                self.letter = self.Theory2["Enharmonic"][self.int]
                self.type = random.choice(self.theory_subtype_list)
                self.current_scale = f"{self.letter} {self.type}"
                self.inv= random.choice(self.invselected)

            case "Sevenths":


                self.int = random.randint(0, 11)
                self.letter = self.Theory2["Enharmonic"][self.int]
                self.type = random.choice(self.theory_subtype_list)
                self.current_scale = f"{self.letter} {self.type}"
                self.inv = random.choice(self.invselected)

            case "Modes":

                self.int = random.randint(0, 11)
                self.letter = self.Theory2["Enharmonic"][self.int]
                self.type = random.choice(self.theory_subtype_list)
                self.current_scale = f"{self.letter} {self.type}"
    def score_increase(self, amount=1):
        self.score += amount
        self.labels['score'].setText(str(self.score))

    def score_decrease(self, amount =5):
        self.score -= amount
        self.labels['score'].setText(str(self.score))





