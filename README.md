# HeathcareQA

HealthCareQA - a Vietnamese health Q&A chatbot based on Retrieval-Augmented Generation (RAG) architecture. The chatbot uses the SeaLLM-7B-v2.5 large language model, fine-tuned by LoRA technique, combined with the ColBERTv2 information retrieval model to provide accurate and reliable medical information to users.



### Setup

# 1. Clone repository

git clone [text](https://github.com/xuantruong118/HeathcareQA.git)

# 2. Installation

pip install -r `requirements.txt`

# 3. Download model

Please download the pre-trained SeaLLM-7B-v2.5 model and the ColBERTv2 model from the following link and place them in the `models` folder.

[SeaLLM-7B-v2.5](https://huggingface.co/xuantruong118/SeaLLM-7B-v2.5)

[ColBERTv2](https://huggingface.co/xuantruong118/ColBERTv2)

# 4. Start server Retriever and LLM
Run the following command to start the server:

```
python retriever.py
```
```
python server.py
```

# 5. Start the chatbot

Run the following command to start the chatbot:

```
python chatbot.py
```
After running complete, open your web browser and navigate to `http://localhost:5000` to access the chatbot.



