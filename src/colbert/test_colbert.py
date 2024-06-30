# from ColBERT.colbert.data import Queries
# from ColBERT.colbert.infra import Run, RunConfig, ColBERTConfig
# from ColBERT.colbert import Searcher, Indexer
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

        # # Indexing
        # indexer = Indexer(checkpoint="medical/checkpoint_colbert_2", config=config)
        # indexer.index(name="test_colbert_medical_cp2.2nbit", collection="medical/data/training_data/collection.tsv", overwrite=True)
        # indexer.index(name="for_reranker.2nbit", collection="train_v301/context_train.tsv", overwrite=True)

    # ### with Run().context(RunConfig(experiment='unsup_simcse')):
        searcher = Searcher(index="test_colbert_medical.2nbit", config=config)


    ################### TEST CASE #################
    s_time = time.time()

    query = "Bệnh gout là gì?"
    query = query.lower()
    matched_entities = [entity for entity in entities if entity in query]
    drug_entities = [entity for entity in drugs if entity in query]

    print(f"Matched entities: {matched_entities}")
    print(F"Matched drugs: {drug_entities}")

    query = tokenize(query)    
    result = searcher.search(query, k=50)
    top_ids = result[0]
    print(f"Top ids before validate entity: {top_ids}")

    top_ids_filterd = []

    for passage_id in top_ids:
        passage = corpus_raw[passage_id]["content"].lower()
        if matched_entities or drug_entities:
            # print(f"Validate entity with {len(matched_entities)} entities and {len(drug_entities)} drugs")
            if any(entity in passage for entity in matched_entities) or any(drug in passage for drug in drug_entities):
                top_ids_filterd.append(passage_id)
        else:
            top_ids_filterd.append(passage_id)

    top_ids_filterd = top_ids_filterd[:10]
        
    print("=========================================")
    print(f"Top passages after validate entity for query: {top_ids_filterd}")
    print("-" * 100)

    for passage_id in top_ids_filterd:
        print(corpus_raw[passage_id]["content"])
        print(corpus_raw[passage_id]["url"])
        print("-" * 100)


        # print(f"[{passage_id}] \t{searcher.collection[passage_id]}")
    # for passage_id, passage_rank, score in zip(*result):
    #     # print(f"[{passage_rank}]\t passage id: [{passage_id}] \t\t {searcher.collection[passage_id]}")
    #     # context = corpus[passage_id]["context"]
    #     print(corpus_raw[passage_id]["content"])
    #     print(f"[{passage_id}]\t [{passage_rank}] \t{[score]}\t {searcher.collection[passage_id]}")
    #     # print(f"[{passage_rank}]\t score: {score} \tpassage id: [{passage_id}] \n {context}")
    #     print("-" * 100)

    e_time = time.time()
    print(f"Time: {e_time - s_time}")

# --------------------------------------------------------------------------

    # ################### Evaluation #################
    # top_k = [1, 3, 5, 10, 20]


    # log = open("result_test.txt", "a", encoding="utf-8")
    # log.write("\n\n\n############### Evaluation by checkpoint combine validate keyword ################\n")

    # with open("medical/data/data_test.json", "r", encoding="utf-8") as f:
    #     data = json.load(f)
    #     total = len(data)
    #     for topk in top_k:
    #         count = 0
    #         false_question = []
    #         for idx, item in tqdm(enumerate(data)):
    #             question = item['title']
    #             positive_id = item["index"]
    #             question = question.lower()

    #             matched_entities = [entity for entity in entities if entity in question]
    #             drug_entities = [entity for entity in drugs if entity in question]

    #             question = tokenize(question)

    #             result = searcher.search(question, k=100)
    #             top_ids = result[0]

    #             top_ids_filterd = []
    #             for passage_id in top_ids:
    #                 passage = corpus_raw[passage_id]["content"].lower()
    #                 if matched_entities or drug_entities:
    #                     # print(f"Validate entity with {len(matched_entities)} entities and {len(drug_entities)} drugs")
    #                     if any(entity in passage for entity in matched_entities) or any(drug in passage for drug in drug_entities):
    #                         top_ids_filterd.append(passage_id)
    #                 else:
    #                     top_ids_filterd.append(passage_id)

    #             top_ids_filtered = top_ids_filterd[:topk]

    #             if positive_id in top_ids_filterd:
    #                 count += 1
    #             else:
    #                 false_question.append(idx)

                
            
    #         print(f"Accuracy@{topk}: {count/total}")
    #         print(f"False: {false_question}")
    #         log.write(f"Accuracy@{topk}: {count/total}\n")
    #         # log.write(f"False Retrieval: {false_question}\n==========================================================\n")
    #         print("-" * 100)
    #         print("\n")
            














# -----------------------------------------------------------------------------

    # ### create data for training reranker
    # with open("reranker_data/v2/doctrain_qrels.tsv", "r", encoding="utf-8") as qrels:
    #     qrels = qrels.readlines()
    #     qrels = [qrel.split("\t") for qrel in qrels]
    #     qrels = {qrel[0]: qrel[2] for qrel in qrels}

    # with open("reranker_data/v2/question_train.tsv", "r", encoding="utf-8") as data:
    #     queries = data.readlines()
        
    # for item in tqdm(queries):
    #     qid, query = item.split("\t")
    #     result = searcher.search(query, k=50)
    #     top_ids = result[0]
    #     positive_id = int(qrels[f"{qid}"])
    #     # remove positive id in top_ids
    #     # print(f"positive id: {positive_id}")
    #     # print(f"top ids: {top_ids}")
    #     try:
    #         top_ids.remove(positive_id)
    #     except:
    #         print(f"{positive_id} not in {top_ids}")
    #         pass
    #     with open("reranker_data/v2/querl_doc_rank.tsv", "a", encoding="utf-8") as fw:
    #         fw.write(f"{qid}\t{positive_id}\t1\n")
    #         for k in range(len(top_ids)):
    #             fw.write(f"{qid}\t{top_ids[k]}\t{k+2}\n")

# ---------------------------------------------------------------------------------

        # with open("medical/data/training_data_v2/queries.tsv", "r", encoding="utf-8") as f:
        #     queries = f.readlines()
        #     fw = open("medical/data/training_data_v2/triple_data.json", "w", encoding="utf-8")

        #     for data in tqdm(queries):
        #         q_id, question, pos_id = data.split("\t")
        #         question = question.lower()
        #         question = tokenize(question)
        #         # print(query)
        #         result = searcher.search(question, k=25)
        #         top_ids = result[0]
                
        #         for ids in top_ids:
        #             if ids != pos_id:
        #                     fw.write(f"[{int(q_id)}, {int(pos_id)}, {int(ids)}]\n")


text = """1. Nguyên nhân gây ngứa khi phát ban sốt xuất huyết\nSốt xuất huyết là bệnh truyền nhiễm được muỗi vằn Aedes Aegypti trung gian vận chuyển virus gây bệnh Dengue cho con người qua đường máu. Bệnh diễn biến nhanh và có nhiều giai đoạn, có thể trở nên nghiêm trọng nếu không chữa trị kịp thời. Những dấu hiệu điển hình khi phát ban là mệt mỏi, đau đầu chóng mặt, nhất là xuất huyết dưới da làm người mắc muốn gãi liên tục. Các nốt mẩn ngứa phát triển khắp cơ thể, đặt biệt là lòng bàn chân, bàn tay. Nguyên nhân là do sau khi cơn sốt thuyên giảm, cơ thể có xu hướng tái hấp thụ dịch ngoại bào vào máu, hình thành những mẩn ngứa. Cơn ngứa ngáy có mức độ tùy thuộc vào cơ địa, có người ngứa đến mất ăn mất ngủ, thường diễn ra trong vài ngày khi cơ thể đang trong giai đoạn phục hồi."""