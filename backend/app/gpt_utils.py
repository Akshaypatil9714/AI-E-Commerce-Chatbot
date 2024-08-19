from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login
import torch
import time

# Replace 'your-access-token' with your actual token
login('your-access-token')

# Load LLama model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3.1-8B")
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Meta-Llama-3.1-8B",
    device_map="auto",
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True,
    offload_folder="offload"
)

def generate_response(context, query, max_time=30):
    try:
        prompt = f"Context: {context[:500]}\n\nQuestion: {query}\n\nAnswer:"
        inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True).to(model.device)
        
        start_time = time.time()
        with torch.no_grad():  # Disable gradient calculation
            outputs = model.generate(
                **inputs, 
                max_new_tokens=100,  # Limit the number of new tokens
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                top_k=50,
                top_p=0.95,
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        if time.time() - start_time > max_time:
            return "I'm sorry, but the response is taking too long to generate. Please try again with a simpler query."
        
        return response.split("Answer:")[-1].strip()  # Return only the generated answer
    except Exception as e:
        print(f"Error generating response: {e}")
        return "I'm sorry, I couldn't generate a response due to an error."