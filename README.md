Basic AI Agent that runs using a local Ollama LLM instance (or uncomment the hf inference api if you have credit limits). Developed as part of the Huggingface AI Agents course.

## Model
This agent is configured to use the llama 3.2B model, run locally via Ollama, and accessed with the LiteLLMModel.

## Tools
The agent is facilitated with the following tools:

1. Fetch current time of a timezone
2. Fetch current weather of a city using OpenWeather APIs

## Access Needed to Run
To allow this agent to work with all its tools, the following keys have to be provided in a secret.config file. Populate this file as <KEY_NAME>=<API_KEY> before running locally.

1. OPENWEATHER_API_KEY:
   Generate API_KEY from https://openweathermap.org/api and provide to the agent to be able to fetch real-time weather data.

## Run Agent
The agent is run locally by executing the app.py script and can be interacted with via the gradio UI hosted on localhost.
