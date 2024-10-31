from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from vllm import LLM, SamplingParams
from transformers import AutoTokenizer
import torch
import os

app = FastAPI()

# Model and tokenizer setup
model_name = "akjindal53244/Llama-3.1-Storm-8B"

# Configure to use two GPUs
llm = None
tokenizer = None

class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = 100  # Max number of tokens to generate

@app.on_event("startup")
def load_model():
    global llm, tokenizer
    print("Loading model and tokenizer on 2 GPUs...")

    # Set environment variable to specify which GPUs to use
    os.environ["CUDA_VISIBLE_DEVICES"] = "0,1"  # Ensures both GPUs 0 and 1 are visible

    # Load the tokenizer from Hugging Face
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    try:
        # Initialize vLLM with tensor parallelism across 2 GPUs and limited swap space
        llm = LLM(
            model=model_name,
            max_model_len=4096,           # Set based on model capacity
            gpu_memory_utilization=0.9,   # Adjust memory utilization
            tensor_parallel_size=2,       # Use 2 GPUs for parallelism
            dtype=torch.float16,          # Use float16 for better performance
            device="cuda",                # Use CUDA for GPU acceleration
            swap_space=222222222222222222222Limit swap space to 4 GB
            enforce_eager=True            # Optional: Enforce eager execution for stability
        )
        print("Model loaded successfully on 2 GPUs.")
    except Exception as e:
        print(f"Failed to load the model: {e}")

@app.post("/generate")
async def generate_text(request: GenerateRequest):
    global llm, tokenizer

    if not llm or not tokenizer:
        raise HTTPException(status_code=500, detail="Model is not loaded.")

    try:
        # Prepare the input and sampling parameters
        sampling_params = SamplingParams(
            max_tokens=request.max_tokens,
            temperature=0.7,
            top_p=0.9
        )

        # Generate the response
        outputs = llm.generate([request.prompt], sampling_params)
        generated_text = outputs[0].outputs[0].text.strip()

        return {"generated_text": generated_text}
    except Exception as e:
        print(f"Error during generation: {e}")
        raise HTTPException(status_code=500, detail="Error during text generation.")

@app.get("/")
async def root():
    return {"message": "Welcome to the multi-GPU vLLM server for Hugging Face model!"}

