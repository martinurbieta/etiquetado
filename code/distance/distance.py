"""
    Input: predicciones y etiquetas
    
    Output: mapeo de realaciones entre
    los datos ingresados
"""

import sys
import ast
import os
from shapely.ops import nearest_points
from shapely.geometry import Polygon

OFFSET = 160

def get_labels_list(labels_lines):
    """
        Obtiene un listado las etiquetas
        agrupadas por columnas y vigas
    """
    column = []
    beam = []
    for line in labels_lines:
        dictionary = ast.literal_eval(line)
        if dictionary["elem"].lower().startswith("c"):
            column.append(dictionary)
        elif dictionary["elem"].lower().startswith("v"):
            beam.append(dictionary)
    return column, beam



def get_items_lists(lines):
    """
        Convierte cada linea en diccionario y 
        asigna las columnas al listado de pivotes 
        y las vigas al listado de dependientes
    """
    pivot = []
    dependent = []
    index_c = 0
    index_b = 0
    for line in lines:
        dictionary = ast.literal_eval(line)
        if dictionary["elem"] == main_dependent_element:
            dependent.append(dictionary)
            #dictionary["elem"] = dictionary["elem"] + str(index_b)
            index_b = index_b + 1
        elif dictionary["elem"] == main_pivot_element:
            pivot.append(dictionary)
            #dictionary["elem"] = dictionary["elem"] + str(index_c)
            index_c = index_c + 1
    return dependent, pivot


def assign_labels(items, labels):
    """
        Se asignan las etiquetas
        a cada elemento
    """
    for item in items:
        found = False
        item_points = item['points']
        item_poly = Polygon([(int(item_points['x1']), int(item_points['y1'])-OFFSET),
                        (int(item_points['x1']), int(item_points['y2'])-OFFSET),
                        (int(item_points['x2']), int(item_points['y1'])-OFFSET),
                        (int(item_points['x2']), int(item_points['y2'])-OFFSET)])
        for label in labels:
            label_points = label['points']
            label_poly = Polygon(label_points)
            p_1, p_2 = nearest_points(item_poly, label_poly)
            points_distance = p_1.distance(p_2)
            print(f"Label: {label['elem']} , distance: {points_distance}, element {item['tag']}")
            if points_distance < cota:
                item['tag'] = label['elem'].upper()
                labels.remove(label)
                found = True
            if found:
                break


def check_minimum_distance(predictions_path, pivot_items, dependent_items):
    """
        Obtiene los relacionados
        segun la distancia de los elementos
    """
    predictions_filename = predictions_path.split('/')[len(predictions_path.split('/')) - 1]
    #genero un archivo de texto por cada imagen de test
    predictions_filename = predictions_filename + "_relacionados" + str(cota) + '.txt'
    with open(predictions_filename,'w') as txt: #abro en modo escritura

        for pivot_item in pivot_items:
            auxpivot = pivot_item.copy()
            auxcercanos = []
            cercanos = []
            auxpivot['points'] = [(int(auxpivot['points']['x1']), int(auxpivot['points']['y1'])),
                            (int(auxpivot['points']['x1']), int(auxpivot['points']['y2'])),
                            (int(auxpivot['points']['x2']), int(auxpivot['points']['y1'])),
                            (int(auxpivot['points']['x2']), int(auxpivot['points']['y2']))]
            pivot_points = pivot_item['points']
            pivot = Polygon([(int(pivot_points['x1']), int(pivot_points['y1'])-OFFSET),
                            (int(pivot_points['x1']), int(pivot_points['y2'])-OFFSET),
                            (int(pivot_points['x2']), int(pivot_points['y1'])-OFFSET),
                            (int(pivot_points['x2']), int(pivot_points['y2'])-OFFSET)])

            for dependent_item in dependent_items:
                auxdependent = dependent_item.copy()
                dependent_points = dependent_item['points']
                dependent = Polygon(
                    [(int(dependent_points['x1']),int(dependent_points['y1'])-OFFSET),
                    (int(dependent_points['x1']),int(dependent_points['y2'])-OFFSET),
                    (int(dependent_points['x2']),int(dependent_points['y1'])-OFFSET),
                    (int(dependent_points['x2']),int(dependent_points['y2'])-OFFSET)])
                p_1, p_2 = nearest_points(pivot, dependent)

                points_distance = p_1.distance(p_2)
                #Si la distancia es menor a una cota determinada, 
                #guardo el elemento dependiente como cercano
                if points_distance < cota:
                    auxdependent['points'] = [(int(auxdependent['points']['x1']),int(auxdependent['points']['y1'])),
                    (int(auxdependent['points']['x1']),int(auxdependent['points']['y2'])),
                    (int(auxdependent['points']['x2']),int(auxdependent['points']['y1'])),
                    (int(auxdependent['points']['x2']),int(auxdependent['points']['y2']))]
                    auxcercanos.append(auxdependent)
                    cercanos.append(dependent_item)


            auxpivot["relItems"] = auxcercanos
            pivot_item["relItems"] = cercanos
            #escribo el elemento pivot con sus relacionados
            txt.write((str(auxpivot) + '\n'))

        #Aplico a la salida formato pseudo json
        txt.close()
    

def read_and_get(predictions_path):
    """
        Abre los archivos, los lee
        y llama a los metodos 
        para realizar los calculos
    """
    pivot_items_list = []
    dependent_items_list = []
    #Verifico que el archivo exista
    try:
        with open(predictions_path, 'r') as predictions_file:
            try:
                with open(main_labels_path, 'r') as labels_file:
                    #Obtengo todas las lineas
                    pred_lines = predictions_file.readlines()
                    labels_lines = labels_file.readlines()
                    #Obtengo los listados
                    dependent_items_list, pivot_items_list = get_items_lists(pred_lines)
                    column_labels, beam_labels = get_labels_list(labels_lines)

                    if main_pivot_element == "column":
                        assign_labels(pivot_items_list, column_labels)
                        assign_labels(dependent_items_list, beam_labels)
                    elif main_pivot_element == "beam":
                        assign_labels(pivot_items_list, beam_labels)
                        assign_labels(dependent_items_list, column_labels)

                    check_minimum_distance(predictions_path, pivot_items_list, dependent_items_list)
            except FileNotFoundError:
                print('El archivo de labels no existe')
                sys.exit()
    except FileNotFoundError:
        print('El archivo de predicciones no existe')
        sys.exit()

    #Verifico que el archivo exista



########################################################

#Verifico cantidad de parametros
if len(sys.argv) < 5:
    print('Falta un argumento --> predictionsFile_path labelsPath cota pivot dependent')
    sys.exit()

#Asigno los parametros
main_predictions_path = sys.argv[1]
main_labels_path = sys.argv[2]
cota = int(sys.argv[3])

main_pivot_element = sys.argv[4]
main_dependent_element = sys.argv[5]

posibles = ['beam', 'column', 'slab']

if main_pivot_element not in posibles or main_dependent_element not in posibles:
    print('Elemento pivote o dependiente invalido. Opciones: beam, column, slab')
    sys.exit()


if os.path.isdir(main_predictions_path):
    for filename in os.listdir(main_predictions_path):
        if filename.startswith("pred_") and '_relacionados' not in filename:
            main_predictions_path = os.getcwd() + '/' + filename
            print(main_predictions_path)
            read_and_get(main_predictions_path)
    print('Proceso terminado ... \n')
    sys.exit()

read_and_get(main_predictions_path)
print('Proceso terminado ... \n')

sys.exit()
