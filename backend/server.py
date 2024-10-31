from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from vllm import LLM, SamplingParams
from transformers import AutoTokenizer
import torch
import os

app = FastAPI()

# Model and tokenizer setup
model_name = "akjindal53244/Llama-3.1-Storm-8B"

# Configure to use only one GPU
llm = None
tokenizer = None

class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = 2000  # Max number of tokens to generate

@app.on_event("startup")
def load_model():
    global llm, tokenizer
    print("Loading model and tokenizer...")

    # Set the environment variable to specify GPU
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"  # Use GPU 0

    # Load the tokenizer from Hugging Face
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    try:
        # Initialize vLLM with single GPU
        llm = LLM(
            model=model_name,
            max_model_len=2000,            # Adjust based on your requirements
            gpu_memory_utilization=0.9,    # Memory usage setting
            tensor_parallel_size=1,        # Single GPU
            dtype=torch.float16,           # Use float16 for better performance
            device="cuda",                 # Use CUDA for GPU acceleration
            enforce_eager=True             # Optional: Enforce eager execution for stability
        )
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Failed to load the model: {e}")

@app.post("/generate")
async def generate_text(request: GenerateRequest):
    global llm, tokenizer

    if not llm or not tokenizer:
        raise HTTPException(status_code=500, detail="Model is not loaded.")

    try:
        # Prepare the sampling parameters
        sampling_params = SamplingParams(
            max_tokens=request.max_tokens,
            temperature=0.7,
            top_p=0.9
        )

        # Generate the response
        outputs = llm.generate([request.prompt], sampling_params)

        # Extract the generated text
        generated_text = outputs[0].outputs[0].text.strip()

        return {"generated_text": generated_text}
    except Exception as e:
        print(f"Error during generation: {e}")
        raise HTTPException(status_code=500, detail="Error during text generation.")

@app.get("/")
async def root():
    return {"message": "Welcome to the vLLM server for Hugging Face model!"}

