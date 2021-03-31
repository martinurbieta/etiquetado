import ast

archivo = open('file.txt', 'r')

lines = archivo.readlines()

for line in lines:
    dictionary = ast.literal_eval(line)
    #Element name 
    print(dictionay["elem"])
    #points
    print(dictionary["points"])
    #specific point [x1, x2, y1, y2]
    print(dictionary["points"]["x1"])
