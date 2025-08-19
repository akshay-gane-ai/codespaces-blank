from euriai.langchain import create_chat_model
import os
import json
from dotenv import load_dotenv
load_dotenv()
EURI_API_KEY = os.getenv("EURI_API_KEY")

def get_chat_model():
    """
    Create a chat model using the Euri AI API with specified parameters.
    """
    with open("med_rag_bot/config.json", "r") as config_file:
        config = json.load(config_file)
    return create_chat_model(
    api_key=EURI_API_KEY,
    model=config["MODEL"],
    temperature=config["TEMPERATURE"]
    )

def ask_chat_model(chat_model, prompt: str):
    response = chat_model.invoke(prompt)
    return response.content

