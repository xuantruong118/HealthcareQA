import json
import tqdm
from tqdm import tqdm


with open("medical/data/processed_data/vinmec_href_full.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    print(len(data))
    data = [item["title"] for item in data if "/thong-tin-duoc/su-dung-thuoc-toan/" in item["link"]]
    print(len(data))
    print(data[0])

drug_file = open("medical/data/drug.txt", "a", encoding="utf-8")

for item in tqdm(data):
    token = item.split()
    item_lower = item.lower()
    token_lower = item_lower.split()
    if "thuốc" not in token_lower:
        continue
    # get token after token "thuốc"
    index = token_lower.index("thuốc")
    try:
        drug = token[index+1]
    except:
        continue
    print(drug)
    drug_file.write(drug + "\n")

