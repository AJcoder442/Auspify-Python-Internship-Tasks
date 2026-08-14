import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import os
from datetime import datetime

# Color Palette for consistent modern dark look
BG_COLOR = "#121212"          # Dark screen background
CARD_BG = "#1e1e1e"           # Card frame background
ACCENT_COLOR = "#00adb5"      # Cool cyan/teal
TEXT_COLOR = "#eeeeee"        # Bright text
MUTED_TEXT = "#888888"        # Gray text
ERROR_COLOR = "#cf6679"       # Soft red
SUCCESS_COLOR = "#4caf50"     # Soft green
PANEL_BORDER = "#2c2c2c"

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Auspify - Premium Expense Tracker")
        self.root.geometry("850x600")
        self.root.configure(bg=BG_COLOR)
        self.root.minsize(800, 500)

        # SQLite database setup
        self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expenses.db")
        self.init_db()

        # Categories list
        self.categories = ["Food", "Transport", "Rent", "Utilities", "Shopping", "Entertainment", "Education", "Others"]

        # Style Configuration
        self.setup_styles()

        # Build UI layout (Two Columns: Input Form and View/Analytics Board)
        self.create_header()
        
        main_content = tk.Frame(self.root, bg=BG_COLOR)
        main_content.pack(fill="both", expand=True, padx=25, pady=(10, 15))

        # Left Column: Input Panel
        self.left_panel = tk.Frame(main_content, bg=CARD_BG, width=280, padx=20, pady=20)
        self.left_panel.pack(side="left", fill="y", padx=(0, 15))
        self.left_panel.pack_propagate(False) # Keep width fixed
        self.create_input_form()

        # Right Column: View Dashboard
        self.right_panel = tk.Frame(main_content, bg=BG_COLOR)
        self.right_panel.pack(side="right", fill="both", expand=True)
        self.create_dashboard()

        # Populate table and analytics
        self.refresh_data()

    def init_db(self):
        """Initializes the SQLite database and creates the expenses table."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT,
                    amount REAL NOT NULL
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to initialize database:\n{str(e)}")

    def setup_styles(self):
        """Applies visual formatting styles for Tkinter widgets."""
        self.style = ttk.Style()
        self.style.theme_use("default")

        # Treeview styling (Dark mode sheet)
        self.style.configure(
            "Treeview",
            background=CARD_BG,
            foreground=TEXT_COLOR,
            fieldbackground=CARD_BG,
            rowheight=28,
            borderwidth=0,
            font=("Segoe UI", 10)
        )
        self.style.map(
            "Treeview",
            background=[("selected", ACCENT_COLOR)],
            foreground=[("selected", BG_COLOR)]
        )
        
        # Header columns styling
        self.style.configure(
            "Treeview.Heading",
            background="#252830",
            foreground=TEXT_COLOR,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            borderwidth=0
        )
        self.style.map(
            "Treeview.Heading",
            background=[("active", ACCENT_COLOR)],
            foreground=[("active", BG_COLOR)]
        )

        # Combobox styling
        self.style.configure(
            "TCombobox",
            postoffset=(0, 0, 0, 0),
            fieldbackground=CARD_BG,
            background=CARD_BG,
            foreground=TEXT_COLOR,
            arrowcolor=TEXT_COLOR
        )

    def create_header(self):
        """Creates the header section."""
        header = tk.Frame(self.root, bg=BG_COLOR)
        header.pack(fill="x", padx=25, pady=(25, 10))

        title = tk.Label(
            header,
            text="AUSPIFY EXPENSE TRACKER",
            font=("Segoe UI", 16, "bold"),
            bg=BG_COLOR,
            fg=ACCENT_COLOR
        )
        title.pack(anchor="w")

        subtitle = tk.Label(
            header,
            text="Record, categorize, and analyze your expenditures instantly.",
            font=("Segoe UI", 10),
            bg=BG_COLOR,
            fg=MUTED_TEXT
        )
        subtitle.pack(anchor="w", pady=(2, 0))

    def create_input_form(self):
        """Creates the input form inside the left panel."""
        tk.Label(self.left_panel, text="ADD NEW EXPENSE", font=("Segoe UI", 12, "bold"), bg=CARD_BG, fg=ACCENT_COLOR).pack(anchor="w", pady=(0, 15))

        # Amount Input
        tk.Label(self.left_panel, text="Amount ($):", font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=TEXT_COLOR).pack(anchor="w", pady=(5, 2))
        amount_container = tk.Frame(self.left_panel, bg=BG_COLOR, bd=1, relief="flat")
        amount_container.pack(fill="x", ipady=3)
        self.amount_entry = tk.Entry(amount_container, font=("Segoe UI", 10), bg=BG_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, bd=0, highlightthickness=0)
        self.amount_entry.pack(fill="x", padx=8)

        # Category Combobox
        tk.Label(self.left_panel, text="Category:", font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=TEXT_COLOR).pack(anchor="w", pady=(12, 2))
        self.category_box = ttk.Combobox(self.left_panel, values=self.categories, state="readonly", font=("Segoe UI", 10))
        self.category_box.pack(fill="x")
        self.category_box.set("Food")

        # Date Input
        tk.Label(self.left_panel, text="Date (YYYY-MM-DD):", font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=TEXT_COLOR).pack(anchor="w", pady=(12, 2))
        date_container = tk.Frame(self.left_panel, bg=BG_COLOR, bd=1, relief="flat")
        date_container.pack(fill="x", ipady=3)
        self.date_entry = tk.Entry(date_container, font=("Segoe UI", 10), bg=BG_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, bd=0, highlightthickness=0)
        self.date_entry.pack(fill="x", padx=8)
        self.date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))

        # Description Input
        tk.Label(self.left_panel, text="Description:", font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=TEXT_COLOR).pack(anchor="w", pady=(12, 2))
        desc_container = tk.Frame(self.left_panel, bg=BG_COLOR, bd=1, relief="flat")
        desc_container.pack(fill="x", ipady=3)
        self.desc_entry = tk.Entry(desc_container, font=("Segoe UI", 10), bg=BG_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, bd=0, highlightthickness=0)
        self.desc_entry.pack(fill="x", padx=8)

        # Submit Button
        self.submit_btn = tk.Button(
            self.left_panel,
            text="+ Record Expense",
            font=("Segoe UI", 10, "bold"),
            bg=ACCENT_COLOR,
            fg=BG_COLOR,
            activebackground="#008b91",
            activeforeground=BG_COLOR,
            bd=0,
            cursor="hand2",
            command=self.add_expense
        )
        self.submit_btn.pack(fill="x", pady=25, ipady=5)
        self.submit_btn.bind("<Enter>", lambda e: self.submit_btn.configure(bg="#00d8e2"))
        self.submit_btn.bind("<Leave>", lambda e: self.submit_btn.configure(bg=ACCENT_COLOR))

    def create_dashboard(self):
        """Creates the right side containing the expense list and statistical analytics."""
        # Top Stats Bar
        stats_frame = tk.Frame(self.right_panel, bg=CARD_BG, pady=12)
        stats_frame.pack(fill="x", pady=(0, 15))

        stats_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(1, weight=1)

        # Stat 1: Total Spending
        self.total_lbl = tk.Label(stats_frame, text="$0.00", font=("Segoe UI", 16, "bold"), bg=CARD_BG, fg=ACCENT_COLOR)
        self.total_lbl.grid(row=0, column=0, sticky="nsew")
        tk.Label(stats_frame, text="TOTAL EXPENDITURES", font=("Segoe UI", 8, "bold"), bg=CARD_BG, fg=MUTED_TEXT).grid(row=1, column=0, sticky="nsew")

        # Stat 2: Top Category
        self.top_cat_lbl = tk.Label(stats_frame, text="None", font=("Segoe UI", 16, "bold"), bg=CARD_BG, fg=TEXT_COLOR)
        self.top_cat_lbl.grid(row=0, column=1, sticky="nsew")
        tk.Label(stats_frame, text="TOP CATEGORY", font=("Segoe UI", 8, "bold"), bg=CARD_BG, fg=MUTED_TEXT).grid(row=1, column=1, sticky="nsew")

        # Table Container
        table_container = tk.Frame(self.right_panel, bg=CARD_BG)
        table_container.pack(fill="both", expand=True)

        # Treeview Scrollbar
        scroll = ttk.Scrollbar(table_container, orient="vertical")
        scroll.pack(side="right", fill="y")

        # Table itself
        cols = ("ID", "Date", "Category", "Description", "Amount")
        self.tree = ttk.Treeview(table_container, columns=cols, show="headings", yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.configure(command=self.tree.yview)

        # Configure columns widths and alignments
        self.tree.heading("ID", text="ID")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Amount", text="Amount")

        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("Date", width=95, anchor="center")
        self.tree.column("Category", width=95, anchor="center")
        self.tree.column("Description", width=220, anchor="w")
        self.tree.column("Amount", width=90, anchor="e")

        # Bottom Action Bar
        action_bar = tk.Frame(self.right_panel, bg=BG_COLOR)
        action_bar.pack(fill="x", pady=(15, 0))

        self.del_btn = tk.Button(
            action_bar,
            text="✕ Delete Selected",
            font=("Segoe UI", 9, "bold"),
            bg=CARD_BG,
            fg=MUTED_TEXT,
            activebackground=ERROR_COLOR,
            activeforeground=TEXT_COLOR,
            bd=0,
            cursor="hand2",
            padx=15,
            pady=5,
            command=self.delete_selected
        )
        self.del_btn.pack(side="left")
        self.del_btn.bind("<Enter>", lambda e: self.del_btn.configure(bg=ERROR_COLOR, fg=TEXT_COLOR))
        self.del_btn.bind("<Leave>", lambda e: self.del_btn.configure(bg=CARD_BG, fg=MUTED_TEXT))

        brand_lbl = tk.Label(
            action_bar,
            text="Auspify Technologies",
            font=("Segoe UI", 8, "italic"),
            bg=BG_COLOR,
            fg=MUTED_TEXT
        )
        brand_lbl.pack(side="right", pady=5)

    def add_expense(self):
        """Records an expense from input boxes and saves it to SQLite database."""
        amount_raw = self.amount_entry.get().strip()
        category = self.category_box.get()
        date = self.date_entry.get().strip()
        description = self.desc_entry.get().strip()

        # Validate inputs
        if not amount_raw:
            messagebox.showwarning("Validation Error", "Amount is required.")
            return

        try:
            amount = float(amount_raw)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Validation Error", "Amount must be a positive number.")
            return

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Validation Error", "Date must follow YYYY-MM-DD format.")
            return

        # Insert to database
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO expenses (date, category, description, amount) VALUES (?, ?, ?, ?)",
                (date, category, description, amount)
            )
            conn.commit()
            conn.close()

            # Clean fields
            self.amount_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            
            # Reset date
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))

            self.refresh_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to record expense:\n{str(e)}")

    def delete_selected(self):
        """Deletes selected row in Treeview from SQLite database."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Select Item", "Please click on a row to delete.")
            return

        # Fetch primary key ID
        item_vals = self.tree.item(selected_item)["values"]
        expense_id = item_vals[0]

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this expense record?")
        if not confirm:
            return

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
            conn.commit()
            conn.close()

            self.refresh_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete record:\n{str(e)}")

    def refresh_data(self):
        """Reloads records from database to populate Treeview and stats panels."""
        # Empty existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id, date, category, description, amount FROM expenses ORDER BY date DESC, id DESC")
            rows = cursor.fetchall()

            total_sum = 0.0
            category_totals = {}

            for r in rows:
                id_, date, cat, desc, amt = r
                total_sum += amt
                category_totals[cat] = category_totals.get(cat, 0.0) + amt
                
                # Format visual output: amount in $ currency formatting
                self.tree.insert("", "end", values=(id_, date, cat, desc, f"${amt:.2f}"))

            # Update stats panels
            self.total_lbl.configure(text=f"${total_sum:.2f}")

            if category_totals:
                # Find category with maximum expense
                top_cat = max(category_totals, key=category_totals.get)
                self.top_cat_lbl.configure(text=f"{top_cat} (${category_totals[top_cat]:.2f})")
            else:
                self.top_cat_lbl.configure(text="None")

            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch database information:\n{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
