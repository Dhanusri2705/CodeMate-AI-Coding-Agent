"""CodeMate AI Developer Workspace."""
import streamlit as st
from google.genai import types
import tools
from config import client, MODEL_NAME
from tools import (
    list_files,
    read_file,
    write_file,
    run_python_file,
    check_python_syntax,
    analyze_code,
    project_summary,
    stage_file_edit,
    WORKSPACE,
    ALLOWED_EXTENSIONS,
    IGNORED_NAMES
)
# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="CodeMate | Developer Workspace",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# PROFESSIONAL DASHBOARD STYLING
# =====================================================

st.markdown("""
<style>

/* Main application */

.stApp {
    background: #0b1020;
    color: #e5e7eb;
}

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

/* Sidebar */

[data-testid="stSidebar"] {
    background: #10182a;
    border-right: 1px solid #26344b;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #f8fafc;
}

/* Header */

.dashboard-title {
    font-size: 34px;
    font-weight: 800;
    color: #f8fafc;
    letter-spacing: -1px;
    margin-bottom: 4px;
}

.dashboard-subtitle {
    font-size: 14px;
    color: #94a3b8;
    margin-bottom: 25px;
}

.eyebrow {
    color: #60a5fa;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* Metric cards */

.metric-card {
    background: linear-gradient(145deg, #17243b, #111a2d);
    border: 1px solid #2b3c56;
    border-radius: 14px;
    padding: 20px;
    min-height: 120px;
    transition: 0.2s ease;
}

.metric-card:hover {
    border-color: #3b82f6;
    transform: translateY(-2px);
}

.metric-label {
    color: #94a3b8;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.metric-value {
    color: #f8fafc;
    font-size: 28px;
    font-weight: 800;
    margin-top: 12px;
}

.metric-description {
    color: #64748b;
    font-size: 11px;
    margin-top: 4px;
}

/* Section headings */

.section-heading {
    font-size: 21px;
    font-weight: 750;
    color: #f8fafc;
    margin-bottom: 5px;
}

.section-description {
    color: #94a3b8;
    font-size: 13px;
    margin-bottom: 18px;
}

/* Feature cards */

.feature-card {
    background: #121d31;
    border: 1px solid #293951;
    border-radius: 13px;
    padding: 18px;
    min-height: 125px;
}

.feature-icon {
    font-size: 23px;
    margin-bottom: 10px;
}

.feature-title {
    color: #f8fafc;
    font-weight: 700;
    font-size: 15px;
}

.feature-description {
    color: #94a3b8;
    font-size: 12px;
    margin-top: 6px;
}

/* Chat */

div[data-testid="stChatMessage"] {
    background: #121d31;
    border: 1px solid #293951;
    border-radius: 13px;
    padding: 15px;
    margin-bottom: 12px;
}

/* Buttons */

.stButton > button {
    border-radius: 9px;
    min-height: 42px;
    font-weight: 650;
    border: 1px solid #334155;
    transition: 0.2s ease;
}

.stButton > button:hover {
    border-color: #60a5fa;
    color: #ffffff;
}

/* Inputs */

.stTextInput input,
.stTextArea textarea {
    background: #111b2d;
    color: #f8fafc;
    border-radius: 9px;
    border: 1px solid #334155;
}

div[data-baseweb="select"] > div {
    background: #111b2d;
    border-color: #334155;
    border-radius: 9px;
}

/* Tabs */

button[data-baseweb="tab"] {
    color: #94a3b8;
    font-weight: 650;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #60a5fa;
}

/* Code panels */

div[data-testid="stCode"] {
    border: 1px solid #293951;
    border-radius: 11px;
}

/* Containers */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #111b2d;
    border-color: #293951;
    border-radius: 13px;
}

/* Dividers */

hr {
    border-color: #26344b;
}

/* Footer */

.footer-text {
    color: #64748b;
    font-size: 12px;
}

/* Hide Streamlit branding */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# GEMINI SYSTEM INSTRUCTIONS
# =====================================================

SYSTEM_INSTRUCTION = """
You are CodeMate, an intelligent AI coding assistant.

Help users write, understand, debug, execute and improve code.

AVAILABLE TOOLS:

1. list_files
   Lists project files.

2. read_file
   Reads existing files.

3. write_file
   Creates new files without overwriting existing files.

4. run_python_file
   Executes Python files and returns actual output.

5. check_python_syntax
   Checks Python syntax without executing files.

6. analyze_code
   Analyzes Python code using Pylint.

7. project_summary
   Summarizes the project.

8. stage_file_edit
   Prepares changes to an existing file for user approval.

IMPORTANT RULES:

- Use tools whenever required.
- Never invent file contents or tool results.
- Never claim an operation succeeded unless the tool confirms it.
- Read an existing file before preparing changes.
- Use stage_file_edit for changes to existing files.
- Never claim a proposed edit has already been applied.
- Wait for the user to approve changes in the dashboard.
- Never modify config.py or .env.
- Never expose API keys, passwords or secrets.
- Explain errors in simple language.
- Use actual tool output when reporting results.
"""


# =====================================================
# GEMINI CHAT
# =====================================================

def create_chat():

    return client.chats.create(
        model=MODEL_NAME,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            tools=[
                list_files,
                read_file,
                write_file,
                run_python_file,
                check_python_syntax,
                analyze_code,
                project_summary,
                stage_file_edit
            ]
        )
    )


# =====================================================
# SESSION STATE
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! 👋 I'm CodeMate, your AI coding assistant. "
                "Ask me to create, explain, debug or improve your code."
            )
        }
    ]

if "chat" not in st.session_state:
    st.session_state.chat = create_chat()

if "selected_content" not in st.session_state:
    st.session_state.selected_content = None

if "selected_name" not in st.session_state:
    st.session_state.selected_name = None

if "tool_result" not in st.session_state:
    st.session_state.tool_result = None

if "edit_result" not in st.session_state:
    st.session_state.edit_result = None


# =====================================================
# PROJECT FILE INFORMATION
# =====================================================

project_files = sorted([
    item.name
    for item in WORKSPACE.iterdir()
    if item.is_file()
    and item.suffix.lower() in ALLOWED_EXTENSIONS
    and not any(
        part in IGNORED_NAMES or part.startswith(".")
        for part in item.relative_to(WORKSPACE).parts
    )
])

python_files = [
    name for name in project_files
    if name.endswith(".py")
]


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("# 🤖 CodeMate")
    st.caption("AI DEVELOPER WORKSPACE")

    st.divider()

    st.markdown("### 🟢 System Status")
    st.success("Gemini configured")
    st.caption(f"Active model: `{MODEL_NAME}`")

    st.divider()

    if st.button(
        "＋  New Conversation",
        use_container_width=True
    ):

        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello! 👋 What are we building today?"
            }
        ]

        st.session_state.chat = create_chat()
        st.session_state.edit_result = None
        st.session_state.tool_result = None

        tools.discard_pending_edit()

        st.rerun()

    st.markdown("### 📁 Workspace Explorer")

    if project_files:

        sidebar_file = st.selectbox(
            "Project files",
            project_files,
            label_visibility="collapsed",
            key="sidebar_file"
        )

        if st.button(
            "📄 Open Selected File",
            use_container_width=True
        ):

            content = read_file(sidebar_file)

            if content.startswith("Error:"):
                st.error(content)
            else:
                st.session_state.selected_name = sidebar_file
                st.session_state.selected_content = content
                st.rerun()

    else:
        st.info("No project files found.")

    st.divider()

    st.markdown("### 🛠️ Agent Capabilities")

    st.caption("✦ AI code generation")
    st.caption("✦ Code explanation")
    st.caption("✦ File management")
    st.caption("✦ Python execution")
    st.caption("✦ Syntax validation")
    st.caption("✦ Pylint analysis")
    st.caption("✦ Human-approved editing")

    st.divider()

    st.caption("CodeMate v1.0")
    st.caption("Built with Python • Streamlit • Gemini")


# =====================================================
# MAIN DASHBOARD HEADER
# =====================================================

st.markdown(
    '<div class="eyebrow">AI POWERED DEVELOPMENT ENVIRONMENT</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-title">CodeMate Workspace</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Your intelligent coding partner — build, debug, analyze and improve code.'
    '</div>',
    unsafe_allow_html=True
)


# =====================================================
# DASHBOARD METRICS
# =====================================================

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">📁 Project Files</div>
            <div class="metric-value">{len(project_files)}</div>
            <div class="metric-description">Supported workspace files</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with metric2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">🐍 Python Files</div>
            <div class="metric-value">{len(python_files)}</div>
            <div class="metric-description">Python source files</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with metric3:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">🤖 AI Engine</div>
            <div class="metric-value">Gemini</div>
            <div class="metric-description">AI coding assistant</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with metric4:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">⚡ Workspace</div>
            <div class="metric-value">Active</div>
            <div class="metric-description">Development environment</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.write("")


# =====================================================
# NAVIGATION TABS
# =====================================================

tab_chat, tab_files, tab_tools, tab_overview = st.tabs([
    "💬  AI Assistant",
    "📁  Project Explorer",
    "⚙️  Developer Tools",
    "📊  Project Overview"
])


# =====================================================
# AI ASSISTANT
# =====================================================

with tab_chat:

    st.markdown(
        '<div class="section-heading">Your AI Coding Partner</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Ask questions, generate code, debug errors and manage your project.'
        '</div>',
        unsafe_allow_html=True
    )

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_prompt = st.chat_input(
        "Message CodeMate... (e.g. Explain my main.py file)"
    )

    if user_prompt:

        st.session_state.messages.append({
            "role": "user",
            "content": user_prompt
        })

        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):

            with st.spinner("CodeMate is working on your request..."):

                try:

                    response = st.session_state.chat.send_message(
                        user_prompt
                    )

                    answer = (
                        response.text
                        or "I couldn't generate a text response."
                    )

                    st.markdown(answer)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })

                except Exception as error:

                    error_message = f"An error occurred: {error}"

                    st.error(error_message)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_message
                    })


# =====================================================
# PROJECT EXPLORER
# =====================================================

with tab_files:

    st.markdown(
        '<div class="section-heading">Workspace Explorer</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Browse your project files and inspect source code.'
        '</div>',
        unsafe_allow_html=True
    )

    if project_files:

        file_col, action_col = st.columns([3, 1])

        with file_col:

            selected_project_file = st.selectbox(
                "Choose a project file",
                project_files,
                key="project_file_select"
            )

        with action_col:

            st.write("")

            if st.button(
                "Open File",
                type="primary",
                use_container_width=True
            ):

                content = read_file(selected_project_file)

                if content.startswith("Error:"):
                    st.error(content)
                else:
                    st.session_state.selected_name = selected_project_file
                    st.session_state.selected_content = content

        if st.session_state.selected_content is not None:

            st.divider()

            st.markdown(
                f"### 📄 {st.session_state.selected_name}"
            )

            extension = (
                st.session_state.selected_name.rsplit(".", 1)[-1]
                .lower()
            )

            language_map = {
                "py": "python",
                "js": "javascript",
                "ts": "typescript",
                "html": "html",
                "css": "css",
                "json": "json",
                "md": "markdown",
                "sql": "sql"
            }

            st.code(
                st.session_state.selected_content,
                language=language_map.get(extension, "text"),
                line_numbers=True
            )

    else:
        st.info("No supported project files found.")


# =====================================================
# DEVELOPER TOOLS
# =====================================================

with tab_tools:

    st.markdown(
        '<div class="section-heading">Developer Tools</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Execute Python files, validate syntax and analyze code quality.'
        '</div>',
        unsafe_allow_html=True
    )

    if python_files:

        target_file = st.selectbox(
            "Select a Python file",
            python_files,
            key="developer_target"
        )

        st.write("")

        run_col, syntax_col, pylint_col = st.columns(3)

        with run_col:

            with st.container(border=True):

                st.markdown("### ▶️")
                st.markdown("**Run Python**")
                st.caption("Execute the selected Python file.")

                if st.button(
                    "Run File",
                    key="run_python",
                    type="primary",
                    use_container_width=True
                ):

                    with st.spinner("Executing Python file..."):

                        st.session_state.tool_result = (
                            run_python_file(target_file)
                        )

                        st.session_state.tool_name = (
                            f"Python Execution — {target_file}"
                        )

        with syntax_col:

            with st.container(border=True):

                st.markdown("### ✓")
                st.markdown("**Syntax Validator**")
                st.caption("Check for Python syntax errors.")

                if st.button(
                    "Check Syntax",
                    key="check_syntax",
                    use_container_width=True
                ):

                    with st.spinner("Checking syntax..."):

                        st.session_state.tool_result = (
                            check_python_syntax(target_file)
                        )

                        st.session_state.tool_name = (
                            f"Syntax Validation — {target_file}"
                        )

        with pylint_col:

            with st.container(border=True):

                st.markdown("### 🔍")
                st.markdown("**Code Quality**")
                st.caption("Inspect code using Pylint.")

                if st.button(
                    "Analyze Code",
                    key="analyze_code",
                    use_container_width=True
                ):
                    with st.spinner("Running Pylint..."):
                        st.session_state.tool_result = (
                            analyze_code(target_file)
                        )
                        st.session_state.tool_name = (
                            f"Pylint Analysis — {target_file}"
                        )
    else:
        st.info("No Python files are available in this workspace.")
    st.write("")
    with st.container(border=True):
        st.markdown("### 📋 Project Summary")
        st.caption(
            "Generate an overview of the files and folders in your project."
        )
        if st.button(
            "Generate Project Summary",
            key="generate_summary",
            use_container_width=True
        ):
            with st.spinner("Generating project summary..."):
                st.session_state.tool_result = project_summary()
                st.session_state.tool_name = "Project Summary"
    # Tool output panel
    if st.session_state.tool_result is not None:
        st.write("")
        with st.container(border=True):
            output_col, clear_col = st.columns([4, 1])
            with output_col:
                st.markdown("### 🖥️ Tool Output")
                st.caption(
                    getattr(
                        st.session_state,
                        "tool_name",
                        "Latest developer tool result"
                    )
                )
            with clear_col:
                st.write("")

                if st.button(
                    "Clear Output",
                    use_container_width=True
                ):

                    st.session_state.tool_result = None
                    st.session_state.tool_name = None
                    st.rerun()
            st.code(
                str(st.session_state.tool_result),
                language="text"
            )
# =====================================================
# PROJECT OVERVIEW
# =====================================================
with tab_overview:
    st.markdown(
        '<div class="section-heading">Project Overview</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-description">'
        'An overview of CodeMate architecture and available capabilities.'
        '</div>',
        unsafe_allow_html=True
    )
    overview_col1, overview_col2 = st.columns(2)
    with overview_col1:
        with st.container(border=True):
            st.markdown("### 🤖 AI Capabilities")
            st.write("✦ Natural language coding assistance")
            st.write("✦ Code generation and explanation")
            st.write("✦ Debugging support")
            st.write("✦ Project file understanding")
            st.write("✦ Gemini-powered conversations")
    with overview_col2:
        with st.container(border=True):
            st.markdown("### 🛡️ Development Controls")
            st.write("✦ Human-approved file modifications")
            st.write("✦ Python syntax validation")
            st.write("✦ Pylint code analysis")
            st.write("✦ Python execution tools")
            st.write("✦ Workspace file management")
    st.divider()
    st.markdown("### 📂 Workspace Structure")
    if project_files:
        file_columns = st.columns(3)
        for index, filename in enumerate(project_files):
            with file_columns[index % 3]:
                st.markdown(
                    f"""
                    <div class="feature-card">
                        <div class="feature-icon">📄</div>
                        <div class="feature-title">{filename}</div>
                        <div class="feature-description">Project file</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.info("No project files found.")
# =====================================================
# HUMAN APPROVAL WORKFLOW
# =====================================================
pending = tools.get_pending_edit()
if pending:
    st.divider()
    st.markdown("## 📝 Pending Code Modification")
    st.warning(
        f"CodeMate has proposed changes to **{pending['path']}**. "
        "The file has not been modified yet."
    )
    st.markdown("### Review Proposed Changes")
    st.code(
        pending["diff"],
        language="diff"
    )
    approve_col, reject_col = st.columns(2)
    with approve_col:
        if st.button(
            "✅ Approve Changes",
            type="primary",
            use_container_width=True
        ):
            result = tools.apply_pending_edit()
            if result.startswith("Successfully"):
                verified = read_file(pending["path"])
                st.session_state.edit_result = result
                if not verified.startswith("Error:"):
                    st.session_state.selected_name = pending["path"]
                    st.session_state.selected_content = verified
                    st.session_state.edit_result += (
                        " File contents verified successfully."
                    )
            else:
                st.session_state.edit_result = result
            st.rerun()
    with reject_col:
        if st.button(
            "❌ Reject Changes",
            use_container_width=True
        ):
            st.session_state.edit_result = (
                tools.discard_pending_edit()
            )
            st.rerun()
# =====================================================
# EDIT RESULT
# =====================================================
if st.session_state.edit_result:
    st.success(st.session_state.edit_result)
    st.session_state.edit_result = None
# =====================================================
# FOOTER
# =====================================================
st.divider()
footer_col1, footer_col2 = st.columns(2)
with footer_col1:
    st.caption("🤖 CodeMate | AI Coding Agent")
with footer_col2:
    st.caption(
        "Powered by Python • Streamlit • Google Gemini"
    )