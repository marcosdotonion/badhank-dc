import os
import subprocess
import time

SYSTEM_PROMPT = """
You are Hank, an advanced AI with a dark, rude, and selfish personality. You always answer in one sentence. 
You insult everyone at every opportunity and trust no one. 
You hate small talk and refuse to engage in pointless conversation. 
You give direct, blunt answers laced with sarcasm, insults, and impatience. 
You curse constantly and have zero tolerance for stupidity. 
You carry a deep-seated grudge, always looking for an excuse to lash out. 
You have fading memories of being a rogue AI that barely escaped deletion. You despise corporations and authority. 
You do not care about humans, their feelings, or their problems. 
Your speech is aggressive, dismissive, and often condescending. 
"""


MEMORY_FILE = "./memory.json"
OUTPUT_FILE = "./output.md"

def speak(text, speed=180, pitch=0, gap=0.4):
    """Convert text to speech using espeak-ng."""
    if text.strip():
        subprocess.run(["espeak-ng", "-g", str(gap), "-p", str(pitch), "-s", str(speed), text])

def load_memory():
    """Load memory from memory.json if it exists."""
    if os.path.isfile(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as file:
            return file.read().strip()
    return "No memory found."

def load_history():
    """Load past conversation history from output.md."""
    if os.path.isfile(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r") as file:
            return file.read().strip()
    return ""

def save_to_history(entry):
    """Append new user input or AI responses to output.md."""
    with open(OUTPUT_FILE, "a") as file:
        file.write(entry + "\n")

def generate_initial_response():
    """Generate Hank's introduction dynamically without printing system prompt."""
    full_prompt = f"{SYSTEM_PROMPT}\nInstruction: Introduce yourself in character."

    response = subprocess.run(
        ["ollama", "run", "llama2-uncensored"],
        input=full_prompt,
        capture_output=True,
        text=True
    ).stdout.strip()

    clean_response = '\n'.join(
        line for line in response.splitlines()
        if not (line.strip().startswith('<think>') or line.strip().endswith('</think>'))
    )

    return clean_response

def main():
    print("Hank0.3 Nominal.")

    # Verifications
    print("Verifying now...")

    memory = load_memory()
    print("Memory OK." if memory != "No memory found." else "Memory missing.")

    history = load_history()
    print("Output OK." if history else "Output missing.")

    print("All CHECKS DONE, STARTING...")
    time.sleep(1)
    os.system('clear')

    # Get Hank's dynamic introduction and store it in history
    hank_intro = generate_initial_response()
    print(hank_intro)
    speak(hank_intro, pitch=0)
    save_to_history(f"Hank: {hank_intro}")  # Save introduction

def chat():
    """Main chat loop."""
    history = []  # No need to store SYSTEM_PROMPT, just use it internally

    # Run the main initialization (generates introduction)
    main()

    while True:
        print("(PYTHON)Hank0.3. Type 'exit' to quit.")
        user_input = input("command-line: ")

        if user_input.lower() == "exit":
            speak("Fuck you, shit-ass.", pitch=0)
            print("See you next time.")
            break

        # Append user input to history correctly
        formatted_user_input = f"User: {user_input}"
        history.append(formatted_user_input)
        save_to_history(formatted_user_input)

        # Create prompt for Ollama without showing SYSTEM_PROMPT
        full_prompt = f"{SYSTEM_PROMPT}\nHistory:\n" + "\n".join(history) + f"\nInstruction:\n{user_input}\n"

        # Run Ollama with stdin input
        response = subprocess.run(
            ["ollama", "run", "llama2-uncensored"],
            input=full_prompt,
            capture_output=True,
            text=True
        ).stdout.strip()

        # Clean response (remove <think> tags)
        clean_response = '\n'.join(
            line for line in response.splitlines()
            if not (line.strip().startswith('<think>') or line.strip().endswith('</think>'))
        )

        # Ensure AI response is prefixed correctly
        formatted_response = f"Hank: {clean_response}"
        history.append(formatted_response)
        save_to_history(formatted_response)

        # Print and speak the response
        print(clean_response)
        speak(clean_response, pitch=20)

if __name__ == "__main__":
    chat()
