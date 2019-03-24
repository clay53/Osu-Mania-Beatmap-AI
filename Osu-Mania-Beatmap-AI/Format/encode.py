import os
from mutagen.mp3 import MP3
from functions import ceil
# Format information: 
# 0: nothing
# 1: single hit
# 2: hold

resolution = 50 # ms
songLength = MP3('audio.mp3').info.length*1000 # ms

original_file = open("original.osu", "r")
original_lines = original_file.readlines()

# Remove line returns from original file
for i in range(0, len(original_lines)):
    original_lines[i] = original_lines[i].rstrip('\r\n')

original_hit_objects = original_lines[original_lines.index("[HitObjects]")+1:len(original_lines)]

poses = []
for i in range(0, len(original_hit_objects)):
    try:
        output = str(original_hit_objects[i][:-1]).split(',')
        
        # Numberize normal inputs
        for j in range(0, len(output)-1):
            output[j] = int(output[j])

        # Numberize extra inputs
        last_index = len(output)-1
        output[last_index] = output[last_index].split(':')
        for j in range(0, len(output[last_index])):
            try:
                output[last_index][j] = int(output[last_index][j])
            except Exception:
                output[last_index][j] = output[last_index][j]

        # Add to list of poses
        pose = output[0]
        if not pose in poses:
            poses.append(pose)

        # Update original array with new data
        original_hit_objects[i] = output
    except Exception:
        print("Failed to analyze line " + (i+1) + " (\"" + original_hit_objects[i] + "\") because of: " + Exception)

# Make it so you can map pos directly to a column number
poses.sort()
posToColumn = {}
for i in range(0, len(poses)):
    posToColumn[poses[i]] = i

# Create empy hit objects array
output_hit_objects = []
for i in range(0, ceil(float(songLength)/resolution)):
    val = []
    for j in range(0, len(poses)):
        val.append(0)
    output_hit_objects.append(val)

# Translate original hit objects to new hit objects
for hit_object in original_hit_objects:
    index = int(round(float(hit_object[2])/resolution))
    column = posToColumn[hit_object[0]]
    if hit_object[3] == 1 or 5:
        output_hit_objects[index][column] = 1
    if hit_object[3] == 128:
        output_hit_objects[index][column] = 2
        for i in range(index+1, ceil(float(hit_object[5][0])/resolution)-1):
            #print(i)
            output_hit_objects[i][column] = 2

# Output to file
if os.path.exists("encoded.asu"):
    os.remove("encoded.asu")
output_file = open("encoded.asu", "a")
output_file.write(str(resolution) + "\n")
for hit_object in output_hit_objects:
    #print(hit_object)
    for i in range(0, len(hit_object)):
        output_file.write(str(hit_object[i]))
        if not i == len(hit_object)-1:
            output_file.write(",")
    output_file.write("\n")