import ast
from shapely.ops import nearest_points
from shapely.geometry import box
from shapely.ops import unary_union
from shapely.geometry import Polygon
import geopandas as gpd

def beautyPrint(array):
    for i in array:
        print(i)

def checkMinimumDistance(pivotItems, dependentItems):

    filename = '/home/colo_/Escritorio/EDF07/unido.txt' #genero un archivo de texto por cada imagen de test
    txt = open(filename,'w') #abro en modo escritura
    anidados = []
    for pivotItem in pivotItems:
        cercanos = []
        pivotPoints = pivotItem['points']
        pivot = Polygon([(int(pivotPoints['x1']), int(pivotPoints['y1'])), (int(pivotPoints['x1']), int(pivotPoints['y2'])),
                        (int(pivotPoints['x2']), int(pivotPoints['y1'])), (int(pivotPoints['x2']), int(pivotPoints['y2']))])
        
        pivot_box = box(int(pivotPoints['x1']), int(pivotPoints['y1']), int(pivotPoints['x2']), int(pivotPoints['y2']))
        
        for dependentItem in dependentItems:
            dependentPoints = dependentItem['points']
            dependent = Polygon([(int(dependentPoints['x1']), int(dependentPoints['y1'])), (int(dependentPoints['x1']), int(dependentPoints['y2'])),
                                 (int(dependentPoints['x2']), int(dependentPoints['y1'])), (int(dependentPoints['x2']), int(dependentPoints['y2']))])
            p1, p2 = nearest_points(pivot, dependent)

            dependent_box = box(int(dependentPoints['x1']), int(dependentPoints['y1']), int(dependentPoints['x2']), int(dependentPoints['y2']))
            
            points_distance = p1.distance(p2)
            #print("Beam: " + dependentItem['elem'] +
             #     " - Distancia: " + str(p1.distance(p2)))

            #Si la distancia es menor a una cota determinada, guardo el elemento dependiente como cercano
            if points_distance < 3:
                boxes = [pivot_box, dependent_box]
                union = unary_union(boxes)
                print(union)
                pivotItem["elem"] = pivotItem["elem"] + dependentItem["elem"]
                cercanos.append(dependentItem)

        #pivotItem["relItems"] = cercanos
        txt.write((str(pivotItem) + '\n')) #escribo el elemento pivot con sus relacionados
        anidados.append(pivotItem)
    return anidados


ocr_path = '/home/colo_/Escritorio/EDF07/text_EDF 07-EST-01.txt'

try:
    ocr_file = open(ocr_path, 'r')
except:
    print('El archivo no existe')
    exit(0)

beams = []
dependents = []
others = []

for line in ocr_file:
    dictionary = ast.literal_eval(line)
    elem = dictionary['elem']
    if elem.lower().startswith('v') and elem.endswith(':'):
        beams.append(dictionary)
    elif elem[0].isnumeric() and len(elem) <= 7 and len(elem) >= 5:
        dependents.append(dictionary)
    else:
        others.append(dictionary)


#beautyPrint(others)
anidados = ((checkMinimumDistance(beams, dependents)))

for i in anidados:
    others.append(i)

#beautyPrint(others)


