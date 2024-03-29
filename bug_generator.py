import pickle

file = open('data/sourcecode.txt')
file = file.readlines()

# Format lại data
lines = []
for line in file:
    if len(line.split()) > 0:
        lines.append(line.split())

# Tìm kiếm các hàm với 2 đối số và swap chúng
clean = []
buggy = []
for i in range(len(lines)):
    for j in range(len(lines[i])):
        if j + 4 >= len(lines[i]):
            break
        if lines[i][j] == '_OParen_' and lines[i][j+2] == '_Com_' and lines[i][j+4] == '_CParen_':
            clean.append(list(lines[i]))
            temp = list(lines[i])
            temp1 = temp[j+1]
            temp[j+1] = lines[i][j+3]
            temp[j+3] = temp1
            buggy.append(temp)

# Gây lỗi ArrayIndexOutOfBoundsException
clean = []
buggy = []
for i in range(len(lines)):
    for j in range(len(lines[i])):
        if j + 4 >= len(lines[i]):
            break
        if lines[i][j] == '_OParen_' and lines[i][j+2] == '_Com_' and lines[i][j+4] == '_CParen_':
            clean.append(list(lines[i]))
            temp = list(lines[i])
            temp1 = temp[j+1]
            temp[j+1] = lines[i][j+5]  # Gây ra lỗi ArrayIndexOutOfBoundsException
            temp[j+5] = temp1
            buggy.append(temp)

# Lưu
with open('clean.pkl', 'wb') as f:
    pickle.dump(clean, f, protocol=pickle.HIGHEST_PROTOCOL)

with open('buggy.pkl', 'wb') as f:
    pickle.dump(buggy, f, protocol=pickle.HIGHEST_PROTOCOL)

