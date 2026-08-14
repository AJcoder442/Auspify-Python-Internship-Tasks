import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
import json
import os
import threading
import difflib
import re
import time

# Color Palette for a premium chat interface (similar to Telegram/ChatGPT)
BG_COLOR = "#0e1621"          # Deep telegram dark background
BUBBLE_BOT = "#182533"         # Darker slate blue for bot bubbles
BUBBLE_USER = "#2b5278"        # Soft blue for user bubbles
ACCENT_COLOR = "#5288c1"      # Accent blue for icons/highlights
TEXT_COLOR = "#f5f5f5"        # White text
MUTED_TEXT = "#7f91a4"        # Muted grey text
INPUT_BG = "#17212b"          # Dark input container background
INPUT_BORDER = "#24303f"      # Input border line

# Standard Q&A dictionary for offline chatbot logic
OFFLINE_KNOWLEDGE = {
    "hello": "Hello there! I am your Auspify Internship Assistant. How can I help you today?",
    "hi": "Hi! How can I assist you with your Python internship tasks today?",
    "hey": "Hey! Need some help coding your Python tasks?",
    "how are you": "I am running optimally and ready to help you write clean code! How are you?",
    "what is this project": "This is Task 6 of your Auspify Python Developer Internship—an intelligent AI Chatbot designed to respond to user queries with a premium GUI interface.",
    "who are you": "I am your Auspify AI Chatbot. I can answer queries locally, or connect to the internet via the Google Gemini API to have advanced conversations!",
    "what are the internship tasks": "The internship requires completing any 4 of the following 6 tasks:\n1. Password Generator (Easy)\n2. To-Do List Application (Easy)\n3. Calculator with GUI (Medium)\n4. Weather Information App (Medium)\n5. Expense Tracker System (Advanced)\n6. AI Chatbot Application (Advanced)",
    "help": "You can ask me questions about this internship, coding in Python, or ask me to tell a joke. You can also configure a Gemini API key at the bottom to talk to me about anything!",
    "python joke": "Why do programmers wear glasses? Because they can't C#! 😄",
    "tell me a joke": "How many programmers does it take to change a light bulb?\nNone, that's a hardware problem! 💡",
    "another joke": "What is a programmer's favorite hangout place?\nFoo Bar! 🍻",
    "who created python": "Python was created by Guido van Rossum and first released in 1991.",
    "what is pep 8": "PEP 8 is Python's style guide. It defines standards for formatting code (like using 4 spaces for indentation) to ensure maximum readability.",
    "how to track tasks": "You can use our Task 2 To-Do List application to manage and persist your daily tasks easily!",
    "how to track expenses": "You can use our Task 5 Expense Tracker System to log expenditures, choose categories, and view automatic SQL-based database analytics!",
    "how to check weather": "You can use our Task 4 Weather Information App to query real-time atmospheric stats using the Open-Meteo API!",
}

class ScrollableFrame(tk.Frame):
    """
    A custom scrollable frame class using Canvas and Scrollbar.
    Optimized for dynamic chat bubble additions.
    """
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.configure(bg=BG_COLOR)

        self.canvas = tk.Canvas(self, bg=BG_COLOR, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=BG_COLOR)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def scroll_to_bottom(self):
        """Forces the scrollbar to snap to the latest message."""
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)


class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auspify - Premium AI Chatbot")
        self.root.geometry("480x680")
        self.root.configure(bg=BG_COLOR)
        self.root.minsize(400, 500)

        # Config details for API key storage
        self.config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
        self.gemini_key = self.load_api_key()

        # Build UI layout
        self.create_header()
        
        # Main message scrollable area
        self.chat_container = ScrollableFrame(self.root)
        self.chat_container.pack(fill="both", expand=True, padx=15, pady=10)

        self.create_input_section()
        self.create_api_key_widget()
        self.create_status_bar()

        # Typing bubble placeholder variable
        self.typing_bubble_frame = None

        # Display initial welcome message
        self.add_message_bubble("Bot", OFFLINE_KNOWLEDGE["hello"])

    def load_api_key(self):
        """Loads Gemini API key from config.json or environment variables."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as file:
                    data = json.load(file)
                    return data.get("gemini_key", "")
            except:
                pass
        return os.environ.get("GEMINI_API_KEY", "")

    def save_api_key(self, new_key):
        """Saves Gemini API key to config.json."""
        self.gemini_key = new_key.strip()
        try:
            with open(self.config_path, "w") as file:
                json.dump({"gemini_key": self.gemini_key}, file)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration:\n{str(e)}")

    def create_header(self):
        """Creates the telegram-style header section."""
        header = tk.Frame(self.root, bg=INPUT_BG, height=60, bd=0)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        # App title status
        info_frame = tk.Frame(header, bg=INPUT_BG)
        info_frame.pack(side="left", padx=20, pady=8)

        title = tk.Label(
            info_frame,
            text="Internship AI Assistant",
            font=("Segoe UI", 12, "bold"),
            bg=INPUT_BG,
            fg=TEXT_COLOR
        )
        title.pack(anchor="w")

        self.status_sub = tk.Label(
            info_frame,
            text="Online",
            font=("Segoe UI", 9),
            bg=INPUT_BG,
            fg=ACCENT_COLOR
        )
        self.status_sub.pack(anchor="w")

    def create_input_section(self):
        """Creates a modern bottom message input bar."""
        input_container = tk.Frame(self.root, bg=INPUT_BG, bd=1, highlightbackground=INPUT_BORDER, highlightcolor=INPUT_BORDER, highlightthickness=1)
        input_container.pack(fill="x", side="bottom")

        # Inner pad wrapper
        pad_frame = tk.Frame(input_container, bg=INPUT_BG, pady=10, padx=15)
        pad_frame.pack(fill="x")

        # Custom text entry container
        entry_bg = tk.Frame(pad_frame, bg=BG_COLOR, bd=0)
        entry_bg.pack(side="left", fill="x", expand=True, ipady=4)

        self.user_entry = tk.Entry(
            entry_bg,
            font=("Segoe UI", 11),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            bd=0,
            highlightthickness=0
        )
        self.user_entry.pack(side="left", fill="x", expand=True, padx=12)
        self.user_entry.bind("<Return>", lambda e: self.send_message())

        # Send Button styled as circular teal icon
        self.send_btn = tk.Button(
            pad_frame,
            text="➤",
            font=("Segoe UI", 12, "bold"),
            bg=ACCENT_COLOR,
            fg=TEXT_COLOR,
            activebackground="#4271a3",
            activeforeground=TEXT_COLOR,
            bd=0,
            cursor="hand2",
            padx=10,
            pady=2,
            command=self.send_message
        )
        self.send_btn.pack(side="right", padx=(10, 0))

    def create_api_key_widget(self):
        """Creates the collapsed Gemini API key config box."""
        settings_frame = tk.Frame(self.root, bg=BG_COLOR)
        settings_frame.pack(fill="x", side="bottom", padx=15, pady=(5, 5))

        self.key_visible = False

        self.toggle_link = tk.Label(
            settings_frame,
            text="🔑 Configure Gemini API Key",
            font=("Segoe UI", 8, "underline"),
            bg=BG_COLOR,
            fg=ACCENT_COLOR,
            cursor="hand2"
        )
        self.toggle_link.pack(anchor="e")
        self.toggle_link.bind("<Button-1>", lambda e: self.toggle_api_section())

        self.key_box = tk.Frame(settings_frame, bg=INPUT_BG, pady=6, padx=10)
        
        tk.Label(self.key_box, text="Gemini Key:", font=("Segoe UI", 8), bg=INPUT_BG, fg=TEXT_COLOR).pack(side="left")
        
        self.key_entry = tk.Entry(
            self.key_box, 
            font=("Segoe UI", 8), 
            bg=BG_COLOR, 
            fg=TEXT_COLOR, 
            bd=1, 
            relief="flat",
            width=26
        )
        self.key_entry.pack(side="left", padx=5)
        self.key_entry.insert(0, self.gemini_key)

        save_btn = tk.Button(
            self.key_box,
            text="Save",
            font=("Segoe UI", 8, "bold"),
            bg=ACCENT_COLOR,
            fg=TEXT_COLOR,
            bd=0,
            cursor="hand2",
            padx=8,
            command=self.save_key_action
        )
        save_btn.pack(side="left")

    def toggle_api_section(self):
        """Toggles visibility of the Gemini API input box."""
        if self.key_visible:
            self.key_box.pack_forget()
            self.key_visible = False
        else:
            self.key_box.pack(fill="x", pady=4, side="bottom")
            self.key_visible = True

    def save_key_action(self):
        """Saves key from the settings box."""
        new_key = self.key_entry.get().strip()
        self.save_api_key(new_key)
        self.toggle_api_section()
        self.update_mode_status()
        self.add_message_bubble("System", "Gemini API key updated successfully.")

    def create_status_bar(self):
        """Creates the bottom status bar."""
        footer = tk.Frame(self.root, bg=INPUT_BG)
        footer.pack(fill="x", side="bottom", ipady=4)

        self.status_lbl = tk.Label(
            footer,
            text="",
            font=("Segoe UI", 8, "bold"),
            bg=INPUT_BG,
            fg=TEXT_COLOR
        )
        self.status_lbl.pack(side="left", padx=15)
        self.update_mode_status()

        brand = tk.Label(
            footer,
            text="Auspify Technologies",
            font=("Segoe UI", 8, "italic"),
            bg=INPUT_BG,
            fg=MUTED_TEXT
        )
        brand.pack(side="right", padx=15)

    def update_mode_status(self):
        """Updates the status bar telling user if the chatbot is in offline or live AI mode."""
        if self.gemini_key:
            self.status_lbl.configure(text="🤖 Live AI Mode Active", fg="#4caf50")
            self.status_sub.configure(text="AI Online", fg="#4caf50")
        else:
            self.status_lbl.configure(text="⚡ Local Helper Mode (No Key)", fg=ACCENT_COLOR)
            self.status_sub.configure(text="Local Assistant", fg=ACCENT_COLOR)

    def add_message_bubble(self, sender, text):
        """Packs a structured chat bubble layout inside the scrollable canvas."""
        # Main row container
        row = tk.Frame(self.chat_container.scrollable_frame, bg=BG_COLOR)
        row.pack(fill="x", pady=6)

        # Bubble configuration based on sender
        if sender == "System":
            lbl = tk.Label(
                row,
                text=text,
                font=("Segoe UI", 8, "italic"),
                bg=BG_COLOR,
                fg=MUTED_TEXT,
                justify="center"
            )
            lbl.pack(fill="x", pady=2)
            self.chat_container.scroll_to_bottom()
            return
            
        elif sender == "User":
            bubble_color = BUBBLE_USER
            text_align = "right"
            pack_side = "right"
            padx_val = (50, 10)  # indent bubble slightly from left wall
        else:
            bubble_color = BUBBLE_BOT
            text_align = "left"
            pack_side = "left"
            padx_val = (10, 50)  # indent bubble slightly from right wall

        # Inner bubble container card
        bubble = tk.Frame(row, bg=bubble_color, padx=12, pady=8)
        bubble.pack(side=pack_side, padx=padx_val)

        # Message Text Label
        msg_lbl = tk.Label(
            bubble,
            text=text,
            font=("Segoe UI", 10),
            bg=bubble_color,
            fg=TEXT_COLOR,
            justify=text_align,
            wraplength=280,   # wrap long texts
            anchor="w" if sender != "User" else "e"
        )
        msg_lbl.pack()

        # Timestamp/metadata
        t_stamp = time.strftime("%H:%M")
        time_lbl = tk.Label(
            bubble,
            text=t_stamp,
            font=("Segoe UI", 7),
            bg=bubble_color,
            fg=MUTED_TEXT
        )
        time_lbl.pack(anchor="e", pady=(2, 0))

        self.chat_container.scroll_to_bottom()

    def show_typing_indicator(self):
        """Displays an animating typing bubble on the left side."""
        if self.typing_bubble_frame:
            return

        self.typing_bubble_frame = tk.Frame(self.chat_container.scrollable_frame, bg=BG_COLOR)
        self.typing_bubble_frame.pack(fill="x", pady=6)

        bubble = tk.Frame(self.typing_bubble_frame, bg=BUBBLE_BOT, padx=15, pady=8)
        bubble.pack(side="left", padx=(10, 50))

        self.typing_label = tk.Label(
            bubble,
            text="Typing .",
            font=("Segoe UI", 9, "italic"),
            bg=BUBBLE_BOT,
            fg=MUTED_TEXT
        )
        self.typing_label.pack()
        
        self.chat_container.scroll_to_bottom()
        self.animate_typing(1)

    def animate_typing(self, step):
        """Animates typing dot extensions dynamically."""
        if not self.typing_bubble_frame:
            return
        
        dots = "." * (step % 4)
        if dots == "":
            dots = "."
        
        self.typing_label.configure(text=f"Typing {dots}")
        
        # Schedule next animation frame
        self.root.after(400, lambda: self.animate_typing(step + 1))

    def remove_typing_indicator(self):
        """Destroys the animating typing bubble."""
        if self.typing_bubble_frame:
            self.typing_bubble_frame.destroy()
            self.typing_bubble_frame = None

    def send_message(self):
        """Retrieves text from Entry box, displays it, and triggers response generation."""
        user_query = self.user_entry.get().strip()
        if not user_query:
            return

        # Show user message
        self.add_message_bubble("User", user_query)
        self.user_entry.delete(0, tk.END)

        # Show typing indicator
        self.show_typing_indicator()

        # Fire a background thread to generate response so the UI doesn't freeze
        self.send_btn.configure(state="disabled")
        threading.Thread(target=self.generate_response_thread, args=(user_query,), daemon=True).start()

    def generate_response_thread(self, query):
        """Background thread worker to search local database or request Gemini API."""
        response = ""
        
        # Simulate network latency slightly to make typing animation feel realistic!
        time.sleep(random.uniform(0.6, 1.2))

        # If API key exists, try reaching Gemini API
        if self.gemini_key:
            response = self.fetch_gemini_response(query)

        # Fallback to local Q&A engine if response is empty (no key or request failed)
        if not response:
            response = self.get_offline_response(query)

        # Push back response to GUI main thread
        self.root.after(0, self.push_response_to_ui, response)

    def push_response_to_ui(self, response):
        """Runs in main thread to update Chat log and re-enable send button."""
        self.remove_typing_indicator()
        self.add_message_bubble("Bot", response)
        self.send_btn.configure(state="normal")

    def get_offline_response(self, query):
        """Fuzzy-matches query to local dict or gives default suggestion."""
        clean_query = re.sub(r'[^\w\s]', '', query.lower().strip())
        
        if clean_query in OFFLINE_KNOWLEDGE:
            return OFFLINE_KNOWLEDGE[clean_query]

        keys = list(OFFLINE_KNOWLEDGE.keys())
        matches = difflib.get_close_matches(clean_query, keys, n=1, cutoff=0.6)
        
        if matches:
            matched_key = matches[0]
            return OFFLINE_KNOWLEDGE[matched_key]

        if "joke" in clean_query:
            return OFFLINE_KNOWLEDGE["tell me a joke"]
        elif "task" in clean_query or "todo" in clean_query:
            return OFFLINE_KNOWLEDGE["how to track tasks"]
        elif "expense" in clean_query or "money" in clean_query:
            return OFFLINE_KNOWLEDGE["how to track expenses"]
        elif "weather" in clean_query or "rain" in clean_query:
            return OFFLINE_KNOWLEDGE["how to check weather"]
        
        return (
            "I'm not quite sure about that query in my offline knowledge base.\n\n"
            "💡 Tip: Try asking about 'internship tasks', 'tell me a joke', 'how to track expenses', "
            "or register a Gemini API key at the bottom for open-ended questions!"
        )

    def fetch_gemini_response(self, query):
        """Performs raw POST request to Gemini REST API endpoint."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_key}"
        headers = {"Content-Type": "application/json"}
        
        prompt = (
            "You are a helpful assistant for a student doing a Python Developer Internship "
            f"at Auspify Technologies. Answer this query professionally: {query}"
        )
        
        body = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }

        try:
            response = requests.post(url, headers=headers, json=body, timeout=8)
            if response.status_code == 200:
                data = response.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                return text
            else:
                return ""
        except Exception:
            return ""


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotApp(root)
    root.mainloop()
