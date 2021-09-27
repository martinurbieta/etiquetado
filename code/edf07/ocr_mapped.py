import ast
import sys
from shapely.ops import nearest_points
from shapely.ops import cascaded_union
from shapely.geometry import Polygon


def check_minimum_distance(pivot_items, dependent_items):
    para_anidar = []
    for pivot_item in pivot_items:
        cercanos = []
        minimo = 9999
        pivot_points = pivot_item['points']
        pivot = Polygon([pivot_points[0], pivot_points[1],
                        pivot_points[2], pivot_points[3]])
        for dependent_item in dependent_items:
            dependent_points = dependent_item['points']
            dependent = Polygon([dependent_points[0], dependent_points[1],
                                 dependent_points[2], dependent_points[3]])
            p_1, p_2 = nearest_points(pivot, dependent)
            points_distance = p_1.distance(p_2)
            # Si la distancia es menor a una cota determinada
            # guardo el elemento dependiente como cercano
            if points_distance < 20:
                if points_distance < minimo:
                    minimo = points_distance
                    cercanos.append(dependent_item)
                    pivot_elem = pivot_item["elem"]
                    dependent_elem = dependent_item["elem"]
                    if 'x' not in pivot_elem:
                        pivot_elem = pivot_elem + dependent_elem
                    else:
                        pivot_elem = f"{pivot_elem.split(':')[0]}:{dependent_elem}"
                    polygons = [pivot, dependent]
                    merged_box = cascaded_union(polygons).bounds
                    xmin, ymin, xmax, ymax = merged_box
                    pivot_item["points"][0] = (int(xmin), int(ymin))
                    pivot_item["points"][1] = (int(xmin), int(ymax))
                    pivot_item["points"][2] = (int(xmax), int(ymin))
                    pivot_item["points"][3] = (int(xmax), int(ymax))
        para_anidar.append(pivot_item)
    return para_anidar


ocr_path = 'ocr/text_EDF 07-EST-04.txt'  # pylint: disable=locally-disabled, invalid-name

try:
    with open(ocr_path, 'r') as ocr_file:
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


        anidados = ((check_minimum_distance(beams, dependents)))

        for a in anidados:
            others.append(a)

        # genero un archivo de texto por cada imagen de test # pylint: disable=locally-disabled, invalid-name
        filename = 'mapped_EDF 07-EST-04.txt'
        with open(filename, 'w') as txt:
            txt.write(''.join(str(i) + '\n' for i in others))
except FileNotFoundError:
    print('El archivo no existe')
    sys.exit()
