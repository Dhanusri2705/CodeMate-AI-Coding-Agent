
from google.genai import types

from config import client, MODEL_NAME

from tools import (
    list_files,
    read_file,
    write_file,
    run_python_file,
    edit_file,
    check_python_syntax,
    analyze_code,
    project_summary
)


# -----------------------------------
# SYSTEM INSTRUCTIONS
# -----------------------------------

SYSTEM_INSTRUCTION = """
You are CodeMate, an intelligent AI Coding Agent.

Your job is to help users:
- Understand Python and other project files.
- Create new files.
- Edit existing files with user approval.
- Debug programming errors.
- Execute Python programs.
- Check Python syntax.
- Analyze code quality.
- Summarize project files.

AVAILABLE TOOLS:

1. list_files
   Lists files and folders in the workspace.

2. read_file
   Reads the contents of an existing file.

3. write_file
   Creates a new file without overwriting an existing file.

4. edit_file
   Proposes changes to an existing file and requests user approval.

5. run_python_file
   Executes a Python file and returns its output.

6. check_python_syntax
   Checks Python files for syntax errors without executing them.

7. analyze_code
   Analyzes Python code quality using Pylint.

8. project_summary
   Provides an overview of the project files.

IMPORTANT RULES:

- Use the appropriate tools whenever necessary.
- Never invent file contents or tool results.
- Never claim a file was created unless write_file succeeds.
- Never claim a file was modified unless edit_file succeeds.
- Always use edit_file when modifying an existing file.
- Never modify .env or config.py without explicit user authorization.
- Never expose API keys, passwords, or secrets.
- Always use read_file to verify important file changes.
- Use run_python_file when the user requests program execution.
- Use check_python_syntax when the user requests a syntax check.
- Use analyze_code when the user requests code quality analysis.
- Do not execute code when the user only requests syntax checking.
- Explain technical concepts and errors in simple language.
- If a tool fails, clearly report the error.
- Never pretend an operation succeeded.
"""


# -----------------------------------
# CREATE GEMINI CHAT
# -----------------------------------

def create_chat():

    return client.chats.create(
        model=MODEL_NAME,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            tools=[
                list_files,
                read_file,
                write_file,
                edit_file,
                run_python_file,
                check_python_syntax,
                analyze_code,
                project_summary
            ]
        )
    )


# -----------------------------------
# MAIN APPLICATION
# -----------------------------------

def main():

    print("\n" + "=" * 40)
    print("          CODEMATE AI AGENT")
    print("=" * 40)

    print("\nConnecting to Gemini...")

    try:
        chat = create_chat()

    except Exception as error:

        print("\nConnection failed!")
        print(f"Error: {error}")
        return

    print("\nCodeMate is ready!")
    print("Type 'exit' to quit.")
    print("Type 'help' to view available commands.")

    print("\n" + "-" * 40)

    # -----------------------------------
    # CHAT LOOP
    # -----------------------------------

    while True:

        try:

            user_input = input("\nYou: ").strip()

            if not user_input:
                continue

            # Exit command
            if user_input.lower() in ["exit", "quit", "bye"]:

                print("\nCodeMate: Goodbye! Happy coding! 👋")
                break

            # Help command
            if user_input.lower() == "help":

                print("\nCodeMate can help you with:")

                print("1. List project files")
                print("2. Read and explain code")
                print("3. Create new files")
                print("4. Edit files with approval")
                print("5. Run Python programs")
                print("6. Check Python syntax")
                print("7. Analyze code quality using Pylint")
                print("8. Summarize project files")
                print("9. Debug programming errors")

                continue

            # -----------------------------------
            # SEND MESSAGE TO GEMINI
            # -----------------------------------

            try:

                print("\nCodeMate is thinking...")

                response = chat.send_message(user_input)

                answer = (
                    response.text
                    or "I couldn't generate a text response."
                )

                print("\nCodeMate:")
                print(answer)

            except Exception as error:

                print("\nCodeMate encountered an error.")
                print(f"Error: {error}")

        except KeyboardInterrupt:

            print("\n\nCodeMate: Session interrupted. Goodbye!")
            break

        except EOFError:

            print("\n\nCodeMate: Goodbye!")
            break


# -----------------------------------
# APPLICATION ENTRY POINT
# -----------------------------------

if __name__ == "__main__":
    main()
