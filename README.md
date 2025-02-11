# badhank discord app
A self-hostable chatbot for Discord that utilizes ollama. He is bad by the way.

## Installation
1. [Install Ollama](https://ollama.com/download/)
2. `pip install discord.py ollama requests`
3. Open `config.toml` and enter your model and bot token
4. Run `run.py`
- Note: if you want the bot to work without it being pinged/mentioned, use runNoMention.py
- Note 2: if you dont want memories and just something simple, use runStable.py
## Usage
To use the bot, ping it via its username (e.g. @bot) or reply to it.

## Support
Any contributions to this would be greatly appreciated. 

## TODO
- Clean code up
- Squash some bugs
- add history "cleaning" (cleans past lines to save on storage, ram, and vram)
