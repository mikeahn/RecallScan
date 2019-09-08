import re
file1 = open("all.txt", "rb")
timestamps = []
for line in file1.readlines():
    # actual_line = line.rstrip('\n')
    line = str(line)

    stamp_matches = re.findall('[1][4-5][0-9]{6}[0][0]', line)
    timestamps = timestamps + stamp_matches



file1.close()
print(timestamps)
with open('all.txt', 'rb') as file:
    data = str(file.read())

    timestamp_set = set(timestamps)
    for i in timestamp_set:
        data = data.replace(i, '"'+i+'"')

    f = open("fixed.txt", "a")
    f.write(data)
