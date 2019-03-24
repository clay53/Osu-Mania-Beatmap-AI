import sys
import os
from mutagen.mp3 import MP3
from PIL import Image

backPeek = int(sys.argv[1]) # ms

songs = os.listdir('./songs')

for j in range(0, len(songs)):
    path = ('./songs/' + songs[j] + '/')
    songLength = MP3(path + 'audio.mp3').info.length*1000
    originalImage = Image.open(path + 'audio.png')
    pPMs = originalImage.size[0]/songLength

    encoded_file = open(path + "encoded.asu", "r")
    encoded_file_lines = encoded_file.readlines()

    # Remove line returns from encoded file
    for i in range(0, len(encoded_file_lines)):
        encoded_file_lines[i] = encoded_file_lines[i].rstrip('\r\n')

    interval = int(encoded_file_lines[0])
    encoded_file_hit_objects = encoded_file_lines[1: len(encoded_file_lines)]

    for i in range(0, len(encoded_file_hit_objects)):
        line = encoded_file_hit_objects[i]
        cropped = originalImage.crop((int(round(pPMs*interval*i))-backPeek, 0, int(round(pPMs*interval*(i+1))), originalImage.size[1]))
        if not os.path.exists('data/' + line):
            os.makedirs('data/' + line)
        cropped.save('data/' + line + '/' + songs[j] + '-' + str(interval*i) + '.jpg')