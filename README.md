# Project Estimator API

This project provides a REST API to estimate the cost and duration of software projects based on a project description and a set of user stories. The backend is implemented using FastAPI and leverages the Llama 3 model (via the MLX library) to generate AI-powered estimates.

## Features

- Accepts a project description and user stories as input.
- Uses the Llama 3 language model to generate project cost and duration estimates.
- Returns structured JSON responses.
- Simple and efficient architecture for easy integration with frontends.

## Requirements

- Python 3.8+
- macOS with Apple Silicon (for running the MLX library on an M1/M2 chip)



## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/project-estimator.git
   cd project-estimator
   ```

2. Set up your Python environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install fastapi uvicorn pydantic requests mlx

   ```

3. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

4. Access the API documentation:
   Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the interactive Swagger UI.

## API Usage

### Endpoint

**POST** `/estimate/`

#### Request Body

```json
{
  "project_description": "Develop a Spotify-like platform",
  "user_stories": [
    "Stream music",
    "Create playlists",
    "Follow artists"
  ]
}
```

#### Response Example

```json
{
  "duration": 2,
  "cost": 15000000
}
```

### Error Handling

If the AI model fails to generate a valid response, the API will return:

```json
{
  "error": "Unable to parse the response. Ensure the model returns valid JSON. Raw response: ..."
}
```

## Architecture

The API consists of the following components:

- **FastAPI Framework:** To handle HTTP requests and responses.
- **MLX Library:** For loading and interacting with the Llama 3 model.
- **Custom Model Input:** A `ProjectInput` Pydantic model to validate input data.

## File Structure

```
project-estimator/
├── main.py           # Entry point for the FastAPI app
├── model.py          # Pydantic models for API input
├── requirements.txt  # Dependencies
└── README.md         # Project documentation
```

## Testing

You can test the API using tools like `curl`, Postman, or an HTTP client library.

### Example with `curl`

```bash
curl -X POST "http://127.0.0.1:8000/estimate/" \
-H "Content-Type: application/json" \
-d '{"project_description": "Develop a Spotify-like platform", "user_stories": ["Stream music", "Create playlists", "Follow artists"]}'
```

<!-- ## Limitations

- The cost and duration estimates are approximate and based on predefined assumptions by the AI model.
- Requires macOS with Apple Silicon to leverage the MLX library effectively.

## Future Enhancements

- Add authentication to secure the API.
- Improve model prompt engineering for more accurate results.
- Add support for multiple LLMs and configurable backends.
- Implement frontend integration and deployment.
 -->
