import os

encoded_file = open("encoded.asu", "r")
encoded_file_lines = encoded_file.readlines()

# Remove line returns from encoded file
for i in range(0, len(encoded_file_lines)):
    encoded_file_lines[i] = encoded_file_lines[i].rstrip('\n')

resolution = int(encoded_file_lines[0])
encoded_file_hit_objects = encoded_file_lines[1: len(encoded_file_lines)]

for i in range(0, len(encoded_file_hit_objects)):
    encoded_file_hit_objects[i] = encoded_file_hit_objects[i].split(',')

def find_hold_end (index, column):
    if int(encoded_file_hit_objects[index][column]) != 2 or encoded_file_hit_objects[index]:
        return index
    else:
        return(find_hold_end(index+1, column))

last_object = [0, 0, 0, 0]
output_hit_objects = []
for i in range(0, len(encoded_file_hit_objects)):
    hit_object = encoded_file_hit_objects[i]
    for j in range(0, len(hit_object)):
        column = int(hit_object[j])
        if (column == 1):
            output_hit_objects.append(str(64 + j*128) + ",192," + str(i*resolution) + ",1,0,0:0:0:0:")
        if (column == 2 and last_object[j] != 2):
            output_hit_objects.append(str(64 + j*128) + ",192," + str(i*resolution) + ",128,0," + str(find_hold_end(i, j)*resolution) + ":0:0:0:0:")
        last_object[j] = column

# Output to file
if os.path.exists("decoded.osu"):
    os.remove("decoded.osu")
output_file = open("decoded.osu", "a")
for line in output_hit_objects:
    output_file.write(line + '\r\n')