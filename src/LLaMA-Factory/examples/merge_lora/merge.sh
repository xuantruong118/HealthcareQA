#!/bin/bash
# DO NOT use quantized model or quantization_bit when merging lora weights

CUDA_VISIBLE_DEVICES=1 python src/export_model.py \
    --model_name_or_path SeaLLMs/SeaLLM-7B-v2.5 \
    --adapter_name_or_path saves/seallm-7b-v2.5/lora/sft \
    --template default \
    --finetuning_type lora \
    --export_dir models/seallm-7b-v2.5 \
    --export_size 4 \
    --export_legacy_format False
