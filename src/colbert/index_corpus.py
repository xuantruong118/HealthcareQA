from colbert.infra import Run, RunConfig, ColBERTConfig
from colbert import Searcher, Indexer

import tqdm
from tqdm import tqdm
from pyvi.ViTokenizer import tokenize
import os
import torch
import json
import time 

# print(torch.cuda.is_available())
# print(os.environ.get('CUDA_PATH'))

os.environ['CUDA_VISIBLE_DEVICES'] = '0'


with open("med/data/vinmec_split.json", "r", encoding="utf-8") as f:
    corpus_raw = json.load(f)

with open('med/data/ten_benh.txt', 'r') as f:
    lines = f.readlines()
    entities = [line.strip().lower() for line in lines]

with open("med/data/drug.txt", "r", encoding="utf-8") as fd:
    data_drug = fd.readlines()
    drugs = [drug.strip().lower() for drug in data_drug]


if __name__=='__main__':
    with Run().context(RunConfig(nranks=1, experiment="default")):
        config = ColBERTConfig(
            nbits=2,
            gpus=1,
            dim=128,
            query_maxlen=128,
            doc_maxlen=256,
            similarity="cosine",
            # centroid_score_threshold=0.8
        )

        # Indexing
        indexer = Indexer(checkpoint="models/colbert", config=config)
        indexer.index(name="test_colbert_medical.2nbit", collection="data/data_training_colbert/training_data/collection.tsv", overwrite=True)
