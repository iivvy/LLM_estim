import os
import requests
from fastapi import APIRouter, HTTPException
from model import ProjectInput, LLMResponse
import json

# Load model API URL and token from environment variables
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
# Set environment variable for the token
router = APIRouter()
def load_huggingface_token():
    try:
        with open('config.json', "r") as config_file:
            config = json.load(config_file)
            return config.get("huggingface_token")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise HTTPException(status_code=500, detail=f"Error loading config file: {e}")

@router.post("/estimate/")
async def estimate(input: ProjectInput):
    HUGGINGFACE_TOKEN = load_huggingface_token()
        

    def llm(project_description, user_stories):
        parameters = {
            "max_new_tokens": 5000,
            "temperature": 0.01,
            "top_k": 50,
            "top_p": 0.95,
            "return_full_text": False
        }
        
        prompt = f"""
<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are a helpful and smart assistant. You estimate the cost and duration of a project based on its description and user stories and you provide at the end a simple explanation for the estimate.
Always respond only with a JSON object containing three keys: "duration" (in years) and "cost" (in dollars) and "explanation". 
<|eot_id|><|start_header_id|>user<|end_header_id|>
Estimate the duration and cost for: ```{project_description}```. 
User stories: ```{', '.join(user_stories)}```.
<|eot_id|><|end_header_id|>
"""
        
        headers = {
            'Authorization': f'Bearer {HUGGINGFACE_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "inputs": prompt.strip(),
            "parameters": parameters
        }
        
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
        
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error from Hugging Face API: {e}")
        try:
            response_json = response.json()  # This will raise an error if the response is not valid JSON
        except ValueError as e:
            raise HTTPException(status_code=422, detail=f"Error decoding JSON from Hugging Face API: {str(e)}")

        
        try:
            response_text = response.json()[0]['generated_text'].strip()
          

        except (KeyError, IndexError, ValueError) as e:
            raise HTTPException(status_code=500, detail=f"Invalid response structure: {str(e)}")
        
        return response_text

    # Call the LLM function
    raw_response = llm(input.project_description, input.user_stories)
    cleaned_response = raw_response.split('\n', 1)[-1]
    # raw_response = llm(input.project_description, input.user_stories)
    print("Raw Response:", cleaned_response)  # Log the raw response

    # Check if response is empty
    if not cleaned_response.strip():  # If it's empty or just whitespace
        raise HTTPException(status_code=422, detail="Received empty response from the API")
    print("---------------------------------------------------")
  
   

    #  parse into Pydantic model
    try:
        llm_response = LLMResponse.parse_raw(cleaned_response)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Error parsing LLM response: {str(e)}")
    print("---------------------------------------------------")
    # Return the structured response
    return  {
        "estimate": {
            "duration": llm_response.duration,
            "cost": llm_response.cost,
            "explanation":llm_response.explanation
        }
    }
