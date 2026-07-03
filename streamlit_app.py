import streamlit as st
import requests

# -----------------------------
# CONFIG
# -----------------------------

FASTAPI_URL = "shl-chatbot-production-0880.up.railway.app"

st.set_page_config(
    page_title="SHL Assessment Recommender",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# SIDEBAR
# -----------------------------

with st.sidebar:

    st.title("🤖 SHL AI")

    st.success("FastAPI Connected")

    st.write("---")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.write("---")

    st.markdown("""
### Features

✅ SHL Catalog

✅ Gemini AI

✅ Vector Search

✅ FastAPI Backend
""")

# -----------------------------
# TITLE
# -----------------------------

st.title("SHL Assessment Recommender")

st.caption("Conversational AI for SHL Product Catalog")

# -----------------------------
# CHAT HISTORY
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# USER INPUT
# -----------------------------

prompt = st.chat_input("Describe the role you are hiring for...")

if prompt:

    # Show User Message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Call FastAPI

    with st.spinner("Searching SHL Assessments..."):

        response = requests.post(

            FASTAPI_URL,

            json={

                "messages": st.session_state.messages

            }

        )

    if response.status_code == 200:

        data = response.json()

        reply = data["reply"]

        recommendations = data["recommendations"]

        end = data["end_of_conversation"]

        # Display Assistant

        with st.chat_message("assistant"):

            st.markdown(reply)

            if len(recommendations):

                st.write("## Recommended Assessments")

                for rec in recommendations:

                    st.markdown(f"""
### {rec['name']}

**Type**

{rec['test_type']}

🔗 {rec['url']}

---
""")

            if end:

                st.success("Conversation Complete")

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": reply
            }
        )

    else:

        st.error("Unable to connect FastAPI Server.")
