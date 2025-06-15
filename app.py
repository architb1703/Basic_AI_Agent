from smolagents import CodeAgent,DuckDuckGoSearchTool, HfApiModel,load_tool,tool, LiteLLMModel
import datetime
import requests
import pytz
import yaml
import os
from tools.final_answer import FinalAnswerTool

from Gradio_UI import GradioUI

# Read API key from secret.config
def load_api_key():
    try:
        with open("secret.config", "r") as f:
            for line in f:
                if line.startswith("OPENWEATHER_API_KEY="):
                    return line.strip().split("=")[1]
    except FileNotFoundError:
        print("Warning: secret.config file not found. Please create it with your OpenWeather API key.")
        return None

@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        # Create timezone object
        tz = pytz.timezone(timezone)
        # Get current time in that timezone
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"

@tool
def get_current_weather(city: str) -> str:
    """A tool that fetches the current weather in a specified city.
    Args:
        city: A string representing a valid city name (e.g., 'New York').
    """
    API_KEY = load_api_key()
    if not API_KEY:
        return "Error: OpenWeather API key not found. Please check your secret.config file."
    
    try:
        geo_loc = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={API_KEY}").json()
        [lat, lon] = geo_loc[0]["lat"], geo_loc[0]["lon"]

        weather = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=imperial").json()

        description = weather["weather"][0]["description"]
        temp = weather["main"]["temp"]
        humid = weather["main"]["humidity"]

        response = f"The weather in {city} is {description}. The temperature is {temp} fahrenheit with {humid}% humidity."
        return response
    except Exception as e:
        return f"Error fetching weather for city '{city}': {str(e)}"

final_answer = FinalAnswerTool()

# If the agent does not answer, the model is overloaded, please use another model or the following Hugging Face Endpoint that also contains qwen2.5 coder:
# model_id='https://pflgm2locj2t89co.us-east-1.aws.endpoints.huggingface.cloud' 

# model = HfApiModel(
# max_tokens=2096,
# temperature=0.5,
# model_id='Qwen/Qwen2.5-Coder-1.5B-Instruct',# it is possible that this model may be overloaded
# custom_role_conversions=None,
# )

model = LiteLLMModel(
    model_id = "ollama/llama3.2:latest",
    api_base="http://127.0.0.1:11434",
    num_ctx=8192,
)

# Import tool from Hub
image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)

with open("prompts.yaml", 'r') as stream:
    prompt_templates = yaml.safe_load(stream)
    
agent = CodeAgent(
    model=model,
    tools=[final_answer, get_current_time_in_timezone, get_current_weather], ## add your tools here (don't remove final answer)
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name=None,
    description=None,
    prompt_templates=prompt_templates
)


GradioUI(agent).launch()