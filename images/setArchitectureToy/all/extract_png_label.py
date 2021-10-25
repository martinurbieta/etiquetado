import subprocess
import os

for filename in os.listdir(os.getcwd()):
    if os.path.isdir(filename):
        if(filename != "png_labels"):
            current_name = filename+"/label.png"
            new_name = filename+"/"+filename+".png"
            #print(current_name)
            print(new_name)
            #subprocess.run(["mv", current_name, new_name])
            subprocess.run(["cp", new_name, "png_labels"])

            #subprocess.run(["labelme_json_to_dataset", filename])
        