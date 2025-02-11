import requests
import json
import discord
import tomllib
import ollama
import os  # Used to save the history file to the computer
import re  # For removing <think></think> tags

# LOAD VARIABLES FROM config.toml
with open("config.toml", 'rb') as f:  # Load config
    config_data = tomllib.load(f)

# API info for Ollama
TOKEN = config_data['discord']['token']  # Load token from config file
API_URL = 'http://localhost:11434/api/chat'

# Get the system prompt from config.toml
SYSTEM_PROMPT = config_data['ollama']['system_prompt']

# Define the path for the conversation history file
HISTORY_FILE_PATH = "history.json"

# Load conversation history from a file if it exists
def load_conversation_history():
    if os.path.exists(HISTORY_FILE_PATH):
        if os.path.getsize(HISTORY_FILE_PATH) == 0:
            return []  # Return empty list if file is empty
        
        with open(HISTORY_FILE_PATH, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []  # Return empty list if file is corrupted
    return []

# Save conversation history to a file
def save_conversation_history():
    with open(HISTORY_FILE_PATH, 'w') as file:
        json.dump(conversation_history, file)

# Store conversation history in a list
conversation_history = load_conversation_history()

# Set what the bot is allowed to listen to
intents = discord.Intents.default()
intents.message_content = True  # Allow reading message content
client = discord.Client(intents=intents)

# Function to remove <think></think> tags from a string
def remove_think_tags(text):
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)

# Function to remove unwanted phrases like "Hank 0.3 says"
def clean_prompt(prompt):
    return re.sub(r'(Hank 0\.3 says:?)', '', prompt, flags=re.IGNORECASE).strip()

# Function to send a request to the Ollama API and get a response
def generate_response(prompt):
    # Initialize the conversation history with an empty list to ensure the system prompt is always included
    conversation_history = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    
    # Add the user's prompt to the conversation history
    conversation_history.append({
        "role": "user",
        "content": prompt
    })
    
    save_conversation_history()

    data = {
        "model": config_data['ollama']['model'],
        "messages": conversation_history,
        "stream": False
    }

    response = requests.post(API_URL, json=data)
    print("Raw Response Content:", response.text)

    try:
        response_data = response.json()
        assistant_message = response_data['message']['content']
        assistant_message = remove_think_tags(assistant_message)
        conversation_history.append({"role": "assistant", "content": assistant_message})
        return assistant_message
    except requests.exceptions.JSONDecodeError:
        return "Error: Invalid API response"

# When the bot is ready
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

# When the bot detects a new message
@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return

    prompt = clean_prompt(message.content)
    try:
        async with message.channel.typing():
            if prompt:
                response = generate_response(prompt)
                await message.channel.send(response)
    except discord.errors.Forbidden:
        print(f"Error: Bot does not have permission to type in {message.channel.name}")

# Run the bot
client.run(TOKEN)
