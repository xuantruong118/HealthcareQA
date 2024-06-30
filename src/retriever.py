from fastapi import FastAPI, Query, Depends, HTTPException, status, Header
from functools import lru_cache
import os
import json
from dotenv import load_dotenv
from fastapi.security import HTTPBearer
import uvicorn
from colbert import Searcher
from pyvi.ViTokenizer import tokenize

load_dotenv()

INDEX_NAME = os.getenv("INDEX_NAME")
INDEX_ROOT = os.getenv("INDEX_ROOT")
API_SECRET_TOKEN = os.environ.get("API_SECRET_TOKEN", "abcd1234")

oauth2_scheme = HTTPBearer()  # use token authentication

with open("med/data/vinmec_split.json", "r", encoding="utf-8") as f:
    corpus_raw = json.load(f)

with open('med/data/ten_benh.txt', 'r') as f:
    lines = f.readlines()
    entities = [line.strip().lower() for line in lines]

with open("med/data/drug.txt", "r", encoding="utf-8") as fd:
    data_drug = fd.readlines()
    drugs = [drug.strip().lower() for drug in data_drug]

def api_key_auth(api_key=Depends(oauth2_scheme)):
    api_keys = [API_SECRET_TOKEN]
    if api_key.credentials not in api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization Failed"
        )

app = FastAPI()

print(f'index_name: {INDEX_NAME}')
print(f'index_root: {INDEX_ROOT}')
print("Loading the searcher...")

searcher = Searcher(index=INDEX_NAME, index_root=INDEX_ROOT)
counter = {"api" : 0}

@lru_cache(maxsize=1000000)
def api_search_query(query, top_k):
    print(f"Query={query}")
    query = query.lower()
    matched_entities = [entity for entity in entities if entity in query]
    drug_entities = [entity for entity in drugs if entity in query]    
    if top_k == None: top_k = 10
    top_k = min(int(top_k), 100)
    query = tokenize(query)
    pids, ranks, scores = searcher.search(query, k=100)
    top_ids_filtered = []
    
    for pid in pids:
        passage = corpus_raw[pid]["content"].lower()
        if matched_entities or drug_entities:
            if any(entity in passage for entity in matched_entities) or any(drug in passage for drug in drug_entities):
                top_ids_filtered.append(pid)
        else:
            top_ids_filtered.append(pid)
            
    top_ids_filtered = top_ids_filtered[:top_k]
        
    topk = []
    for pid in top_ids_filtered:
        text = corpus_raw[pid]       
        # text = searcher.collection[pid]     
        d = {'text': text, 'pid': pid}
        topk.append(d)
    print(f"Topk: \n{topk}")
        
    return topk

@app.get("/api/search")
def api_search(query: str, k: int = 10, api_key: str = Depends(api_key_auth)):
    counter["api"] += 1
    print("API request count:", counter["api"])
    return api_search_query(query, k)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("RETRIEVER_PORT", 5678)))