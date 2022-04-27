# import os
# import music21 as m21
# import json
# from music21 import *
# import tensorflow.keras as keras
# import numpy as np
#
# KERN_DATASET_PATH= "deutschl/erk"
# SAVE_DIR="dataset"
# SINGLE_FILE_DATASET = "file_dataset"
# SEQUENCE_LENGTH = 64
# MAPPING_PATH="mapping.json"
#
# ACCEPTABLE_DURATIONS={
#     0.25, #16分音符
#     0.5, #8分音符
#     0.75, # 8分音符的点音符
#     1.0, #4分音符
#     1.5, #4分音符的点音符
#     2, #二分音符
#     3,
#     4
# }
#
#
# # kern,MIDI,MusicXML -> m21 -> kern, MIDI...
#
# def load_songs_in_kern(dataset_path):
#
#     songs = []
#     # go through all the files in dataset and load them with music21
#     for path,subdir,files in os.walk(dataset_path):
#     # path: 正在遍历的文件夹的名字
#     # dirs: 正在遍历的文件夹下子文件夹的集合
#     # files: 正在遍历的文件夹中的文件集合
#         for file in files:
#             if file[-3:] == "krn":
#                 song = m21.converter.parse(os.path.join(path,file))
#                 songs.append(song)
#
#     return songs
#
# def has_acceptable_durations(song,acceptable_durations):
#     for note in song.flat.notesAndRests:
#         if note.duration.quarterLength not in acceptable_durations:
#             return False
#     return True
#
# def transpose(song):
#     # get key from the song
#     parts = song.getElementsByClass(m21.stream.Part)
#     measures_part0 = parts[0].getElementsByClass(m21.stream.Measure)
#     key = measures_part0[0][4]
#
#     # estimate key using music21
#     if not isinstance(key,m21.key.Key):
#         key = song.analyze("key")
#     print(key)
#
#     # get interval for transposition. E.g..,Bmaj -> Cmaj
#     if key.mode == "major":
#         interval = m21.interval.Interval(key.tonic,m21.pitch.Pitch("C"))
#     elif key.mode == "minor":
#         interval = m21.interval.Interval(key.tonic, m21.pitch.Pitch("A"))
#
#     # transpose song by calculated interval
#     transposed_song = song.transpose(interval)
#
#     return transposed_song
#
# def encode_song(song,time_step=0.25):
#     # p=60,d=1.0->[60,"_","_","_"]
#     encoded_song=[]
#
#     for event in song.flat.notesAndRests:
#
#         # handle notes
#         if isinstance(event,m21.note.Note):
#             symbol=event.pitch.midi #60
#         # handle rest
#         elif isinstance(event,m21.note.Rest):
#             symbol="r"
#
#         #convert the note/rest into time series notation
#         steps = int(event.duration.quarterLength / time_step)
#         for step in range(steps):
#             if step == 0:
#                 encoded_song.append(symbol)
#             else:
#                 encoded_song.append("_")
#
#     # cast encoded song to string
#     encoded_song=" ".join(map(str,encoded_song))
#
#     return encoded_song
#
# def preprocess(dataset_path):
#
#     # load the fork songs
#     print("Loading songs...")
#     songs = load_songs_in_kern(dataset_path)
#     print(f"Loaded {len(songs)} songs.")
#
#     for i,song in enumerate(songs):
#
#         # filter out songs that have non-acceptable durations
#         if not has_acceptable_durations(song,ACCEPTABLE_DURATIONS):
#             continue
#
#         # transpose songs to Cmai/Amin
#         song=transpose(song)
#
#         # encode songs in music time series representation
#         encoded_song = encode_song(song)
#         # save songs to text file
#         save_path=os.path.join(SAVE_DIR,str(i))
#         with open(save_path,"w") as fp:
#             fp.write(encoded_song)
#
# def load(file_path):
#     with open(file_path,"r") as fp:
#         song = fp.read()
#     return song
#
# def create_single_file_dataset(dataset_path,file_dataset_path,sequence_length):
#     new_song_delimiter = "/ " * sequence_length
#     songs = ""
#
#     # load encoded songs and add delimiters
#     for path,_,files in os.walk(dataset_path):
#         for file in files:
#             file_path = os.path.join(path,file)
#             song = load(file_path)
#             songs = songs + song + " " + new_song_delimiter
#
#     songs = songs[:-1]
#     # save string that contain all dataset
#     with open(file_dataset_path,"w") as fp:
#         fp.write(songs)
#     return songs
#
# def create_mapping(songs,mapping_path):
#     mappings = {}
#
#     # identify the vacabulary
#     songs = songs.split()
#     vocabulary = list(set(songs))
#
#     #create mappings
#     for i,symbol in enumerate(vocabulary):
#         mappings[symbol] = i
#
#     # save the vacabulary to a json file
#     with open(mapping_path,"w") as fp:
#         json.dump(mappings,fp,indent=4)
#
# def convert_songs_to_int(songs):
#     int_songs=[]
#
#     # load mappings
#     with open(MAPPING_PATH,"r") as fp:
#         mappings = json.load(fp)
#
#     # cast songs string to a list
#     songs = songs.split()
#
#     # map songs to int
#     for symbol in songs:
#         int_songs.append(mappings[symbol])
#     return int_songs
#
# def generate_training_sequences(sequences_length):
#     # [11, 12, 13, 14, ...] -> i:[11,12], t:13  滑窗
#
#     # load songs and map them to int
#     songs = load(SINGLE_FILE_DATASET)
#     int_songs = convert_songs_to_int(songs)
#
#     # generate the training sequences
#     # 100 symbols, 64 sl, 100-64=34
#     inputs=[]
#     targets=[]
#
#     num_sequences = len(int_songs) - sequences_length
#     for i in range(num_sequences):
#         inputs.append(int_songs[i:i+sequences_length])
#         targets.append(int_songs[i+sequences_length])
#
#     # one-hot encode the sequences
#     # inputs: (# of sequences, sequence length,vocabulary_sizes)
#     vocabulary_size = len(set(int_songs))
#     inputs = keras.utils.to_categorical(inputs,num_classes=vocabulary_size)
#     targets = np.array(targets)
#
#     return inputs,targets
#
# def main():
#     preprocess(KERN_DATASET_PATH)
#     songs = create_single_file_dataset(SAVE_DIR, SINGLE_FILE_DATASET, SEQUENCE_LENGTH)
#     create_mapping(songs,MAPPING_PATH)
#     inputs,targets = generate_training_sequences(SEQUENCE_LENGTH)
#
#
#
# if __name__ == '__main__':
#     env = environment.Environment()
#     environment.Environment()['musicxmlPath'] = r'D:/software/MuseScore3/bin/MuseScore3.exe'
#     environment.Environment()['musescoreDirectPNGPath'] = r'D:/software/MuseScore3/bin/MuseScore3.exe'
#     main()



import os
import json
import music21 as m21
import numpy as np
import tensorflow.keras as keras

KERN_DATASET_PATH = "deutschl/erk"
SAVE_DIR = "dataset"
SINGLE_FILE_DATASET = "file_dataset"
MAPPING_PATH = "mapping.json"
SEQUENCE_LENGTH = 64

# durations are expressed in quarter length
ACCEPTABLE_DURATIONS = [
    0.25, # 16th note
    0.5, # 8th note
    0.75,
    1.0, # quarter note
    1.5,
    2, # half note
    3,
    4 # whole note
]


def load_songs_in_kern(dataset_path):
    """Loads all kern pieces in dataset using music21.

    :param dataset_path (str): Path to dataset
    :return songs (list of m21 streams): List containing all pieces
    """
    songs = []

    # go through all the files in dataset and load them with music21
    for path, subdirs, files in os.walk(dataset_path):
        for file in files:

            # consider only kern files
            if file[-3:] == "krn":
                song = m21.converter.parse(os.path.join(path, file))
                songs.append(song)
    return songs


def has_acceptable_durations(song, acceptable_durations):
    """Boolean routine that returns True if piece has all acceptable duration, False otherwise.

    :param song (m21 stream):
    :param acceptable_durations (list): List of acceptable duration in quarter length
    :return (bool):
    """
    for note in song.flat.notesAndRests:
        if note.duration.quarterLength not in acceptable_durations:
            return False
    return True


def transpose(song):
    """Transposes song to C maj/A min

    :param piece (m21 stream): Piece to transpose
    :return transposed_song (m21 stream):
    """

    # get key from the song
    parts = song.getElementsByClass(m21.stream.Part)
    measures_part0 = parts[0].getElementsByClass(m21.stream.Measure)
    key = measures_part0[0][4]

    # estimate key using music21
    if not isinstance(key, m21.key.Key):
        key = song.analyze("key")

    # get interval for transposition. E.g., Bmaj -> Cmaj
    if key.mode == "major":
        interval = m21.interval.Interval(key.tonic, m21.pitch.Pitch("C"))
    elif key.mode == "minor":
        interval = m21.interval.Interval(key.tonic, m21.pitch.Pitch("A"))

    # transpose song by calculated interval
    tranposed_song = song.transpose(interval)
    return tranposed_song


def encode_song(song, time_step=0.25):
    """Converts a score into a time-series-like music representation. Each item in the encoded list represents 'min_duration'
    quarter lengths. The symbols used at each step are: integers for MIDI notes, 'r' for representing a rest, and '_'
    for representing notes/rests that are carried over into a new time step. Here's a sample encoding:

        ["r", "_", "60", "_", "_", "_", "72" "_"]

    :param song (m21 stream): Piece to encode
    :param time_step (float): Duration of each time step in quarter length
    :return:
    """

    encoded_song = []

    for event in song.flat.notesAndRests:

        # handle notes
        if isinstance(event, m21.note.Note):
            symbol = event.pitch.midi # 60
        # handle rests
        elif isinstance(event, m21.note.Rest):
            symbol = "r"

        # convert the note/rest into time series notation
        steps = int(event.duration.quarterLength / time_step)
        for step in range(steps):

            # if it's the first time we see a note/rest, let's encode it. Otherwise, it means we're carrying the same
            # symbol in a new time step
            if step == 0:
                encoded_song.append(symbol)
            else:
                encoded_song.append("_")

    # cast encoded song to str
    encoded_song = " ".join(map(str, encoded_song))

    return encoded_song


def preprocess(dataset_path):

    # load folk songs
    print("Loading songs...")
    songs = load_songs_in_kern(dataset_path)
    print(f"Loaded {len(songs)} songs.")

    for i, song in enumerate(songs):

        # filter out songs that have non-acceptable durations
        if not has_acceptable_durations(song, ACCEPTABLE_DURATIONS):
            continue

        # transpose songs to Cmaj/Amin
        song = transpose(song)

        # encode songs with music time series representation
        encoded_song = encode_song(song)

        # save songs to text file
        save_path = os.path.join(SAVE_DIR, str(i))
        with open(save_path, "w") as fp:
            fp.write(encoded_song)

        if i % 10 == 0:
            print(f"Song {i} out of {len(songs)} processed")


def load(file_path):
    with open(file_path, "r") as fp:
        song = fp.read()
    return song


def create_single_file_dataset(dataset_path, file_dataset_path, sequence_length):
    """Generates a file collating all the encoded songs and adding new piece delimiters.

    :param dataset_path (str): Path to folder containing the encoded songs
    :param file_dataset_path (str): Path to file for saving songs in single file
    :param sequence_length (int): # of time steps to be considered for training
    :return songs (str): String containing all songs in dataset + delimiters
    """

    new_song_delimiter = "/ " * sequence_length
    songs = ""

    # load encoded songs and add delimiters
    for path, _, files in os.walk(dataset_path):
        for file in files:
            file_path = os.path.join(path, file)
            song = load(file_path)
            songs = songs + song + " " + new_song_delimiter

    # remove empty space from last character of string
    songs = songs[:-1]

    # save string that contains all the dataset
    with open(file_dataset_path, "w") as fp:
        fp.write(songs)

    return songs


def create_mapping(songs, mapping_path):
    """Creates a json file that maps the symbols in the song dataset onto integers

    :param songs (str): String with all songs
    :param mapping_path (str): Path where to save mapping
    :return:
    """
    mappings = {}

    # identify the vocabulary
    songs = songs.split()
    vocabulary = list(set(songs))

    # create mappings
    for i, symbol in enumerate(vocabulary):
        mappings[symbol] = i

    # save voabulary to a json file
    with open(mapping_path, "w") as fp:
        json.dump(mappings, fp, indent=4)


def convert_songs_to_int(songs):
    int_songs = []

    # load mappings
    with open(MAPPING_PATH, "r") as fp:
        mappings = json.load(fp)

    # transform songs string to list
    songs = songs.split()

    # map songs to int
    for symbol in songs:
        int_songs.append(mappings[symbol])

    return int_songs


def generate_training_sequences(sequence_length):
    """Create input and output data samples for training. Each sample is a sequence.

    :param sequence_length (int): Length of each sequence. With a quantisation at 16th notes, 64 notes equates to 4 bars

    :return inputs (ndarray): Training inputs
    :return targets (ndarray): Training targets
    """

    # load songs and map them to int
    songs = load(SINGLE_FILE_DATASET)
    int_songs = convert_songs_to_int(songs)

    inputs = []
    targets = []

    # generate the training sequences
    num_sequences = len(int_songs) - sequence_length
    for i in range(num_sequences):
        inputs.append(int_songs[i:i+sequence_length])
        targets.append(int_songs[i+sequence_length])

    # one-hot encode the sequences
    vocabulary_size = len(set(int_songs))
    # inputs size: (# of sequences, sequence length, vocabulary size)
    inputs = keras.utils.to_categorical(inputs, num_classes=vocabulary_size)
    targets = np.array(targets)

    print(f"There are {len(inputs)} sequences.")

    return inputs, targets


def main():
    preprocess(KERN_DATASET_PATH)
    songs = create_single_file_dataset(SAVE_DIR, SINGLE_FILE_DATASET, SEQUENCE_LENGTH)
    create_mapping(songs, MAPPING_PATH)
    #inputs, targets = generate_training_sequences(SEQUENCE_LENGTH)


if __name__ == "__main__":
    main()


