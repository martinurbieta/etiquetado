import ast
from shapely.ops import nearest_points
from shapely.ops import cascaded_union
from shapely.geometry import Polygon
import geopandas as gpd

def beautyPrint(array):
    count = 0
    for i in array:
        print(i)
        count += 1
    print(f"Cantidad de elementos: {count}")

def checkMinimumDistance(pivotItems, dependentItems):
    anidados = []
    for pivotItem in pivotItems:
        cercanos = []
        min = 9999
        pivotPoints = pivotItem['points']
        pivot = Polygon([pivotPoints[0], pivotPoints[1], pivotPoints[2], pivotPoints[3]])
        
        for dependentItem in dependentItems:
            dependentPoints = dependentItem['points']
            dependent = Polygon([dependentPoints[0], dependentPoints[1], dependentPoints[2], dependentPoints[3]])
            p1, p2 = nearest_points(pivot, dependent)
            
            points_distance = p1.distance(p2)
            
            #Si la distancia es menor a una cota determinada, guardo el elemento dependiente como cercano
            if points_distance < 20:
                if points_distance < min:
                    min = points_distance
                    cercanos.append(dependentItem)
                    if 'x' not in pivotItem["elem"]:
                        pivotItem["elem"] = pivotItem["elem"] + dependentItem["elem"]
                    else:
                        pivotItem["elem"] = pivotItem["elem"].split(':')[0] + ":"+dependentItem["elem"]
                    
                    polygons = [pivot, dependent]
                    merged_box = cascaded_union(polygons).bounds
                    xmin, ymin, xmax, ymax = merged_box
                    
                    pivotItem["points"][0] = (int(xmin), int(ymin)) 
                    pivotItem["points"][1] = (int(xmin), int(ymax))
                    pivotItem["points"][2] = (int(xmax), int(ymin)) 
                    pivotItem["points"][3] = (int(xmax), int(ymax))
        
        anidados.append(pivotItem)

    return anidados


ocr_path = 'ocr/text_EDF 07-EST-04.txt'

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

filename = 'mapped_EDF 07-EST-04.txt' #genero un archivo de texto por cada imagen de test
txt = open(filename,'w')

txt.write(''.join(str(i) + '\n' for i in others))



