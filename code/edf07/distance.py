from shapely.ops import nearest_points
from shapely.geometry import Polygon
import sys
import ast
import json
import os
import re


pivotItemsList = []
dependentItemsList = []

def getLabelsList(labels_lines):
    column = []
    beam = []

    for line in labels_lines:
        dictionary = ast.literal_eval(line)
        if dictionary["elem"].lower().startswith("c"):
            column.append(dictionary)
        elif dictionary["elem"].lower().startswith("v"):
            beam.append(dictionary)

    return column, beam



def getItemsLists(lines, pivot_element, dependent_element):
    #Convierte cada linea en diccionario y asigna las columnas al listado de pivotes y las vigas al listado de dependientes
    pivot = []
    dependent = []

    index_c = 0
    index_b = 0

    for line in lines:
        dictionary = ast.literal_eval(line)
        if dictionary["elem"] == dependent_element:
            dependent.append(dictionary)
            #dictionary["elem"] = dictionary["elem"] + str(index_b)
            index_b = index_b + 1
        elif dictionary["elem"] == pivot_element:
            pivot.append(dictionary)
            #dictionary["elem"] = dictionary["elem"] + str(index_c)
            index_c = index_c + 1
    return dependent, pivot

def assignLabels(items, labels):
    for item in items:
        found = False
        item_points = item['points']
        item_poly = Polygon([(int(item_points['x1']), int(item_points['y1'])), (int(item_points['x1']), int(item_points['y2'])),
                         (int(item_points['x2']), int(item_points['y1'])), (int(item_points['x2']), int(item_points['y2']))])
        for label in labels:
            label_points = label['points']
            label_poly = Polygon(label_points)
            p1, p2 = nearest_points(item_poly, label_poly)
            points_distance = p1.distance(p2)
            print("Label{} , distance{}, element {}".format(label['elem'], points_distance, item['tag']))
            if points_distance < 200:
                item['tag'] = label['elem'].upper()
                labels.remove(label)
                found = True
            if found:
                break
    return 




def checkMinimumDistance(predictions_path, pivotItems, dependentItems):
    filename = predictions_path.split('/')[len(predictions_path.split('/')) - 1]
    print(filename)
    filename = filename + "_relacionados" + str(cota) + '.txt' #genero un archivo de texto por cada imagen de test
    txt = open(filename,'w') #abro en modo escritura

    for pivotItem in pivotItems:
        cercanos = []
        pivotPoints = pivotItem['points']
        pivot = Polygon([(int(pivotPoints['x1']), int(pivotPoints['y1'])), (int(pivotPoints['x1']), int(pivotPoints['y2'])),
                        (int(pivotPoints['x2']), int(pivotPoints['y1'])), (int(pivotPoints['x2']), int(pivotPoints['y2']))])

        for dependentItem in dependentItems:
            dependentPoints = dependentItem['points']
            dependent = Polygon([(int(dependentPoints['x1']), int(dependentPoints['y1'])), (int(dependentPoints['x1']), int(dependentPoints['y2'])),
                                 (int(dependentPoints['x2']), int(dependentPoints['y1'])), (int(dependentPoints['x2']), int(dependentPoints['y2']))])
            p1, p2 = nearest_points(pivot, dependent)

            points_distance = p1.distance(p2)
            #print("Beam: " + dependentItem['elem'] +
             #     " - Distancia: " + str(p1.distance(p2)))

            #Si la distancia es menor a una cota determinada, guardo el elemento dependiente como cercano
            if points_distance < cota:
                cercanos.append(dependentItem)


        pivotItem["relItems"] = cercanos

        txt.write((str(pivotItem) + '\n')) #escribo el elemento pivot con sus relacionados


    #Aplico a la salida formato pseudo json
    txt.close()
    return
    

def readAndGet(predictions_path, labels_path, pivot_element, dependent_element):
    #Verifico que el archivo exista
    try:
        predictions_file = open(predictions_path, 'r')
    except:
        print('El archivo de predicciones no existe')
        exit(0)

    #Verifico que el archivo exista
    try:
        labels_file = open(labels_path, 'r')
    except:
        print('El archivo de labels no existe')
        exit(0)

    #Obtengo todas las lineas
    pred_lines = predictions_file.readlines()
    labels_lines = labels_file.readlines()
    #Obtengo los listados
    dependentItemsList, pivotItemsList = getItemsLists(pred_lines, pivot_element, dependent_element)
    column_labels, beam_labels = getLabelsList(labels_lines)

    if pivot_element == "column":
        assignLabels(pivotItemsList, column_labels)
        assignLabels(dependentItemsList, beam_labels)
    elif pivot_element == "beam":
        assignLabels(pivotItemsList, beam_labels)
        assignLabels(dependentItemsList, column_labels)

    output = checkMinimumDistance(predictions_path, pivotItemsList, dependentItemsList)

########################################################

#Verifico cantidad de parametros
if len(sys.argv) < 5:
    print('Falta un argumento --> predictionsFile_path labelsPath cota pivot dependent')
    exit(0)

#Asigno los parametros
predictions_path = sys.argv[1]
labels_path = sys.argv[2]
cota = int(sys.argv[3])

pivot_element = sys.argv[4]
dependent_element = sys.argv[5]

posibles = ['beam', 'column', 'slab']

if pivot_element not in posibles or dependent_element not in posibles:
    print('Elemento pivote o dependiente invalido. Opciones: beam, column, slab')
    exit(0)


if os.path.isdir(predictions_path):
    for filename in os.listdir(predictions_path):
        if filename.startswith("pred_") and '_relacionados' not in filename:
            predictions_path = os.getcwd() + '/' + filename
            print(predictions_path)
            readAndGet(predictions_path, pivot_element, dependent_element)
    print('Proceso terminado ... \n')
    exit(0)

readAndGet(predictions_path, labels_path, pivot_element, dependent_element)
print('Proceso terminado ... \n')

#Guardo el output en relacionados.json
exit(0)