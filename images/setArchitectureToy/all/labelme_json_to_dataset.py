import subprocess
import os

for filename in os.listdir(os.getcwd()):
    if filename.endswith(".json"):
        subprocess.run(["labelme_json_to_dataset", filename])