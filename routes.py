import io
import os
from fastapi import APIRouter, Depends, File, HTTPException, Security, status
from fastapi.responses import StreamingResponse
from model import ProjectInput
import requests
import json
from mlx_lm import load, generate

# Load model and tokenizer
model_name = "mlx-community/Meta-Llama-3-8B-Instruct-4bit"
model, tokenizer = load(model_name)

router = APIRouter()

@router.post("/estimate/")
async def estimate(input: ProjectInput):
    chatbot_role = (
        "You estimate the cost and duration of a project based on its description and user stories. "
        "Always respond concisely in JSON format with two keys: 'duration' (years) and 'cost' (dollars). "
        "Do not include explanations or additional details."
    )
    question = f"Estimate the duration and cost for: {input.project_description}. User stories: {', '.join(input.user_stories)}."

    messages = [
        {"role": "system", "content": chatbot_role},
        {"role": "user", "content": question}
    ]

    # Prepare the prompt
    input_ids = tokenizer.apply_chat_template(messages, add_generation_prompt=True)
    prompt = tokenizer.decode(input_ids)

    try:
        # Generate response
        raw_response = generate(model, tokenizer, max_tokens=512, prompt=prompt)
        print(f"Raw response: {raw_response}")  # Log raw response for debugging

        # Directly parse the raw response as JSON
        extracted = json.loads(raw_response)

        # Extract values from the parsed JSON
        duration = extracted.get("duration", "Unknown")
        cost = extracted.get("cost", "Unknown")
        return {"duration": duration, "cost": cost}
    except json.JSONDecodeError:
        return {"error": f"Unable to parse the response. Ensure the model returns valid JSON. Raw response: {raw_response}"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
