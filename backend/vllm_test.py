import torch
from vllm import LLM, SamplingParams
from transformers import AutoTokenizer

def main():
    model_name = "akjindal53244/Llama-3.1-Storm-8B"

    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    print("Loading model with vLLM...")
    try:
        # Load the model with single GPU settings
        llm = LLM(
            model=model_name,
            max_model_len=4096,          # Adjust as needed for token length
            gpu_memory_utilization=0.8,  # Adjust memory utilization if necessary
            tensor_parallel_size=1,      # Use only one GPU
            dtype=torch.float16,         # Use float16 for better performance
            device="cuda:0",             # Set to use GPU 0
            enforce_eager=True           # Optional: use eager mode for stability
        )
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    prompt = "Once upon a time,"
    print(f"Prompt: {prompt}")

    # Tokenize the prompt
    inputs = tokenizer(prompt, return_tensors="pt")

    # Define sampling parameters for text generation
    sampling_params = SamplingParams(
        temperature=0.7,
        top_p=0.9,
        max_tokens=4000  # Generate up to 1000 tokens in response
    )

    print("Generating text...")
    try:
        # Generate the response
        outputs = llm.generate([prompt], sampling_params)

        # Decode the generated tokens
        generated_text = outputs[0].outputs[0].text.strip()
        print("Generated Text:")
        print(generated_text)

    except Exception as e:
        print(f"Error generating text: {e}")

if __name__ == "__main__":
    main()

