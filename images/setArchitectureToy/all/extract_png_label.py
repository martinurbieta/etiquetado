import subprocess
import os

for filename in os.listdir(os.getcwd()):
    if os.path.isdir(filename):
        current_name = filename+"/label.png"
        new_name = filename+"/"+filename+".png"
        print(current_name)
        print(new_name)
        subprocess.run(["mv", new_name, current_name])

        #subprocess.run(["labelme_json_to_dataset", filename])
        