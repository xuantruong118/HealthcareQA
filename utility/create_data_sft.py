import json
import tqdm
from tqdm import tqdm
import datasets
import numpy as np

dataset = []


with open('new/medical_qa.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    # get random 900 samples
    random_indices = np.random.choice(len(data), 900, replace=False)
    data_train = [data[i] for i in random_indices]
    data_test = [data[i] for i in range(len(data)) if i not in random_indices]
    
    print(len(data))

    for item in tqdm(data):
        messages = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": item["title"]
                },
                {
                    "role": "assistant",
                    "content": item["content"]
                }
            ]
        }

        dataset.append(messages)
        
f.close()

with open("med_test_seallm.json", "w", encoding="utf-8") as f:
    json.dump(data_test, f, ensure_ascii=False, indent=4)
    f.close()

with open("seallm_sft_med.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=4)

