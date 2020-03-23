import os
import json

dirs = ['biorxiv_medrxiv']

for d in dirs:
    for file in os.listdir(f"{d}/{d}"):
        print(file)
