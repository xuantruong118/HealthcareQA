import requests
import json
import pandas as pd
import tqdm
from tqdm import tqdm
import time
import openai
from openai import OpenAI


def get_anwser(question):
    url = "https://litellm.dev.ftech.ai/v1/chat/completions" # or "https://api.openai.com/v1/engines/davinci/completions" for GPT-3.5

    headers = {
        "Content-Type": "application/json",
        'Authorization': 'insert your API key here'
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

    response = response['choices'][0]['message']['content']

    return response



data_test = pd.read_csv('[Test]MedQA_final.csv', encoding='utf-8')
data_test = data_test['text']
data_test = data_test.tolist()

gpt_answers = open('gpt_answers.jsonl', 'a', encoding='utf-8')

gpt_turbo_answers = []

for question in tqdm(data_test):
    answer = get_anwser(question)
    # write answer to jsonl file
    gpt_answers.write(json.dumps({'question': question, 'answer': answer}, ensure_ascii=False) + '\n')

    gpt_turbo_answers.append(answer)
    
    time.sleep(1.5)
    

gpt_answers.close()

# add the answers to the column "GPT 3.5 turbo" of dataframe
data_test = pd.read_csv('new/[Test] MedQA.csv', encoding='utf-8')
data_test['GPT 3.5 turbo'] = gpt_turbo_answers

data_test.to_csv('new/MedQA_GPT_3.5_turbo.csv', encoding='utf-8', index=False)
