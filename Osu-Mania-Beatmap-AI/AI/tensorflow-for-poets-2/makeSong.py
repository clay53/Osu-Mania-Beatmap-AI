import sys
import os
import thread
import time
from mutagen.mp3 import MP3
from PIL import Image
import subprocess

path = '../'
backPeek = int(sys.argv[1]) # ms
songLength = MP3(path + 'audio.mp3').info.length*1000
originalImage = Image.open(path + 'audio.png')
pPMs = originalImage.size[0]/songLength

encoded_file = open(path + "encoded.asu", "w+")

interval = 50
encoded_file.write(str(interval) + '\n')

results = {}

sections = int(songLength/float(interval))
def do (i):
    cropped = originalImage.crop((int(round(pPMs*interval*i))-backPeek, 0, int(round(pPMs*interval*(i+1))), originalImage.size[1]))
    cropped.save(str(i) + 'tmp.png')

    response = subprocess.Popen(
        [
            "python",
            "-m",
            "scripts.label_image",
            "--graph=tf_files/retrained_graph.pb",
            "--image=" + str(i) + "tmp.png"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    stdout,stderr = response.communicate()
    lines = stdout.split('\n')
    for j in range(0, len(lines)):
        item = lines[j]
        if "Evaluation time" in item:
            result = lines[j+2][:-16].replace(' ', ',')
            print(str(i+1) + "/" + str(sections) + " - " + result)
            results[i] = (result + '\n')
            os.remove(str(i) + 'tmp.png')

maxThreads = 10
madeThreads = 0

for i in range(0, sections):
    thread.start_new_thread(do, (i,))
    madeThreads += 1
    time.sleep(0.75)
    while madeThreads-len(results) >= maxThreads:
        time.sleep(1)
while len(results) < sections:
    time.sleep(1)
print(results)
for i in range(0, len(results)):
    encoded_file.write(results[i])