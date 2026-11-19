import ast
from pathlib import Path

# Only allow access inside the CodeMate workspace
WORKSPACE = Path(__file__).resolve().parent

# Files the agent is allowed to read
ALLOWED_EXTENSIONS = {
    ".py", ".txt", ".md", ".json", ".html",
    ".css", ".js", ".ts", ".java", ".c",
    ".cpp", ".h", ".cs", ".go", ".rs", ".sql"
}

IGNORED_NAMES = {
    ".env", "venv", "__pycache__", ".git",
    ".idea", ".vscode"
}


def list_files():
    """List project files without exposing sensitive files."""

    items = []

    for item in sorted(WORKSPACE.iterdir()):
        if item.name in IGNORED_NAMES or item.name.startswith("."):
            continue

        if item.is_dir():
            items.append(f"[FOLDER] {item.name}")
        elif item.is_file():
            items.append(f"[FILE] {item.name}")

    return "\n".join(items) if items else "No project files found."


def read_file(path: str):
    """Read an allowed source file from the project workspace."""

    try:
        requested_path = Path(path)

        if requested_path.is_absolute():
            return "Error: Absolute paths are not allowed."

        file_path = (WORKSPACE / requested_path).resolve()

        # Prevent access outside the workspace
        if not file_path.is_relative_to(WORKSPACE):
            return "Error: Access outside the project folder is not allowed."

        # Prevent access to sensitive folders and files
        if any(part in IGNORED_NAMES or part.startswith(".")
               for part in requested_path.parts):
            return "Error: Access to hidden or sensitive files is not allowed."

        if not file_path.is_file():
            return "Error: File does not exist."

        if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
            return "Error: This file type is not allowed."

        if file_path.stat().st_size > 100_000:
            return "Error: File is too large to read."

        return file_path.read_text(encoding="utf-8")

    except UnicodeDecodeError:
        return "Error: File is not a readable text file."

    except OSError as error:
        return f"File reading error: {error}"

def write_file(path: str, content: str):
    """Create a new source-code file without overwriting existing files."""

    try:
        requested_path = Path(path)

        if requested_path.is_absolute():
            return "Error: Absolute paths are not allowed."

        file_path = (WORKSPACE / requested_path).resolve()

        # Prevent access outside the workspace
        if not file_path.is_relative_to(WORKSPACE):
            return "Error: Access outside the project folder is not allowed."

        # Block hidden and sensitive paths
        if any(
            part in IGNORED_NAMES or part.startswith(".")
            for part in requested_path.parts
        ):
            return "Error: Hidden or sensitive paths are not allowed."

        # Allow only approved file types
        if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
            return "Error: This file type is not allowed."

        # Never overwrite an existing file
        if file_path.exists():
            return "Error: File already exists. No changes were made."

        # Create parent directories if needed
        file_path.parent.mkdir(parents=True, exist_ok=True)

        file_path.write_text(content, encoding="utf-8")

        return f"Successfully created file: {requested_path}"

    except OSError as error:
        return f"File creation error: {error}"

import subprocess
import sys


def run_python_file(path: str):
    """Execute a Python file inside the CodeMate workspace."""

    try:
        requested_path = Path(path)

        if requested_path.is_absolute():
            return "Error: Absolute paths are not allowed."

        file_path = (WORKSPACE / requested_path).resolve()

        if not file_path.is_relative_to(WORKSPACE):
            return "Error: Access outside workspace is not allowed."

        if any(
            part in IGNORED_NAMES or part.startswith(".")
            for part in requested_path.parts
        ):
            return "Error: Hidden or sensitive paths are blocked."

        if file_path.suffix.lower() != ".py":
            return "Error: Only Python files can be executed."

        if not file_path.is_file():
            return "Error: Python file not found."

        result = subprocess.run(
            [sys.executable, str(file_path)],
            cwd=WORKSPACE,
            capture_output=True,
            text=True,
            timeout=10
        )

        output = result.stdout or ""

        if result.stderr:
            output += "\nErrors:\n" + result.stderr

        if not output:
            output = "Program executed without output."

        return (
            f"Exit code: {result.returncode}\n"
            f"Execution result:\n{output}"
        )

    except subprocess.TimeoutExpired:
        return "Error: Execution timed out after 10 seconds."

    except OSError as error:
        return f"Execution error: {error}"

import difflib


def edit_file(path: str, new_content: str):
    """Edit an existing project file after explicit user approval."""

    try:
        requested_path = Path(path)

        if requested_path.is_absolute():
            return "Error: Absolute paths are not allowed."

        file_path = (WORKSPACE / requested_path).resolve()

        # Workspace security check
        if not file_path.is_relative_to(WORKSPACE):
            return "Error: Access outside workspace is not allowed."

        # Block hidden and sensitive paths
        if any(
            part in IGNORED_NAMES or part.startswith(".")
            for part in requested_path.parts
        ):
            return "Error: Hidden or sensitive files are blocked."

        if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
            return "Error: This file type is not allowed."

        if not file_path.is_file():
            return "Error: File does not exist."

        if file_path.stat().st_size > 100_000:
            return "Error: File is too large to edit."

        old_content = file_path.read_text(encoding="utf-8")

        if old_content == new_content:
            return "No changes needed. File is already up to date."

        # Show the proposed changes
        diff = difflib.unified_diff(
            old_content.splitlines(),
            new_content.splitlines(),
            fromfile="Current file",
            tofile="Proposed file",
            lineterm=""
        )

        print("\nProposed changes:")
        print("\n".join(diff))

        # Ask the human for approval
        approval = input(
            "\nDo you approve these changes? Type YES to confirm: "
        ).strip()

        if approval.upper() != "YES":
            return "Edit cancelled. No changes were made."

        # Apply the approved changes
        file_path.write_text(new_content, encoding="utf-8")

        return f"Successfully updated {requested_path} with your approval."

    except UnicodeDecodeError:
        return "Error: File is not a readable text file."

    except OSError as error:
        return f"File editing error: {error}"

def check_python_syntax(path: str):
    """Check Python code for syntax errors without executing it."""

    try:
        requested_path = Path(path)

        if requested_path.is_absolute():
            return "Error: Absolute paths are not allowed."

        file_path = (WORKSPACE / requested_path).resolve()

        if not file_path.is_relative_to(WORKSPACE):
            return "Error: Access outside workspace is not allowed."

        if any(
            part in IGNORED_NAMES or part.startswith(".")
            for part in requested_path.parts
        ):
            return "Error: Hidden or sensitive files are blocked."

        if file_path.suffix.lower() != ".py":
            return "Error: Only Python files can be checked."

        if not file_path.is_file():
            return "Error: Python file not found."

        if file_path.stat().st_size > 100_000:
            return "Error: File is too large to check."

        source = file_path.read_text(encoding="utf-8")

        compile(source, str(file_path), "exec")

        return f"Syntax check passed: {requested_path} contains no syntax errors."

    except SyntaxError as error:
        return (
            f"Syntax error in {path}:\n"
            f"Line: {error.lineno}\n"
            f"Error: {error.msg}"
        )

    except UnicodeDecodeError:
        return "Error: File is not a readable text file."

    except OSError as error:
        return f"Syntax checking error: {error}"

def analyze_code(path: str):
    """Analyze Python code quality using Pylint."""

    try:
        requested_path = Path(path)

        if requested_path.is_absolute():
            return "Error: Absolute paths are not allowed."

        file_path = (WORKSPACE / requested_path).resolve()

        if not file_path.is_relative_to(WORKSPACE):
            return "Error: Access outside workspace is not allowed."

        if any(
            part in IGNORED_NAMES or part.startswith(".")
            for part in requested_path.parts
        ):
            return "Error: Hidden or sensitive files are blocked."

        if file_path.suffix.lower() != ".py":
            return "Error: Only Python files can be analyzed."

        if not file_path.is_file():
            return "Error: Python file not found."

        if file_path.stat().st_size > 100_000:
            return "Error: File is too large to analyze."

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pylint",
                "--score=n",
                "--reports=n",
                str(file_path)
            ],
            cwd=WORKSPACE,
            capture_output=True,
            text=True,
            timeout=30
        )

        output = result.stdout + result.stderr

        if not output.strip():
            output = "No code quality issues reported by Pylint."

        return (
            f"Pylint exit code: {result.returncode}\n"
            f"Code analysis results:\n{output}"
        )

    except subprocess.TimeoutExpired:
        return "Error: Code analysis timed out."

    except OSError as error:
        return f"Analysis error: {error}"

def project_summary():
    """Summarize the files present in the CodeMate workspace."""

    try:
        files = []

        for item in sorted(WORKSPACE.iterdir()):
            if item.name in IGNORED_NAMES or item.name.startswith("."):
                continue

            if item.is_file():
                files.append(f"- {item.name}")

            elif item.is_dir():
                files.append(f"- [Folder] {item.name}")

        if not files:
            return "The project workspace is empty."

        return (
            "CodeMate Project Files:\n"
            + "\n".join(files)
        )

    except OSError as error:
        return f"Project summary error: {error}"

import difflib

# Stores a proposed edit until the user approves or rejects it.
PENDING_EDIT = None


def stage_file_edit(path: str, new_content: str):
    """Prepare a file edit for user approval without changing the file."""
    global PENDING_EDIT

    try:
        requested_path = Path(path)

        if requested_path.is_absolute():
            return "Error: Absolute paths are not allowed."

        file_path = (WORKSPACE / requested_path).resolve()

        if not file_path.is_relative_to(WORKSPACE):
            return "Error: Access outside workspace is not allowed."

        if any(
            part in IGNORED_NAMES or part.startswith(".")
            for part in requested_path.parts
        ):
            return "Error: Hidden or sensitive files are blocked."

        if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
            return "Error: This file type is not allowed."

        if not file_path.is_file():
            return "Error: File does not exist."

        if file_path.stat().st_size > 100_000:
            return "Error: File is too large to edit."

        old_content = file_path.read_text(encoding="utf-8")

        if old_content == new_content:
            return "No changes needed. The file is already up to date."

        diff = "\n".join(difflib.unified_diff(
            old_content.splitlines(),
            new_content.splitlines(),
            fromfile="Current file",
            tofile="Proposed file",
            lineterm=""
        ))

        PENDING_EDIT = {
            "path": str(requested_path),
            "old_content": old_content,
            "new_content": new_content,
            "diff": diff
        }

        return (
            "File edit prepared. No changes have been made yet.\n"
            "The user must review and approve the proposed changes."
        )

    except (OSError, UnicodeDecodeError) as error:
        return f"Error preparing file edit: {error}"


def get_pending_edit():
    """Return the currently staged edit."""
    return PENDING_EDIT


def discard_pending_edit():
    """Discard the proposed edit without changing the file."""
    global PENDING_EDIT
    PENDING_EDIT = None
    return "Proposed edit rejected. No changes were made."


def apply_pending_edit():
    """Apply a staged edit after the user approves it."""
    global PENDING_EDIT

    if PENDING_EDIT is None:
        return "Error: No pending edit to approve."

    try:
        requested_path = Path(PENDING_EDIT["path"])
        file_path = (WORKSPACE / requested_path).resolve()

        if not file_path.is_relative_to(WORKSPACE):
            return "Error: Access outside workspace is not allowed."

        if not file_path.is_file():
            return "Error: File no longer exists."

        if file_path.read_text(encoding="utf-8") != PENDING_EDIT["old_content"]:
            return "Error: File changed after the proposal. Please prepare a new edit."

        file_path.write_text(
            PENDING_EDIT["new_content"],
            encoding="utf-8"
        )

        PENDING_EDIT = None

        return f"Successfully updated {requested_path} with your approval."

    except (OSError, UnicodeDecodeError) as error:
        return f"Error applying edit: {error}"
