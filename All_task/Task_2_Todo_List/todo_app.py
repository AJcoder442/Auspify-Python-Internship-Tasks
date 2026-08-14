import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import os

# Define color palette for a premium dark mode
BG_COLOR = "#121212"          # Deep dark background
CARD_BG = "#1e1e1e"           # Slightly lighter dark for task items/containers
ACCENT_COLOR = "#00adb5"      # Modern teal/cyan accent
TEXT_COLOR = "#eeeeee"        # Crisp white text
MUTED_TEXT = "#888888"        # Gray text for completed/subtle items
BUTTON_BG = "#393e46"         # Gray button background
BUTTON_HOVER = "#00adb5"      # Accent color on hover
DELETE_BG = "#cf6679"         # Muted red for delete button
DELETE_HOVER = "#ff4d6d"      # Bright red on hover

class ScrollableFrame(tk.Frame):
    """
    A custom scrollable frame class using Canvas and Scrollbar.
    This allows the list of tasks to scale gracefully when many tasks are added.
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
        
        # Bind canvas configuration to make the inner frame expand to the canvas width
        self.canvas.bind('<Configure>', self._on_canvas_configure)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Enable mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_canvas_configure(self, event):
        # Stretch the inner frame to match the canvas width
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        # Scroll canvas with mouse wheel
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auspify - Premium To-Do List")
        self.root.geometry("500x650")
        self.root.configure(bg=BG_COLOR)
        
        # Set minimum window size
        self.root.minsize(400, 500)

        # File path for database
        self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")
        self.tasks = []
        
        # Load existing tasks
        self.load_tasks()

        # Build UI Header
        self.create_header()

        # Build Task Input Box
        self.create_input_section()

        # Build Task List Container (Scrollable)
        self.task_list_frame = ScrollableFrame(self.root)
        self.task_list_frame.pack(fill="both", expand=True, padx=25, pady=10)

        # Build Footer (Stats Panel)
        self.create_footer()

        # Populate initial tasks
        self.render_tasks()

    def create_header(self):
        """Creates the top branding header."""
        header_frame = tk.Frame(self.root, bg=BG_COLOR)
        header_frame.pack(fill="x", padx=25, pady=(25, 10))

        # Title text
        title_label = tk.Label(
            header_frame, 
            text="AUSPIFY TASK MANAGER", 
            font=("Segoe UI", 16, "bold"), 
            bg=BG_COLOR, 
            fg=ACCENT_COLOR
        )
        title_label.pack(anchor="w")

        # Subtitle text
        subtitle_label = tk.Label(
            header_frame, 
            text="Organize and track your daily internship tasks.", 
            font=("Segoe UI", 10), 
            bg=BG_COLOR, 
            fg=MUTED_TEXT
        )
        subtitle_label.pack(anchor="w", pady=(2, 0))

    def create_input_section(self):
        """Creates the input field and add button."""
        input_frame = tk.Frame(self.root, bg=BG_COLOR)
        input_frame.pack(fill="x", padx=25, pady=15)

        # Custom entry styling container
        entry_container = tk.Frame(input_frame, bg=CARD_BG, bd=1, relief="flat")
        entry_container.pack(side="left", fill="x", expand=True, ipady=4)

        # New Task Entry
        self.task_entry = tk.Entry(
            entry_container, 
            font=("Segoe UI", 11), 
            bg=CARD_BG, 
            fg=TEXT_COLOR, 
            insertbackground=TEXT_COLOR, # caret color
            bd=0, 
            highlightthickness=0
        )
        self.task_entry.pack(side="left", fill="x", expand=True, padx=10)
        self.task_entry.bind("<Return>", lambda event: self.add_task())
        
        # Placeholder text implementation
        self.placeholder_text = "What needs to be done today?"
        self.task_entry.insert(0, self.placeholder_text)
        self.task_entry.configure(fg=MUTED_TEXT)
        
        self.task_entry.bind("<FocusIn>", self._clear_placeholder)
        self.task_entry.bind("<FocusOut>", self._restore_placeholder)

        # Add Button
        self.add_btn = tk.Button(
            input_frame,
            text="+ Add Task",
            font=("Segoe UI", 10, "bold"),
            bg=ACCENT_COLOR,
            fg=BG_COLOR,
            activebackground="#008b91",
            activeforeground=BG_COLOR,
            bd=0,
            cursor="hand2",
            padx=15,
            command=self.add_task
        )
        self.add_btn.pack(side="right", padx=(10, 0), ipady=5)
        
        # Add button hover effect
        self.add_btn.bind("<Enter>", lambda e: self.add_btn.configure(bg="#00d8e2"))
        self.add_btn.bind("<Leave>", lambda e: self.add_btn.configure(bg=ACCENT_COLOR))

    def _clear_placeholder(self, event):
        if self.task_entry.get() == self.placeholder_text:
            self.task_entry.delete(0, tk.END)
            self.task_entry.configure(fg=TEXT_COLOR)

    def _restore_placeholder(self, event):
        if not self.task_entry.get().strip():
            self.task_entry.delete(0, tk.END)
            self.task_entry.insert(0, self.placeholder_text)
            self.task_entry.configure(fg=MUTED_TEXT)

    def create_footer(self):
        """Creates the bottom stats bar."""
        self.footer_frame = tk.Frame(self.root, bg=CARD_BG)
        self.footer_frame.pack(fill="x", side="bottom", ipady=10)

        self.stats_label = tk.Label(
            self.footer_frame, 
            text="0 of 0 tasks completed", 
            font=("Segoe UI", 9, "bold"), 
            bg=CARD_BG, 
            fg=TEXT_COLOR
        )
        self.stats_label.pack(side="left", padx=25)

        # A subtle brand label
        brand_label = tk.Label(
            self.footer_frame, 
            text="Auspify Technologies", 
            font=("Segoe UI", 8, "italic"), 
            bg=CARD_BG, 
            fg=MUTED_TEXT
        )
        brand_label.pack(side="right", padx=25)

    def render_tasks(self):
        """Renders/Updates the list of tasks dynamically."""
        # Clear existing items in scrollable frame
        for widget in self.task_list_frame.scrollable_frame.winfo_children():
            widget.destroy()

        if not self.tasks:
            # If task list is empty, display a placeholder message
            empty_label = tk.Label(
                self.task_list_frame.scrollable_frame,
                text="🎉 All caught up! Create a task above.",
                font=("Segoe UI", 11, "italic"),
                bg=BG_COLOR,
                fg=MUTED_TEXT,
                pady=40
            )
            empty_label.pack(fill="x", expand=True)
            self.update_stats()
            return

        for index, task in enumerate(self.tasks):
            # Container for individual task row
            task_row = tk.Frame(self.task_list_frame.scrollable_frame, bg=CARD_BG, bd=0)
            task_row.pack(fill="x", pady=5, ipady=4)

            # Checkbox to complete task
            is_completed = tk.BooleanVar(value=task["completed"])
            
            # Custom styled styling checkbutton
            cb = tk.Checkbutton(
                task_row,
                variable=is_completed,
                bg=CARD_BG,
                activebackground=CARD_BG,
                activeforeground=TEXT_COLOR,
                selectcolor=BG_COLOR,  # tick container bg in standard tkinter
                bd=0,
                cursor="hand2",
                highlightthickness=0,
                command=lambda idx=index, var=is_completed: self.toggle_task(idx, var.get())
            )
            cb.pack(side="left", padx=(10, 5))

            # Task Text (with visual strikethrough if completed)
            font_style = ("Segoe UI", 11)
            text_color = TEXT_COLOR
            if task["completed"]:
                font_style = ("Segoe UI", 11, "overstrike")
                text_color = MUTED_TEXT

            task_lbl = tk.Label(
                task_row,
                text=task["title"],
                font=font_style,
                bg=CARD_BG,
                fg=text_color,
                anchor="w",
                justify="left",
                wraplength=320 # wrap long task text
            )
            task_lbl.pack(side="left", fill="x", expand=True, padx=5, pady=5)
            
            # Allow clicking the text to toggle the checkbox
            task_lbl.bind("<Button-1>", lambda event, idx=index, var=is_completed: self.toggle_task(idx, not var.get()))

            # Delete Button
            del_btn = tk.Button(
                task_row,
                text="✕",
                font=("Segoe UI", 9, "bold"),
                bg=CARD_BG,
                fg=MUTED_TEXT,
                activebackground=DELETE_BG,
                activeforeground=BG_COLOR,
                bd=0,
                cursor="hand2",
                padx=8,
                pady=2,
                relief="flat",
                command=lambda idx=index: self.delete_task(idx)
            )
            del_btn.pack(side="right", padx=(5, 10))

            # Bind hover animations to Delete button
            def on_enter(e, btn=del_btn):
                btn.configure(bg=DELETE_BG, fg=TEXT_COLOR)
            def on_leave(e, btn=del_btn):
                btn.configure(bg=CARD_BG, fg=MUTED_TEXT)
            
            del_btn.bind("<Enter>", on_enter)
            del_btn.bind("<Leave>", on_leave)

        self.update_stats()

    def add_task(self):
        """Adds a new task from the input box."""
        task_text = self.task_entry.get().strip()
        
        # Guard clause for empty tasks or placeholders
        if not task_text or task_text == self.placeholder_text:
            messagebox.showwarning("Empty Task", "Please enter a valid task description.")
            return

        # Add to list
        self.tasks.append({
            "title": task_text,
            "completed": False
        })

        # Save to file
        self.save_tasks()

        # Clear input box and reset placeholder behavior
        self.task_entry.delete(0, tk.END)
        self.root.focus() # removes focus to trigger placeholder if configured

        # Re-render list
        self.render_tasks()

    def toggle_task(self, index, completed_val):
        """Toggles the completion status of a task."""
        self.tasks[index]["completed"] = completed_val
        self.save_tasks()
        self.render_tasks()

    def delete_task(self, index):
        """Deletes a task from the list."""
        self.tasks.pop(index)
        self.save_tasks()
        self.render_tasks()

    def update_stats(self):
        """Calculates and updates completion status stats in the footer."""
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task["completed"])
        self.stats_label.configure(text=f"{completed} of {total} tasks completed")

    def load_tasks(self):
        """Loads tasks database from tasks.json file."""
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r", encoding="utf-8") as file:
                    self.tasks = json.load(file)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load tasks database:\n{str(e)}")
                self.tasks = []

    def save_tasks(self):
        """Saves current task list to tasks.json file."""
        try:
            with open(self.db_path, "w", encoding="utf-8") as file:
                json.dump(self.tasks, file, indent=4, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks database:\n{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
