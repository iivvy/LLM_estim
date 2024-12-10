import io
import os
from fastapi import APIRouter, Depends, File, HTTPException, Security, status
from fastapi.responses import StreamingResponse
from model import ProjectInput
import requests
from mlx_lm import load, generate

# Load model and tokenizer
model_name = "mlx-community/Meta-Llama-3-8B-Instruct-4bit"
model, tokenizer = load(model_name)

router = APIRouter()

@router.post("/estimate/")
async def estimate(input: ProjectInput):
    chatbot_role = "You estimate cost and duration of a project based on its descriptions and user stories."
    question = f"Estimate the duration and cost for: {input.project_description}. User stories: {', '.join(input.user_stories)}. Provide only cost in dollars and duration in years."

    messages = [
        {"role": "system", "content": chatbot_role},
        {"role": "user", "content": question}
    ]

    # Prepare the prompt
    input_ids = tokenizer.apply_chat_template(messages, add_generation_prompt=True)
    prompt = tokenizer.decode(input_ids)

    # Generate response
    response = generate(model, tokenizer, max_tokens=512, prompt=prompt)
    return {"estimate": response}