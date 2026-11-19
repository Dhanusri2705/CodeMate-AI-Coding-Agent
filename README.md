# CodeMate – AI-Powered Coding Agent

An intelligent personal AI coding assistant built using Python, Google Gemini and Streamlit.

## Project Overview

CodeMate is an AI-powered coding agent that helps developers understand, create, execute, debug and improve code through a conversational interface and integrated development tools.

The project demonstrates the fundamentals of building an AI agent that interacts with a local development workspace using tools.

## Objectives

- Build a personal AI-powered coding agent from the ground up.
- Understand agentic execution loops and tool calling.
- Integrate Google Gemini with Python.
- Enable AI-assisted project file operations.
- Implement user-approved file modifications.
- Develop an interactive developer dashboard.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming |
| Google Gemini API | AI intelligence |
| Google Gen AI SDK | Model integration |
| Streamlit | Web dashboard |
| Pylint | Code quality analysis |
| python-dotenv | Environment configuration |
| Git and GitHub | Version control |

## Key Features

- Conversational AI coding assistant
- Project file listing and reading
- File creation and modification
- User approval before applying proposed edits
- Python file execution
- Python syntax validation
- Pylint code analysis
- Project overview and developer dashboard

## Project Structure

```text
CodeMate/
├── app.py
├── main.py
├── config.py
├── tools.py
├── calculator.py
├── test_calculator.py
├── hello.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Dhanusri2705/CodeMate-AI-Coding-Agent.git
cd CodeMate-AI-Coding-Agent
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Gemini API key

Create a `.env` file in the project directory:

```text
GEMINI_API_KEY=your_gemini_api_key
```

Never upload your API key to GitHub.

### 
