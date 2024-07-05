from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
#from flask import Flask, request, jsonify

# Check for GPU availability
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load the model and tokenizer
model = AutoModelForCausalLM.from_pretrained(
    "universitytehran/PersianMind-v1.0",
    torch_dtype=torch.bfloat16,
    low_cpu_mem_usage=True,
    device_map={"": device},
)
tokenizer = AutoTokenizer.from_pretrained(
    "universitytehran/PersianMind-v1.0",
)

# Function to generate ad suggestions
def generate_ad_suggestions(prompt):
    TEMPLATE = "{context}\nYou: {prompt}\nPersianMind: "
    CONTEXT = ("This is a conversation with PersianMind, an AI assistant designed to help users create effective ad titles and descriptions for selling their belongings on an online marketplace. "
               "You can describe the item you want to sell, and it will suggest an appropriate title and description for your ad. "
               "Please provide as much detail as possible about the item you are selling.")
    
    # Format the input prompt
    model_input = TEMPLATE.format(context=CONTEXT, prompt=prompt)
    input_tokens = tokenizer(model_input, return_tensors="pt")
    input_tokens = input_tokens.to(device)
    
    # Generate suggestions
    generate_ids = model.generate(**input_tokens, max_new_tokens=512, do_sample=False, repetition_penalty=1.1)
    model_output = tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
    
    # Extract the model's response
    response = model_output[len(model_input):].strip()
    return response

# Flask app setup
#app = Flask(__name__)

#@app.route('/generate-ad', methods=['POST'])
#def generate_ad():
    #data = request.get_json()
    #prompt = data['prompt']
    #suggestions = generate_ad_suggestions(prompt)
    #return jsonify({'suggestions': suggestions})

if __name__ == '__main__':
    app.run(debug=True)

user_prompt = "من یک تلفن همراه سامسونگ گلکسی S21 برای فروش دارم. عنوان و توضیحات مناسب برای آگهی را پیشنهاد دهید."
suggestions = generate_ad_suggestions(user_prompt)
print(suggestions)
