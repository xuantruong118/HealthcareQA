import requests
import json
import pandas as pd
import tqdm
from tqdm import tqdm
import time
import openai
from openai import OpenAI


def get_anwser(question):
    url = "https://litellm.dev.ftech.ai/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        'Authorization': 'Bearer sk-aoAA3GLIpOGywPeTgW3WYw '
    }

    data = {
        "messages": [
            {
                "role": "user",
                "content": f"{question}"
            }
        ],
        "temperature": 0.2,
        "top_p": 0.9,
        "stream": False,
        "model": "gpt-3.5-turbo"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    response = response.json()
    print(response)
    print("--------------------------------------\n")
    response = response['choices'][0]['message']['content']

    return response

# def get_openai_answer(question):
#     client = OpenAI(api_key="sk-proj-0wrGp7yOyzizaesDGYzCT3BlbkFJHAXbiRx1XV6vmtKsh7gd")

#     response = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {
#             "role": "user",
#             "content": "Who won the world series in 2020?"
#         }
#     ]
#     )

#     response = response.choices[0].text

#     return response


# question = "Bệnh gout là gì?"

# answer = get_openai_answer(question)


data_test = pd.read_csv('new/[Test] MedQA.csv', encoding='utf-8')
data_test = data_test['text']
data_test = data_test.tolist()
data_test = data_test[122:]

gpt_answers = open('gpt_answers.jsonl', 'a', encoding='utf-8')

# gpt_turbo_answers = []

for question in tqdm(data_test):
    answer = get_anwser(question)
    # write answer to jsonl file
    gpt_answers.write(json.dumps({'question': question, 'answer': answer}, ensure_ascii=False) + '\n')

    # gpt_turbo_answers.append(answer)
    
    time.sleep(1.5)
    

# gpt_answers.close()

# add the answers to the column "GPT 3.5 turbo" of dataframe
# data_test = pd.read_csv('new/[Test] MedQA.csv', encoding='utf-8')
# data_test['GPT 3.5 turbo'] = gpt_turbo_answers

# data_test.to_csv('new/MedQA_GPT_3.5_turbo.csv', encoding='utf-8', index=False)

