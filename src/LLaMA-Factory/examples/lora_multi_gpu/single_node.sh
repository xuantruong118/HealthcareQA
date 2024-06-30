#!/bin/bash

CUDA_VISIBLE_DEVICES=1,2 accelerate launch \
    --config_file examples/accelerate/single_config.yaml \
    src/train_bash.py \
    --stage pt \
    --do_train \
    --dataset_dir data \
    --flash_attn True \
    --finetuning_type lora \
    --lora_dropout 0.05 \
    --lora_alpha 32\
    --use_unsloth True \
    --model_name_or_path Qwen/Qwen1.5-4B \
    --dataset medical_mc4 \
    --lora_target q_proj,v_proj \
    --output_dir saves/Qwen1.5-4B/lora/pretrain \
    --overwrite_cache \
    --overwrite_output_dir \
    --cutoff_len 1024 \
    --preprocessing_num_workers 16 \
    --per_device_train_batch_size 16 \
    --per_device_eval_batch_size 8 \
    --gradient_accumulation_steps 4 \
    --weight_decay 0.1 \
    --lr_scheduler_type cosine \
    --logging_steps 10 \
    --warmup_steps 200 \
    --save_steps 3000 \
    --eval_steps 3000 \
    --evaluation_strategy steps \
    --load_best_model_at_end \
    --learning_rate 1e-5 \
    --num_train_epochs 1.0 \
    --val_size 0.0001 \
    --plot_loss \
    --bf16