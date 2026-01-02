import customtkinter as ctk
import threading
import q_core  # We import your existing brain!

# --- CONFIGURATION ---
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class QCoreApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. WINDOW SETUP
        self.title("Q-CORE v2.0")
        self.geometry("700x500")

        # 2. GRID LAYOUT (The skeleton)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) # Chat area expands
        self.grid_rowconfigure(1, weight=0) # Input area stays fixed

        # 3. CHAT DISPLAY (Where the bot talks)
        self.chat_display = ctk.CTkTextbox(self, width=600, font=("Roboto", 14))
        self.chat_display.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.chat_display.insert("0.0", "SYSTEM: Q-Core Online. Ready for commands...\n\n")
        self.chat_display.configure(state="disabled") # User can't type here, only read

        # 4. INPUT FIELD (Where you type)
        self.entry = ctk.CTkEntry(self, placeholder_text="Type command here...", width=500, height=40)
        self.entry.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.entry.bind("<Return>", self.send_command) # Press Enter to send

        # 5. BUTTONS
        self.send_button = ctk.CTkButton(self, text="SEND", command=self.send_command, width=100)
        self.send_button.place(relx=0.85, rely=0.92, anchor="center")

        # Voice Button (Future Upgrade)
        self.voice_button = ctk.CTkButton(self, text="🎤", width=40, command=self.activate_voice)
        self.voice_button.place(relx=0.95, rely=0.92, anchor="center")

    def print_to_gui(self, text, sender="BOT"):
        """Helper to write text to the chat window"""
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"\n[{sender}]: {text}\n")
        self.chat_display.see("end") # Auto-scroll to bottom
        self.chat_display.configure(state="disabled")

    def send_command(self, event=None):
        user_input = self.entry.get()
        if not user_input: return
        
        # 1. Show User Input
        self.print_to_gui(user_input, "YOU")
        self.entry.delete(0, "end")

        # 2. Run Processing in a separate thread (so UI doesn't freeze)
        threading.Thread(target=self.process_backend, args=(user_input,)).start()

    def process_backend(self, user_input):
        # A. Check Action (Hands)
        action_result = q_core.perform_action(user_input)
        if action_result:
            self.print_to_gui(action_result, "Q-CORE")
            q_core.speak(action_result)
            return

        # B. Check Quantum Brain (Soul)
        mood = q_core.get_quantum_mood(user_input)
        
        # Construct Prompt
        memories = ", ".join(q_core.CORE_MEMORY.get('notes', []))
        system_prompt = (
            f"You are Q-Core. Act {mood}. "
            f"Memory: {memories}. "
            f"Short answer."
        )
        
        try:
            response = q_core.ollama.chat(model='phi3', messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_input},
            ])
            bot_reply = response['message']['content']
            
            self.print_to_gui(bot_reply, "Q-CORE")
            q_core.speak(bot_reply)
            
        except Exception as e:
            self.print_to_gui(f"Error: {str(e)}", "SYSTEM")

    def activate_voice(self):
        self.print_to_gui("Listening...", "EARS")
        # Run voice in thread
        threading.Thread(target=self.process_voice).start()

    def process_voice(self):
        text = q_core.listen_for_command()
        if text:
            # Send the heard text to the normal processing function
            self.process_backend(text)
        else:
            self.print_to_gui("Did not hear anything.", "EARS")

if __name__ == "__main__":
    app = QCoreApp()
    app.mainloop()

