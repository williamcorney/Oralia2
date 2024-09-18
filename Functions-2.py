# import os
import json
import random
selectedscale = {}
with open('./midi.json', 'r') as file:  Theory2 = json.load(file)

def midi_note_scale_generator(notes, octaves = 2, base_note=60, repeat_middle=False):

    adjusted_notes = [note + base_note for note in notes]
    extended_notes = adjusted_notes[:]
    for octave in range(1, octaves ): extended_notes.extend([note + 12 * octave for note in adjusted_notes[1:]])
    middle_note = extended_notes[-1]
    if repeat_middle: reversed_notes = extended_notes[::-1]
    else: reversed_notes = extended_notes[:-1][::-1]
    extended_notes.extend(reversed_notes)
    return extended_notes


randomscale = random_number = random.randint(0, 11)

selectedscale[(Theory2['Chromatic'][int(randomscale)])] = midi_note_scale_generator((Theory2['Scales']['Major'][str(randomscale)]))
print (selectedscale)
