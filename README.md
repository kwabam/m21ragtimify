This project uses a corpus of ragtime pieces, stored as MIDi files, extracts the onset patterns of the melody in each song, 
and applies the data probabilistically to transform the melody of an input song into a ragtime style.

melody_extract is a small program to extract the melody via the skyline algorithm, used in _V1v2Gen.py. Music21 has a built-in
method for extracting melodies, by simply dividing melody and harmony into separate tracks, but this is a little inconsistent
with some MIDI files.

_DBuild.py generates the V1 and V2 databases. It reads in a subset of RAG-C data, generating binary onset patterns for each
midi file and storing them in a json file, keeping track of the number of times each pattern appears in the subset.

_V1v2Gen.py is the heart of the program. It uses the frequency data from the databases built from _DBuild.py, applying them
probabilitistically to a midi file input. Effectively, this shifts the melody note onset data from the input to sound more 
like a ragtime piece.

