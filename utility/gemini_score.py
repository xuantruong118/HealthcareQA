import google.generativeai as genai
import pandas as pd
import re
import tqdm
from tqdm import tqdm
import time
from scipy.spatial.distance import cosine



genai.configure(api_key="")

for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)
print("--------------------")
model = genai.GenerativeModel('gemini-1.5-pro-latest')

data_test = pd.read_csv("[Test] MedQA_answer.csv", encoding='utf-8')


our_model_scores = []
gpt3_scores = []

for item in tqdm(data_test.iterrows()):
    question = item[1]['question']
    answer1 = item[1]['Our-model']
    answer2 = item[1]['GPT-3.5-turbo']
    answer_reference = item[1]['Reference_answer ']

    prompt = f"""
    Bạn là một bác sĩ giỏi, chuyên môn cao. Nhiệm vụ của bạn là đánh giá ba câu trả lời (hai câu trả lời cần đánh giá và một câu trả lời tham khảo) dựa trên một câu hỏi nhất định. Hãy xem xét mức độ liên quan, chính xác, đầy đủ, rõ ràng và mạch lạc của mỗi câu trả lời. Sau đó, chấm điểm cho hai câu trả lời cần đánh giá trên thang điểm từ 1 đến 10, trong đó 1 là kém nhất và 10 là tốt nhất. Sử dụng câu trả lời tham khảo như một điểm chuẩn để so sánh và đưa ra đánh giá khách quan hơn. Giải thích lý do cho điểm số của bạn.
    Câu hỏi: {question}
    Câu trả lời 1: {answer1}
    Câu trả lời 2: {answer2}
    Câu trả lời tham khảo: {answer_reference}
    """

    response = model.generate_content(prompt)
    time.sleep(10)

    # pattern = r"\*\*Điểm[:]\*\* (\d+)/10"
    pattern = r"(\d+)/10"

    # Tìm tất cả các kết quả khớp với biểu thức chính quy
    matches = re.findall(pattern, response.text)

    # Chuyển đổi các kết quả khớp thành số nguyên và lưu vào một danh sách
    scores = [int(match) for match in matches]

    our_model_scores.append(scores[0])
    gpt3_scores.append(scores[1])

    # print("Điểm câu trả lời 1:", scores[0])
    # print("Điểm câu trả lời 2:", scores[1])

print(f"Average Our-model scores: {sum(our_model_scores)/len(our_model_scores)}")
print(f"Average GPT-3.5-turbo scores: {sum(gpt3_scores)/len(gpt3_scores)}")

# add to data_test
data_test['Our-model_scores'] = our_model_scores
data_test['GPT-3.5-turbo_scores'] = gpt3_scores
# save to csv
data_test.to_csv('MedQA_answer_scores.csv', index=False)



# for m in genai.list_models():
#   if 'generateContent' in m.supported_generation_methods:
#     print(m.name)
#     print("------")

from ragas.metrics import answer_similarity
import numpy as np


def similarity_score(ground_truth, answer):
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=[ground_truth, answer],
        task_type="semantic_similarity"
    )

    embedding1 = result['embedding'][0]
    embedding2 = result['embedding'][1]

    # Calculate cosine similarity
    # Note: cosine function from scipy calculates cosine distance, not similarity, hence 1 - cosine_distance
    similarity_score = 1 - cosine(embedding1, embedding2)

    return similarity_score


data_test = pd.read_csv("MedQA_answer_scores.csv", encoding='utf-8')
data_test = data_test.dropna()

our_model_scores = 0
gpt_score = 0

for item in tqdm(data_test.iterrows()):
    answer1 = item[1]['Our-model']
    answer2 = item[1]['GPT-3.5-turbo']
    answer_reference = item[1]['Reference_answer ']

    score1 = similarity_score(answer_reference, answer1)
    score2 = similarity_score(answer_reference, answer2)

    our_model_scores += score1
    gpt_score += score2

    print(f"Semantic similarity score: {score1}")
    print(f"Semantic similarity score: {score2}")

    data_test.loc[item[0], 'Our-model_similarity_score'] = score1
    data_test.loc[item[0], 'GPT-3.5-turbo_similarity_score'] = score2


avg_our_model_scores = our_model_scores/len(data_test)
avg_gpt_score = gpt_score/len(data_test)

print(f"Average Our-model similarity scores: {avg_our_model_scores}")
print(f"Average GPT-3.5-turbo similarity scores: {avg_gpt_score}")


