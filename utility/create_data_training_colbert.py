import tqdm
from tqdm import tqdm
from rank_bm25 import *
import json
from pyvi.ViTokenizer import tokenize
import multiprocessing


with open("medical/data/training_data/collection.tsv") as corpus:
    corpus = corpus.readlines()


    corpus = [doc.split("\t")[1] for doc in corpus]
    tokenized_corpus = [doc.split() for doc in corpus]


bm25 = BM25Plus(tokenized_corpus, k1=1.5, b=0.75)

def get_top_n(query, top_n=25):
    tokenized_query = query.split()
    top_n_text, top_n_ids = bm25.get_top_n(tokenized_query, corpus, n=top_n)
    return top_n_ids

def create_triple_data(item):
    q_id, question, pos_id = item.split("\t")
    top_n_ids = get_top_n(item)
    triples = []

    for top_id in top_n_ids:
        if int(top_id) != int(pos_id):
            triples.append(json.dumps([int(q_id), int(pos_id), int(top_id)]))

    return triples

with open("medical/data/training_data/queries.tsv", "r") as f:
    queries = f.readlines()

with multiprocessing.Pool() as pool:
    results = list(tqdm(pool.imap(create_triple_data, queries), total=len(queries)))

with open("medical/data/training_data/trip_data.json", "w", encoding="utf-8") as triple_data:
    for triples in results:
        for triple in triples:
            triple_data.write(triple)
            triple_data.write("\n")