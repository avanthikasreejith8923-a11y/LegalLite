import streamlit as st
from core.extractor import extract_text
from core.summarizer import summarize_document, detect_risks
from core.rag import create_vector_store, ask_question
from core.translator import translate_text
from core.voice import text_to_speech
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

    if "summary" not in st.session_state:
        with st.spinner("Summarizing..."):
            st.session_state.summary = summarize_document(text)

    # Summary and Risk
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Plain English Summary")
        st.write(st.session_state.summary)

    with col2:
        st.subheader("Risk Flags")
        with st.spinner("Detecting risks..."):
            risks = detect_risks(text)
        st.warning(risks)

    st.divider()

    # Voice section
    st.subheader("Listen to Summary")

    voice_languages = {
        "English": "en",
        "Malayalam": "ml",
        "Hindi": "hi",
        "Tamil": "ta"
    }

    selected_voice_lang = st.selectbox(
        "Select voice language",
        list(voice_languages.keys()),
        key="voice_lang"
    )

    if st.button("Generate Audio"):
        with st.spinner("Generating audio..."):
            if selected_voice_lang == "English":
                audio_text = st.session_state.summary
                lang_code = "en"
            else:
                lang_code = voice_languages[selected_voice_lang]
                audio_text = translate_text(
                    st.session_state.summary,
                    lang_code
                )

            audio_file = text_to_speech(
                audio_text,
                lang_code,
                "summary_audio.mp3"
            )

        st.audio("summary_audio.mp3")
        st.success("Audio ready. Press play above.")

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
        list(languages.keys()),
        key="translate_lang"
    )

    if st.button("Translate"):
        with st.spinner(f"Translating to {selected_lang}..."):
            translated = translate_text(
                st.session_state.summary,
                languages[selected_lang]
            )
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