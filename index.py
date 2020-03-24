import os
import json
import pandas as pd
from tqdm import tqdm
import re
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np

style.use("ggplot")

dirs = ['biorxiv_medrxiv', 'comm_use_subset', 'noncomm_use_subset', 'pmc_custom_license']
docs = []
for d in dirs:
    for file in tqdm(os.listdir(f"{d}/{d}")):
        file_path = f"{d}/{d}/{file}"
        j = json.load(open(file_path, "rb"))

        title = j['metadata']['title']

        try:
            abstract = j['abstract'][0]
        except:
            abstract = ""

        full_text = ""
        for text in j['body_text']:
            full_text += text['text'] + '\n\n'

        docs.append([title, abstract, full_text])

    df = pd.DataFrame(docs, columns=['title', 'abstracct', 'full_text'])
    incubation = df[ df['full_text'].str.contains('incubation') ]

    texts = incubation['full_text'].values

    incubation_times = []

    for t in texts:
        for sentence in t.split(". "):
            if "incubation" in sentence:
                single_day = re.findall(r" \d{1,2} day", sentence)

                if len(single_day) == 1:
                    num = single_day[0].split(" ")
                    incubation_times.append(float(num[1]))

    print(incubation_times)
    print(len(incubation_times))

    print(f"The mean projected incubation time is {np.mean(incubation_times)}")
    plt.hist(incubation_times, bins=10)
    plt.ylabel("bin counts")
    plt.xlabel("incubation time (days)")
    plt.show()