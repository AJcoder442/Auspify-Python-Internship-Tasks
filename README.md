# Python Developer Internship Project Portfolio - Auspify Technologies

Welcome to my Python Developer Internship portfolio repository. This repository contains the source code, databases, configuration files, and running instructions for my internship tasks.

Per the program guidelines, **4 out of the 6 required tasks** have been implemented. To showcase advanced user experience (UX) and clean visual designs, **all 4 tasks have been built with a modern, customized Graphical User Interface (GUI)** using Python's standard `tkinter` library.

---

## 📂 Repository Structure

The projects are organized in individual task folders:

```text
e:\internships\Remote\
├── Task_2_Todo_List/              # Task 2: To-Do List Application (GUI)
│   ├── todo_app.py                # Main executable application
│   ├── tasks.json                 # JSON database (auto-created)
│   └── README.md                  # Project details & user guide
│
├── Task_4_Weather_App/            # Task 4: Weather Information App (GUI)
│   ├── weather_app.py             # Main executable application
│   └── README.md                  # Project details & user guide
│
├── Task_5_Expense_Tracker/        # Task 5: Expense Tracker System (GUI)
│   ├── expense_tracker.py         # Main executable application
│   ├── expenses.db                # SQLite database (auto-created)
│   └── README.md                  # SQL schema & dashboard details
│
├── Task_6_AI_Chatbot/             # Task 6: AI Chatbot Application (GUI)
│   ├── chatbot_app.py             # Main executable application
│   ├── config.json                # Gemini API key storage (auto-created)
│   └── README.md                  # Chatbot flow & configuration steps
│
├── Launch_Expense_Tracker.bat     # Windows Double-click Launcher for Task 5
└── README.md                      # This main directory index guide
```

---

## 🛠️ Summary of Implemented Tasks

### 1. [Task 2: To-Do List Application](file:///e:/internships/Remote/Task_2_Todo_List/README.md)
* **Goal**: Manage daily tasks efficiently with persistence.
* **Implementation**: Built with a responsive layout where tasks are dynamic checkable rows. Users can add new tasks, check tasks as completed (applying strikethroughs and color fading), or delete tasks.
* **Storage**: Data is saved automatically in real-time to a `tasks.json` file.
* **Key Command**: `python Task_2_Todo_List/todo_app.py`

### 2. [Task 4: Weather Information App](file:///e:/internships/Remote/Task_4_Weather_App/README.md)
* **Goal**: Fetch real-time weather parameters using an external API.
* **Implementation**: Integrates with the **Open-Meteo Free API** to geocode city names and fetch real-time parameters (Temperature, Humidity, Wind speed, and Pressure) dynamically without requiring any API keys.
* **Fail-Safe Mechanism**: If the app is offline, it transitions to **Demo Mode** and simulates realistic weather data.
* **Key Command**: `python Task_4_Weather_App/weather_app.py`

### 3. [Task 5: Expense Tracker System](file:///e:/internships/Remote/Task_5_Expense_Tracker/README.md)
* **Goal**: Log, classify, and analyze daily expenditures.
* **Implementation**: Formulates a dual-panel dashboard. The left panel serves as the input form with validations. The right panel includes a spreadsheet-style table (`ttk.Treeview`) and real-time total aggregations and top-spending category calculations.
* **Storage**: Integrates directly with an embedded **SQLite3** relational database (`expenses.db`).
* **Key Command**: `python Task_5_Expense_Tracker/expense_tracker.py`

### 4. [Task 6: AI Chatbot Application](file:///e:/internships/Remote/Task_6_AI_Chatbot/README.md)
* **Goal**: Develop an intelligent chatbot that responds to user queries.
* **Implementation**: Built with a scrollable messaging logs interface. It supports asynchronous background execution for network requests to guarantee the GUI never freezes.
* **Response Methods**:
  * **Offline Mode (Default)**: Employs fuzzy keyword matching (`difflib`) to answer questions about the internship, give python tips, and tell programming jokes.
  * **Gemini AI Mode**: Connects directly to the **Google Gemini REST API** if a user provides an API key inside the app settings.
* **Key Command**: `python Task_6_AI_Chatbot/chatbot_app.py`

---

## 🚀 Getting Started

### Prerequisites
Make sure you have Python 3.10+ installed.

### Dependencies
Only one external dependency is used (`requests`), which is typically pre-installed or can be fetched via:
```bash
pip install requests
```

### Running the Apps
### Running the Apps

#### Option A: Windows Double-Click Launcher (Easy)
For **Task 5 (Expense Tracker)**, you can run the app instantly without opening a terminal window by double-clicking:
* `Launch_Expense_Tracker.bat`

#### Option B: Terminal Command Line (All Platforms)
To run any of the applications, open your terminal at the root directory and execute:
```bash
# To-Do List Application
python Task_2_Todo_List/todo_app.py

# Weather Application
python Task_4_Weather_App/weather_app.py

# Expense Tracker System
python Task_5_Expense_Tracker/expense_tracker.py

# AI Chatbot Application
python Task_6_AI_Chatbot/chatbot_app.py
```

---

## 🌟 Professional Quality Standards Met
- **Clean Folder Hierarchy**: Standardized separate directories for every project as required.
- **Modern UI Styling**: Harmonious dark/slate styling, custom flat themes, hover states, and clear fonts (Segoe UI) across all applications.
- **Robust Error Handling**: Real-world fallbacks (offline modes, invalid formats warnings, API rate-limit recovery) to ensure 100% application uptime.
- **Documentation**: Dedicated explanatory documentation files in all project folders.
