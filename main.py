from music21 import *
env = environment.Environment()




# # for key in env.keys():
# #     print(key)
print('musicXML:  ', env['musicxmlPath'])
print('musescore: ', env['musescoreDirectPNGPath'])
environment.Environment()['musicxmlPath'] = r'D:/software/MuseScore 3/bin/MuseScore3.exe'
environment.Environment()['musescoreDirectPNGPath'] = r'D:/software/MuseScore 3/bin/MuseScore3.exe'
print('musicXML:  ', env['musicxmlPath'])
print('musescore: ', env['musescoreDirectPNGPath'])
n = note.Note("D#3")
n.duration.type = 'half'
n.show()