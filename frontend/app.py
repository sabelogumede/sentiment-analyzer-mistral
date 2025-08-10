# Streamlit frontend for sentiment analyzer using Mistral via Ollama
# Features: live char count, non-text detection, loading state, clear input, and explanation

import streamlit as st
import requests
import re  # For input validation

# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Mistral Sentiment Analyzer",
    page_icon="🎭",
    layout="centered"
)

# -----------------------------------------------------------------------------
# App Title & Description
# -----------------------------------------------------------------------------
st.title("🎭 Sentiment Analyzer (Mistral)")
st.markdown(
    """
    Powered by **Mistral via Ollama** – runs 100% locally.  
    Classify text as **Positive**, **Negative**, or **Neutral** — no data leaves your machine.

    ⏳ **Be patient** – analysis takes **5–60 seconds**, depending on input length.
    """
)

# -----------------------------------------------------------------------------
# Input Section with Live Character Count
# -----------------------------------------------------------------------------
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("### Enter text to analyze:")

# Get input from user
raw_input = st.text_area(
    "Input text",
    value=st.session_state.get("input_text", ""),
    height=150,
    placeholder="I love this product! It works perfectly.",
    label_visibility="collapsed"
)

# Safely handle None and normalize
current_text = (raw_input or "").strip()
st.session_state.input_text = current_text

# Character count
char_count = len(current_text)

# Display count
st.markdown(
    f"<p style='text-align: right; color: #666; font-size: 0.9em;'>Characters: {char_count}</p>",
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# Input Validation: Warn if no letters (likely non-text)
# -----------------------------------------------------------------------------
if current_text:
    # Check if input contains any letters (a-z or A-Z)
    if not re.search(r'[a-zA-Z]', current_text):
        st.warning("⚠️ Input contains no letters. Sentiment analysis works best with natural language (e.g., sentences). Results may be neutral by default.")

# -----------------------------------------------------------------------------
# Initialize Session State
# -----------------------------------------------------------------------------
if "sentiment_result" not in st.session_state:
    st.session_state.sentiment_result = None
if "explanation" not in st.session_state:
    st.session_state.explanation = None

# -----------------------------------------------------------------------------
# Analyze Button
# -----------------------------------------------------------------------------
if st.button("🔍 Analyze Sentiment", type="primary"):
    if not current_text:
        st.error("❌ Please enter text to analyze.")
    elif len(current_text) < 3:
        st.error("❌ Text too short. Enter at least 3 characters.")
    else:
        # Reset previous results
        st.session_state.sentiment_result = None
        st.session_state.explanation = None

        with st.spinner("🧠 Mistral is analyzing sentiment..."):
            try:
                response = requests.post(
                    "http://localhost:8000/analyze/",
                    json={"text": current_text},
                    timeout=35
                )

                if response.status_code == 200:
                    sentiment = response.json().get("sentiment", "Unknown")
                    st.session_state.sentiment_result = sentiment
                else:
                    error = response.json().get("detail", "Unknown error")
                    st.error(f"❌ Failed: {error}")

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend. Is FastAPI running?")
            except requests.exceptions.Timeout:
                st.error("⏰ Request timed out. Try shorter text.")
            except Exception as e:
                st.error(f"💥 Error: {e}")

# -----------------------------------------------------------------------------
# Display Result with Explanation
# -----------------------------------------------------------------------------
if st.session_state.sentiment_result:
    sentiment = st.session_state.sentiment_result

    # Color-coded output
    if sentiment == "Positive":
        st.subheader("🟢 Predicted Sentiment: **Positive**")
    elif sentiment == "Negative":
        st.subheader("🔴 Predicted Sentiment: **Negative**")
    else:
        st.subheader("🟡 Predicted Sentiment: **Neutral**")

    # ✅ Generate explanation only once
    if st.session_state.explanation is None:
        with st.spinner("🧠 Generating explanation..."):
            try:
                explanation_res = requests.post(
                    "http://localhost:8000/explain/",
                    json={
                        "text": current_text,
                        "sentiment": sentiment
                    },
                    timeout=30
                )
                if explanation_res.status_code == 200:
                    explanation = explanation_res.json().get("explanation", "No explanation available.")
                else:
                    explanation = "Could not generate explanation."
            except Exception as e:
                explanation = "Could not connect to explanation service."

            st.session_state.explanation = explanation

    # ✅ Display explanation
    st.markdown("#### 🔍 Why?")
    st.write(st.session_state.explanation)

# -----------------------------------------------------------------------------
# Clear Input & Result Button
# -----------------------------------------------------------------------------
if st.session_state.sentiment_result and st.session_state.input_text:
    if st.button("🗑️ Clear Input & Result", type="secondary"):
        st.session_state.input_text = ""