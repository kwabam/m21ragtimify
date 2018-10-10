import music21 as m21

def generateBassOctave(root, time):
    if time%2 == 0: #use root
        bass_note = m21.pitch.Pitch(root + "3")
        bass_octave = m21.pitch.Pitch(root + "4")
        chord = m21.chord.Chord([bass_note,bass_octave])
    else: #use 5th
        bass_note = m21.pitch.Pitch(root + "3")
        bass_note = bass_note.transpose("P5")
        triad_low = bass_note.transpose("P4")
        triad_high = triad_low.transpose("M3")
        chord = m21.chord.Chord([bass_note, triad_low,triad_high])
    return chord
def generateHighChord(root):
    return 0


if __name__ == "__main__":
    note_stream = m21.stream.Stream()
    chord_sequence = ("C4", "F8", "C14", "G22")
    time = 0
    for item in chord_sequence:
        root = item[0]
        time_end = int(item[1:])
        print(time_end, "tend")
        for time in range(time,time_end):
            note_stream.append(generateBassOctave(root, time))
            print(time)

    note_stream.show()