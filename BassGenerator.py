import random
import os
import music21 as m21
from fractions import Fraction


def generate_bass_octave(root, time):
    if time % 2 == 0:  # use root
        print("root")
        if time % 4 == 0:

            bass_note = m21.pitch.Pitch(root + "2")
            bass_octave = m21.pitch.Pitch(root + "3")
            if random.randint(1, 3) == 1:
                chord = m21.chord.Chord([bass_note])
            else:
                chord = m21.chord.Chord([bass_note, bass_octave])
        else:
            print("5th")
            bass_note = m21.pitch.Pitch(root + "2")
            bass_note = bass_note.transpose("P5")
            triad_high = bass_note.transpose("P8")
            chord = m21.chord.Chord([bass_note, triad_high])
    else:  # use 5th
        print("5th")
        bass_note = m21.pitch.Pitch(root + "3")
        bass_note = bass_note.transpose("P5")
        triad_low = bass_note.transpose("P4")
        triad_high = triad_low.transpose("M3")
        chord = m21.chord.Chord([bass_note, triad_low, triad_high])
    return chord


def generate_bassline(chord_sequence):
    note_stream = m21.stream.Part()
    time = 0
    for item in chord_sequence:
        root = item[0]
        time_end = int(item[1:])
        print(time_end, "tend")
        for time in range(time, time_end):
            note_stream.append(generate_bass_octave(root, time))
            print(time)
        time += 1
    note_stream.clef = m21.clef.BassClef()
    return note_stream


def get_duration(t):
    d = m21.duration.Duration()
    d.quarterLength = float(Fraction(t))*4
    return d.type


def get_duration_int(t):
    t = float(Fraction(t))
    return t * 4


def generate_basschord(root, duration, position):
    chord = ''
    if root == '-1':
        return m21.note.Rest(quarterLength = duration)
    elif root[-1:] is not ']':
        r = int(root)
        if r > 50:
            r -= 12
        if position == 1:
            lo = m21.note.Note(r-12, quarterLength = duration)
            hi = m21.note.Note(r, quarterLength = duration)
            chord = m21.chord.Chord([lo, hi])
        elif position == 3:
            lo = m21.note.Note(r - 5, quarterLength = duration)
            hi = m21.note.Note(r + 7, quarterLength = duration)
            chord = m21.chord.Chord([lo, hi])
        else:
            f = m21.note.Note(r+7, quarterLength = duration)
            m = m21.note.Note(r+12, quarterLength = duration)
            t = m21.note.Note(r + 16, quarterLength = duration)
            chord = m21.chord.Chord([f,m,t])
        return chord
    else:
        r = int(root[:-3])
        if r > 50:
            r -= 12
        if position == 1:
            lo = m21.note.Note(r-12, quarterLength = duration)
            hi = m21.note.Note(r, quarterLength = duration)
            chord = m21.chord.Chord([lo, hi])
        elif position == 3:
            lo = m21.note.Note(r - 5, quarterLength = duration)
            hi = m21.note.Note(r + 7, quarterLength = duration)
            chord = m21.chord.Chord([lo, hi])
        else:
            f = m21.note.Note(r + 7, quarterLength = duration)
            m = m21.note.Note(r + 12, quarterLength = duration)
            t = m21.note.Note(r + 16, quarterLength = duration)
            s = m21.note.Note(r+10, quarterLength = duration)
            chord = m21.chord.Chord([f,s,m,t])
        return chord


def read_xmk(filename):
    os.chdir('/Users/kw169/Desktop/input')
    f = open(filename)
    song_parameters = f.readline().split(']')
    timesig = song_parameters[0][1:] + "/" + song_parameters[1][1:]
    tempo = song_parameters[2][1:]
    print("Time Signature: ", timesig, "\tTempo: ", tempo)

    melody = []
    bassline = []
    x = m21.stream.Stream()
    y = m21.stream.Stream()
    offset = 0
    c = -1
    for line in f:
        line = line.rstrip()
        if line[0] == '=':
            bassline.append([])
            c += 1
            print(line)
            offset = 0
            continue

        info = line.split("\t")
        duration = get_duration_int(info[0])
        offset += duration
        melody_note = info[1]
        bass_note = info[-1]

        try:
            if melody_note == '-1':  # rest
                x.append(m21.note.Rest(quarterLength=duration))
            else:
                x.append(m21.note.Note(int(melody_note), quarterLength=duration))
            bassline[c].append((bass_note, offset - duration))
            # chord = generate_basschord(bass_note, duration, offset)
            # y.append(chord)

        except:
            continue

    for measure in bassline:
        for i in range(4):
            choice = 0
            best_d = 100
            for j in range(len(measure)):
                print(measure[j])
                d = abs(i - measure[j][1])
                if d < best_d:
                    best_d = d
                    choice = j
            try:
                chord = generate_basschord(measure[choice][0], 1, i+1)
            except:
                chord = m21.note.Note(int(melody_note), quarterLength=1)
            y.append(chord)



    full_score = m21.stream.Score()
    full_score.insert(0, x)
    full_score.insert(0, y)
    # x.show('midi')
    #full_score.show('midi')

    return x, y


if __name__ == "__main__":
    read_xmk("yankeeDb.xmk")
    # chord_sequence = ("C8", "G10", "C12", "G14", "C16")
    # bassline = generate_bassline(chord_sequence)
    # bassline.show()
