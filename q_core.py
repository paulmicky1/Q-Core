import pennylane as qml
from pennylane import numpy as np
import ollama
import sys
import os
import webbrowser
import subprocess
import speech_recognition as sr
import json
import pyttsx3
import threading

# --- 0. CONFIGURATION ---
MEMORY_FILE = "q_memory.json"

# Initialize Voice Engine (The Mouth)
engine = pyttsx3.init()
engine.setProperty('rate', 160) # Speed of speech
engine.setProperty('volume', 1.0)

def speak(text):
    """Makes the bot talk. We run it in a loop to prevent freezing."""
    print(f"   [AUDIO OUTPUT]: {text}")
    engine.say(text)
    engine.runAndWait()

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_memory(memory_dict):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory_dict, f, indent=4)

CORE_MEMORY = load_memory()

# --- 1. THE QUANTUM LAYER (The Soul) ---
dev = qml.device("default.qubit", wires=1)

@qml.qnode(dev)
def quantum_intuition(input_sentiment):
    qml.RX(input_sentiment, wires=0)
    return qml.probs(wires=0)

def get_quantum_mood(user_text):
    if not user_text: return "Neutral"
    val = sum([ord(c) for c in user_text]) / 100.0
    probs = quantum_intuition(val)
    return "Logical" if probs[0] > 0.5 else "Creative"

# --- 2. THE ACTION LAYER (Hands + Memory) ---
def perform_action(command):
    command = command.lower().strip()
    
    # A. MEMORY COMMANDS
    if "remember that" in command:
        fact = command.split("remember that")[1].strip()
        if 'notes' not in CORE_MEMORY: CORE_MEMORY['notes'] = []
        CORE_MEMORY['notes'].append(fact)
        save_memory(CORE_MEMORY)
        return f"I have saved this memory: {fact}"

    if "what do you remember" in command:
        if 'notes' in CORE_MEMORY:
            return f"I remember that: {', '.join(CORE_MEMORY['notes'])}"
        else:
            return "My memory is currently empty."

    # B. BROWSER / SYSTEM COMMANDS
    if "youtube" in command:
        if len(command) > 10:
            term = command.replace("youtube", "").replace("search", "").replace("play", "").strip()
            webbrowser.open(f"https://www.youtube.com/results?search_query={term}")
            return f"Searching YouTube for {term}"
        else:
            webbrowser.open("https://www.youtube.com")
            return "Opening YouTube."

    elif "google" in command:
        term = command.replace("google", "").replace("search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={term}")
        return f"Googling {term}"
        
    elif "open terminal" in command:
        subprocess.Popen(["gnome-terminal"]) 
        return "Terminal launched."

    return None

# --- 3. VOICE INPUT (The Ears) ---
def listen_for_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n   [EARS: Listening...]")
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5)
            print("   [EARS: Processing...]")
            command = r.recognize_google(audio)
            print(f"   [YOU SAID]: {command}")
            return command
        except:
            return ""

# --- 4. MAIN LOOP ---
def chat_with_qcore():
    os.system('clear') 
    print("\n=============================================")
    print("      Q-CORE: QUANTUM INTELLIGENCE SYSTEM")
    print("=============================================")
    
    # Startup Sound
    speak("Q Core systems online. Waiting for command.")

    mode = input("\nSelect Mode -> (1) Keyboard  (2) Voice: ")
    
    while True:
        try:
            user_input = ""
            if mode == "2":
                input("\nPress ENTER to speak...")
                user_input = listen_for_command()
                if not user_input: continue
            else:
                user_input = input("\nYOU: ")

            if user_input.lower() in ["exit", "quit"]: 
                speak("Shutting down.")
                break

            # 1. Action Check
            action_result = perform_action(user_input)
            if action_result:
                speak(action_result) # Bot speaks the action confirmation
                continue 

            # 2. Quantum Context & Response
            mood = get_quantum_mood(user_input)
            print(f"   [Quantum State: {mood}]")

            memories = ", ".join(CORE_MEMORY.get('notes', []))
            system_prompt = (
                f"You are Q-Core. Act {mood}. "
                f"Your memory contains: {memories}. "
                f"Keep your answer under 2 sentences. Speak naturally."
            )
            
            response = ollama.chat(model='phi3', messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_input},
            ])

            bot_reply = response['message']['content']
            
            # 3. Speak and Print
            print(f"Q-CORE: {bot_reply}")
            speak(bot_reply)
            
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    chat_with_qcore()
