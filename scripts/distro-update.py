import json
import subprocess
import os

with open("/etc/tilingDistro/info.json") as file:
        data = json.load(file)

path = os.path.join(data['path_to_repo'], "main.py")
subprocess.run(["python3", path])
