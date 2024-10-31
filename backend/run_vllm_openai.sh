#!/bin/bash

# Define the path to the log file
LOG_FILE="vllm_openai_logs.log"

# Redirect all output and errors to the log file
exec > >(tee -a $LOG_FILE) 2>&1

# Run vllm server
vllm serve neuralmagic/Meta-Llama-3-8B-Instruct-FP8 --dtype auto --api-key token-what-a-day --gpu-memory-utilization 0.7 --enable-prefix-caching

