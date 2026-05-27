import streamlit as st
from core.extractor import extract_text
from core.summarizer import summarize_document, detect_risks
from core.rag import create_vector_store, ask_question
from core.translator import translate_text
import tempfile
import os

st.set_page_config(
    page_title="LegalLite",
    page_icon="",
    layout="wide"
)

st.markdown("""
<style>
    .stApp { background-color: #FAF7F2; color: #2C1810; }
    h1, h2, h3 { font-family: Georgia, serif; color: #2C1810; }
    p, li, div { color: #2C1810; }
    .stWarning { background-color: #FFF3E0; color: #2C1810; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("# LegalLite")
st.markdown("*Finally understand what you're signing.*")
st.divider()

col_up, col_space = st.columns([1, 2])
with col_up:
    uploaded_file = st.file_uploader(
        "Upload document",
        type=["pdf", "png", "jpg", "jpeg"],
        label_visibility="collapsed"
    )

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False,
        suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    with st.spinner("Reading your document..."):
        text = extract_text(tmp_path)

    st.success("Document read successfully.")

    if "vector_store" not in st.session_state:
        with st.spinner("Preparing chatbot..."):
            st.session_state.vector_store = create_vector_store(text)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Summary and Risk
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Plain English Summary")
        with st.spinner("Summarizing..."):
            summary = summarize_document(text)
        st.write(summary)

    with col2:
        st.subheader("Risk Flags")
        with st.spinner("Detecting risks..."):
            risks = detect_risks(text)
        st.warning(risks)

    st.divider()

    # Translation section
    st.subheader("Translate Summary")
    
    languages = {
        "Malayalam": "ml",
        "Hindi": "hi",
        "Tamil": "ta",
        "Telugu": "te",
        "Kannada": "kn",
        "Bengali": "bn",
        "French": "fr",
        "Arabic": "ar"
    }
    
    selected_lang = st.selectbox(
        "Select language",
        list(languages.keys())
    )
    
    if st.button("Translate"):
        with st.spinner(f"Translating to {selected_lang}..."):
            translated = translate_text(summary, languages[selected_lang])
        st.success(f"Translation ({selected_lang}):")
        st.write(translated)

    st.divider()

    # Chatbot
    st.subheader("Ask about your document")

    for human, assistant in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(human)
        with st.chat_message("assistant"):
            st.write(assistant)

    question = st.chat_input("Ask anything about your document...")

    if question:
        with st.chat_message("user"):
            st.write(question)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = ask_question(
                    st.session_state.vector_store,
                    question,
                    st.session_state.chat_history
                )
            st.write(answer)
        st.session_state.chat_history.append((question, answer))

    os.unlink(tmp_path)