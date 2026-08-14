# Task 5: Expense Tracker System (GUI)

A premium, interactive Graphical User Interface (GUI) application to record, categorize, and analyze daily expenses. It uses an embedded SQL database (`SQLite3`) for persistence, and computes automatic analytics on user expenditures.

## Key Features

- **Double-Panel Layout**:
  - **Left Form**: Easy input fields to log expense items, with input validation (numbers, date strings, category choice).
  - **Right Dashboard**: Dynamic analytics tracking total expenditures and showing the highest expense category alongside a database viewer.
- **Relational Storage**: Connects directly to SQLite (`expenses.db`), creating structured tables dynamically to save data securely.
- **Spreadsheet-style Table View**: Displays all recorded expenses using a custom styled `ttk.Treeview` spreadsheet with customizable fields and formatting.
- **Dynamic Aggregate Calculations**: Recalculates total sums and categorizes top-spending segments on addition or deletion in real time.
- **Record Deletion**: Select any entry from the table view and delete it with automatic database synchronization.
- **Premium Styling**: Styled with a dark-slate color scheme, custom tables, Segoe UI fonts, and hover highlight effects.

## Files

- `expense_tracker.py`: The Python application source code.
- `expenses.db`: Auto-generated database containing SQL table records.

## How to Run

1. Open a terminal in the folder.
2. Run the application:
   ```bash
   python expense_tracker.py
   ```

## Database Schema

The SQLite schema is set up automatically as:
```sql
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    amount REAL NOT NULL
);
```
Categories supported: `Food`, `Transport`, `Rent`, `Utilities`, `Shopping`, `Entertainment`, `Education`, and `Others`.
