from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from accelerate import Accelerator
import time  # Importing time module for performance tracking

# Initialize the accelerator
accelerator = Accelerator()

# Model name
model_name = "akjindal53244/Llama-3.1-Storm-8B"

# Load tokenizer
print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Load the model with multi-GPU support
print("Loading model...")
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",  # Distributes across available GPUs
    torch_dtype=torch.float16,  # Use half precision to save memory
    low_cpu_mem_usage=True
)

# Prepare the model with the accelerator
model = accelerator.prepare(model)
print("Model loaded successfully!")

# Define a prompt for testing
prompt = "Can you explain to me how to build a 3D gas reservoir simulator? In Julia?"

# Tokenize the input prompt
print("Tokenizing input...")
inputs = tokenizer(prompt, return_tensors="pt").to(accelerator.device)

# Measure the start time
print("Generating text...")
start_time = time.time()

# Generate text using the model with performance tracking
with torch.no_grad():
    output = model.generate(
        inputs["input_ids"],
        max_new_tokens=500,  # Adjust for longer output if needed
        do_sample=True,
        temperature=0.7,
        pad_token_id=tokenizer.eos_token_id  # Avoid padding-related warnings
    )

# Measure the end time
end_time = time.time()

# Calculate tokens per second
generated_tokens = output.shape[1]  # Number of tokens generated
time_taken = end_time - start_time  # Total time in seconds
tokens_per_second = generated_tokens / time_taken

# Decode and print the generated text
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
print("Generated text:", generated_text)

# Print performance metrics
print(f"Tokens generated: {generated_tokens}")
print(f"Time taken: {time_taken:.2f} seconds")
print(f"Tokens per second: {tokens_per_second:.2f}")

