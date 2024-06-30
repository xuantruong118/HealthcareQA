import argparse
import requests
import gradio as gr
from openai import OpenAI


from vllm.entrypoints.openai.api_server import app

# Argument parser setup
parser = argparse.ArgumentParser(
    description='Chatbot Interface with Customizable Parameters')
parser.add_argument('--model-url',
                    type=str,
                    default='http://localhost:8761/v1',
                    help='Model URL')
parser.add_argument('-u',
                    '--url-retriever',
                    type=str,
                    default='http://localhost:5678/api/search',
                    help='URL for the retriever server')
parser.add_argument('-m',
                    '--model',
                    type=str,
                    default="LLaMA/models/seallm-7b-v2.5-sft",
                    help='Model name for the chatbot')
parser.add_argument("--host", type=str, default="0.0.0.0")
parser.add_argument("--port", type=int, default=8001)

# Parse the arguments
args = parser.parse_args()

# Set OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "token-abc123"
retriever_api_key = "abcd1234"
openai_api_base = args.model_url

# Create an OpenAI client to interact with the API server
client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

CHAT_EXAMPLES = [
    ["Sốt xuất huyết là gì? Cách phòng tránh bệnh sốt xuất huyết?"],
    ["Cách phòng tránh bệnh tiểu đường hiệu quả?"],
    ["Các biện pháp phòng tránh bệnh suy giảm trí nhớ"],
]

def retriever(query, k):
    contexts = []
    headers = {"Authorization": f"Bearer {retriever_api_key}"}
    # Send a GET request to the retriever server
    response = requests.get(args.url_retriever, params={"query": query, "top_k": k}, headers=headers)
    response = response.json()

    for item in response:
        contexts.append(item["text"]['content'])

    return contexts

def response(message, history, system_message, max_new_tokens, temperature, top_p):
    # get context for the message
    contexts = retriever(message, 5)
    context = "\n".join(f"Context {i+1}: {ctx}" for i, ctx in enumerate(contexts))

    if len(contexts) != 0:
        system_message = f"""You are a helpful assistant. You are given the following contexts to help answer the question.
        CONTEXT: {context}"""
    
    # Convert chat history to OpenAI format
    history_openai_format = [{
        "role": "system",
        # "content": "You are a helpful assistant."
        "content": system_message
    }]
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human})
        history_openai_format.append({
            "role": "assistant",
            "content": assistant
        })
    history_openai_format.append({"role": "user", "content": f"QUESTION: {message}"})
    
    print(f"Max new tokens: {max_new_tokens}")
    
    print(f"Chat history: {history_openai_format}")
    
    print("-------------------------------")

    # Create a chat completion request and send it to the API server
    stream = client.chat.completions.create(
        model=args.model,  # Model name to use
        messages=history_openai_format,  # Chat history
        max_tokens=max_new_tokens,  # Maximum tokens to generate
        stream=True,  # Stream response
        top_p=top_p,  # Top-p value for text generation
        frequency_penalty=0.1,  # Frequency penalty for text generation
        temperature=temperature,  # Temperature for text generation
        extra_body={
            "add_generation_prompt": True
            # "max_new_tokens": max_new_tokens
        })

    # Read and return generated text from response stream
    partial_message = ""
    for chunk in stream:
        partial_message += (chunk.choices[0].delta.content or "")
        yield partial_message

def save_feedback(name, quality_confirm, desired_answer):
    print(f"Name: {name}, Quality: {quality_confirm}, Feedback: {desired_answer}")
    return "Thank you for your feedback! We will use it to improve our service."

demo = gr.ChatInterface(
    response,
    title="Heathcare Assistant",
    description="Ask any question about healthcare and get answers from the AI assistant.",
    chatbot = gr.Chatbot(label="Assistant", show_copy_button=True, likeable=True),
    additional_inputs=[
        gr.Textbox(value="You are a helpful assistant.", label="System Message"),
        gr.Slider(minimum=1, maximum=2048, value=512, step=1, label="Max new tokens"),
        gr.Slider(minimum=0.1, maximum=1.0, value=0.7, step=0.1, label="Temperature"),
        gr.Slider(minimum=0.1, maximum=1.0, value=0.75, step=0.05, label="Top-p"),
    ],
    examples=CHAT_EXAMPLES,
    cache_examples=False
)

with demo:
    with gr.Column(scale=1):
        name = gr.Textbox(placeholder="Nguyen Van A", label="What is your name?")
        quality_confirm = gr.Radio(["CORRECT", "INCORRECT"], label="Rate for the answer")
        desired_answer = gr.Textbox(placeholder="", lines=4, label="Feedback")
        btn_save = gr.Button("Save")
        save_status = gr.Label(label="", min_width=80)  # Add this line
        
    btn_save.click(fn=save_feedback, inputs=[name, quality_confirm, desired_answer], outputs=[save_status])  # Modify this line

print("-------------------------------")
# Create and launch a chat interface with Gradio
demo.queue().launch(server_name=args.host,
                    server_port=args.port,
                    share=True)
