import requests
from bs4 import BeautifulSoup
import json
import tqdm
from tqdm import tqdm
import time
import regex as re


def clean_text(text):
    text = text.split('\n')
    text_clean = text[0] + "\n" + " ".join(text[1:])
    text_clean = text_clean.strip()
    return text_clean

def remove_n(text):
    if text.startswith("\n"):
        text = text[1:]
    return text

def process_subtext(text):

    # Define the pattern to split by
    pattern = r"(?=\n\d+\.)"

    # Split the text by the pattern
    documents = re.split(pattern, text)
    documents = [doc for doc in documents if doc]
    documents = [clean_text(remove_n(doc)) for doc in documents]
    text_process = "\n".join(documents)

    return text_process


def abc():
    pass


split_full_text = []

with open("vinmec_full.json", "r") as f:
    data = json.load(f)

for item in tqdm(data):
    text = item["content"]
    url = item["url"]

    main_sections = re.split(r'\n(?=\d+\. )', text.strip())

    main_sections = main_sections[1:]

    documents = []
    for section in main_sections:
        # print(section)
        section = process_subtext(section)
        lines = section.split('\n')
        main_title = lines[0]
        try:
            main_title_content = lines[1]
        except:
            continue    
        if len(lines) > 2:
            for i in range(2, len(lines), 2):  # Start from 2, increment by 2
                subtitle = lines[i]
                subtitle_content = lines[i+1] if i+1 < len(lines) else ''  # Get content if exists
                documents.append(f"{main_title}\n{main_title_content}\n{subtitle}\n{subtitle_content}")
        else:
            documents.append(f"{main_title}\n{main_title_content}")

    documents = [clean_text(doc) for doc in documents]

    for doc in documents:
        title = doc.split('\n')[0].split(".")[1].strip()
        split_tet = {
            "url": url,
            "title": title,
            "content": doc
        }
        split_full_text.append(split_tet)


with open("vinmec_split.json", "w") as f:
    json.dump(split_full_text, f, ensure_ascii=False, indent=4)



























# ### Split doc by number =======> OK

# documents = re.split('\n\d+(\.\d+)?\.', text)
# # documents = re.split('\n\d+\.', text)

# # remove None in documents
# documents = [doc for doc in documents if doc]

# # remove doc with length < 2
# documents = [doc for doc in documents if len(doc.split()) > 10]
# documents = [clean_text(doc) for doc in documents]

# # Print each document
# for i, doc in enumerate(documents):
#     print(f"Document {i+1}:Length: {len(doc.split())}\n{doc}\n------------------------")

    