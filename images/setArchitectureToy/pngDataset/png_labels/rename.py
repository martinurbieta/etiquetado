import subprocess
import os

for filename in os.listdir(os.getcwd()):
    end = len(filename) - len(filename.split("_")[len(filename.split("_"))-1]) -1
    #print(end)
    new_name = filename[0:end]+".png"
    subprocess.run(["mv", filename, new_name ])
    #print(filename.split("_")[0] + ".png")