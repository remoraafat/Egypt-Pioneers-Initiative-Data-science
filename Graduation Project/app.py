# app.py
import streamlit as st
import tempfile
import os
import json
import requests
from resume_parser import extract_text_from_pdf
from resume_analyzer import analyze_resume
from chat_memory import init_db, save_message, get_chat_history, clear_chat_history
from auth import init_users_db, register_user, login_user

# === Initialize Databases ===
init_db()
init_users_db()

# === Configure Streamlit ===
st.set_page_config(page_title="HR Resume Chatbot", layout="centered")
st.title("📄 HR Resume Chatbot")
st.markdown("Upload your resume (PDF) to get job suggestions, a score, and tips!")

# === Session state init ===
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_data = None

# === Login/Register UI ===
def login_ui():
    st.subheader("🔐 Login or Register")
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            success, user_data = login_user(email, password)
            if success:
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_data = user_data
                    # st.success(f"Welcome back, {user_data['name']}!")
                    st.rerun()
            else:
                st.error("Invalid email or password.")

    with tab2:
        name = st.text_input("Full Name", key="reg_name")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_pass")
        gender = st.radio("Gender", ["Male", "Female", "Other"], key="reg_gender")
        if st.button("Register"):
            if not name or not email or not password:
                st.error("Please fill all fields.")
            else:
                success, msg = register_user(name, email, password, gender)
                if success:
                        success, user_data = login_user(email, password)
                        st.session_state.logged_in = True
                        st.session_state.user_data = user_data
                        st.rerun()
                else:
                    st.error(msg)


# === Require Login ===
if not st.session_state.logged_in:
    login_ui()
    st.stop()

# === Logged-in Info ===
USER_ID = st.session_state.user_data['user_id']
user_name = user_name = st.session_state.user_data['name']
with st.sidebar:
    user_name = st.session_state.user_data['name']
    st.markdown(
        f"""
        <div style='
            background-color: #2E8B57;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            color: white;
            margin-bottom: 20px;
        '>
            <h3 style='margin-bottom: 5px;'>👋 Welcome, {user_name}!</h3>
            <p style='font-size: 14px;'>You're logged into the HR Resume Chatbot.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Description of Sidebar Purpose
    st.markdown(
        """
        **What can you do here?**
        - Upload your resume and job description.
        - Analyze and get tailored job suggestions.
        - Chat with the HR bot for resume tips.
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")

    # Centered Logout Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_data = None
            st.rerun()


# === Resume Upload ===
uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

# === Optional Job Description Upload ===
st.markdown("---")
st.markdown("Optionally upload a Job Description (PDF) to get a tailored analysis.")
jd_file = st.file_uploader("Upload job description (PDF)", type=["pdf"], key="jd")

def extract_pdf_text(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    text = extract_text_from_pdf(tmp_path)
    os.remove(tmp_path)
    return text

jd_text = extract_pdf_text(jd_file) if jd_file else None

if uploaded_file:
    resume_text = extract_pdf_text(uploaded_file)

    # === Analyze Resume ===
    if st.button("🔍 Analyze Resume"):
        with st.spinner("Analyzing your resume..."):
            result = analyze_resume(resume_text, jd_text)

        try:
            parsed = json.loads(result)
            pretty_response = (
                f"👤 **Name:** {parsed.get('Name', 'N/A')}\n\n"
                f"📧 **Email:** {parsed.get('Email', 'N/A')}\n\n"
                f"📞 **Phone:** {parsed.get('Phone', 'N/A')}\n\n"
                f"🔗 **LinkedIn:** {parsed.get('LinkedIn', 'N/A')}\n\n"
                f"🐙 **GitHub:** {parsed.get('GitHub', 'N/A')}\n\n"
                f"💼 **Suggested Job Titles:**\n" +
                "\n".join([f"- {t}" for t in parsed.get("job_titles", [])]) + "\n\n"
                f"📊 **Resume Score:** **{parsed.get('score', 'N/A')} / 100**\n\n"
                f"💼 **Experience:**\n{parsed.get('experience', 'N/A')}\n\n"
                f"🎓 **Education:**\n{parsed.get('education', 'N/A')}\n\n"
                f"🛠️ **Skills:**\n{parsed.get('skills', 'N/A')}\n\n"
                f"📜 **Certifications:**\n{parsed.get('certifications', 'N/A')}\n\n"
                f"🛠️ **Suggestions to Improve:**\n" +
                "\n".join([f"- {s}" for s in parsed.get("suggestions", [])])
            )



            save_message(USER_ID, "user", "Analyze Resume")
            save_message(USER_ID, "assistant", pretty_response)

            st.success("✅ Analysis complete!")
            # st.markdown(pretty_response)

        except json.JSONDecodeError:
            st.error("⚠️ Failed to parse the response. Please try again.")
            st.text(result)

# === Chat History ===
st.divider()
st.subheader("💬 Chat with the HR Bot")
history = get_chat_history(USER_ID, limit=None)
for role, message in history:
    with st.chat_message(role):
        st.markdown(message)

# === Chat Input ===
if user_question := st.chat_input("Ask anything about your resume..."):
    save_message(USER_ID, "user", user_question)
    with st.chat_message("user"):
        st.markdown(user_question)

    past = get_chat_history(USER_ID)
    messages = [{"role": role, "content": msg} for role, msg in past]
    messages.append({"role": "user", "content": user_question})

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "deepseek/deepseek-prover-v2:free",
        "messages": messages,
        "temperature": 0.0,
    }

    with st.spinner("Thinking..."):
        try:
            res = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                data=json.dumps(payload)
            )
            res.raise_for_status()
            message_content = res.json()["choices"][0]["message"]["content"]
        except Exception as e:
            message_content = f"Error: {e}"

        with st.chat_message("assistant"):
            st.markdown(message_content)

        save_message(USER_ID, "assistant", message_content)

# === Clear Chat History ===
st.divider()
if 'confirm_delete' not in st.session_state:
    st.session_state.confirm_delete = False

if st.button("🗑️ Clear All Chat History"):
    st.session_state.confirm_delete = True

if st.session_state.confirm_delete:
    st.warning("Are you sure you want to delete all chat history? This cannot be undone.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes, delete all history"):
            clear_chat_history(USER_ID)
            st.experimental_rerun()
    with col2:
        if st.button("Cancel"):
            st.session_state.confirm_delete = False