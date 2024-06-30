#!/bin/bash

CUDA_VISIBLE_DEVICES=2 python -m vllm.entrypoints.openai.api_server \
    --gpu-memory-utilization 0.4 \
    --dtype bfloat16 \
    --port 8761 \
    --model LLaMA/models/seallm-7b-v2.5-sft \
    # --enable-lora \
    --api-key token-abc123
