from transformers import AutoConfig

model_name = "akjindal53244/Llama-3.1-Storm-8B"
config = AutoConfig.from_pretrained(model_name)
print(f"Max Sequence Length: {config.max_position_embeddings}")

