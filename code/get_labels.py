import os

import json


directory = "/home/colo_/Documentos/etiquetado/images/setArchitecture/labels"
dictio = {}
for filename in os.listdir(directory):
    if filename.endswith(".json"):
        # Opening JSON file
        f = open(os.path.join(directory, filename))

        # returns JSON object as
        # a dictionary
        data = json.load(f)

        for i in data["shapes"]:
            #print(i["label"])
            dictio[i["label"]] = 0
        #print(json.dumps(data, indent=4, sort_keys=True))

        # Closing file
        f.close()
    else:
        pass

for i in dictio:
    print(i)
