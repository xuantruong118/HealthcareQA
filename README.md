# HeathcareQA

HealthCareQA - a Vietnamese health Q&A chatbot based on Retrieval-Augmented Generation (RAG) architecture. The chatbot uses the SeaLLM-7B-v2.5 large language model, fine-tuned by LoRA technique, combined with the ColBERTv2 information retrieval model to provide accurate and reliable medical information to users.



# Setup

### 1. Clone repository

git clone https://github.com/xuantruong118/HeathcareQA.git

### 2. Installation

pip install -r `requirements.txt`

### 3. Download model and data
### Training
I use [bkai-foundation-models/vietnamese-bi-encoder](https://huggingface.co/bkai-foundation-models/vietnamese-bi-encoder) as the base model to train ColBERTv2 Retriever.
For the training llm stage, I use [SeaLLMs/SeaLLM-7B-v2.5](https://huggingface.co/SeaLLMs/SeaLLM-7B-v2.5) as base model for continued pretraining. Then use this pretrained model to train supervised finetuning.

Data for fine-tuning SeaLLM-7B-v2.5 and ColBERTv2 can be downloaded from the following link:
[Data](https://drive.google.com/drive/folders/1T5w7L0o5uRJYK8LzH2J5Vz1T9TJ-5j9W?usp=sharing)

After downloading, extract the data and place it in the `data` folder.

### Inference
Please download the supervised-finetuned SeaLLM-7B-v2.5 model and the ColBERTv2 model from the following link and place them in the `models` folder.

| Model | Link |
|:---:|:---:|
| SeaLLM-7B-v2.5 | [https://huggingface.co/xuantruong118/SeaLLM-7B-v2.5](https://huggingface.co/xuantruong118/SeaLLM-7B-v2.5) |
| ColBERTv2 | [https://huggingface.co/xuantruong118/ColBERTv2](https://huggingface.co/xuantruong118/ColBERTv2) |



The data used to Retriever for the chatbot can be downloaded from the following link and placed in the `data` folder.

Data: https://drive.google.com/drive/folders/1sG9w7x3Xs9L7Zzr9Vg0Zq2t5BjzQZVJ-?usp=sharing

### 4. Start server Retriever and LLM
Run the following command to start the server:

#### Retriever server
```
python retriever.py
```
vLLM server
```
python server.py
```

### 5. Start the chatbot

Run the following command to start the chatbot:

```
python chatbot.py
```
After running complete, open your web browser and navigate to `http://localhost:5000` to access the chatbot.


### Contact

If you have any questions or suggestions, please feel free to contact me via email: truongxl.yd1@gmail.com



