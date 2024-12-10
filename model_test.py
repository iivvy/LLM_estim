from mlx_lm import load
from mlx_lm import generate


model_name = "mlx-community/Meta-Llama-3-8B-Instruct-4bit"
model, tokenizer = load(model_name)
chatbot_role = "You estimates cost and a duration of a project based on its descriptions and user stories."
question = "Please estimate the duration and cost  of developing a platform like spotify, dont provide details just the cost in dollars and duration in years"

messages = [
    {"role": "system", "content": chatbot_role},
    {"role": "user", "content": question}
]

# Apply the chat template to format the input for the model
input_ids = tokenizer.apply_chat_template(messages, add_generation_prompt=True)

# Decode the tokenized input back to text format to be used as a prompt for the model
prompt = tokenizer.decode(input_ids)

# Generate a response using the model
response = generate(model, tokenizer, max_tokens=512, prompt=prompt)
print('response:------------------', response)


