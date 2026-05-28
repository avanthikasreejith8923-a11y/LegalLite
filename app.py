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
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600&family=Inter:wght@300;400;500&display=swap');

.stApp {
    background-color: #FFFFFF;
    font-family: 'Inter', sans-serif;
}

.header {
    background-color: #000000;
    padding: 32px 40px;
    text-align: center;
    margin-bottom: 0px;
}

.logo-text {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3rem;
    font-weight: 600;
    color: #FFFFFF;
    letter-spacing: 0.3em;
}

.logo-sub {
    font-size: 0.65rem;
    color: #888888;
    letter-spacing: 0.3em;
    margin-top: 4px;
}

.flashcard-section {
    background-color: #F2F2F2;
    padding: 14px 40px;
    text-align: center;
    border-bottom: 1px solid #DDDDDD;
    margin-bottom: 40px;
}

.flashcard-text {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.1rem;
    color: #444444;
    font-style: italic;
    letter-spacing: 0.03em;
}

.section-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.3rem;
    font-weight: 600;
    color: #000000;
    margin-bottom: 12px;
    letter-spacing: 0.05em;
    border-bottom: 1px solid #000000;
    padding-bottom: 6px;
}

.card {
    background-color: #FAFAFA;
    border-radius: 6px;
    padding: 20px 24px;
    border: 1px solid #E8E8E8;
    margin-bottom: 16px;
    color: #222222;
    line-height: 1.8;
    font-size: 14px;
}

.risk-card {
    background-color: #FAFAFA;
    border-radius: 6px;
    padding: 20px 24px;
    border: 1px solid #E8E8E8;
    border-left: 3px solid #000000;
    margin-bottom: 16px;
    color: #222222;
    line-height: 1.8;
    font-size: 14px;
}

.stButton button {
    background-color: #000000 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 10px 24px !important;
    font-size: 12px !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: 0.1em !important;
    width: 100% !important;
}

.stButton button:hover {
    background-color: #222222 !important;
}

.stSelectbox > div > div {
    background-color: #FFFFFF !important;
    border: 1px solid #CCCCCC !important;
    border-radius: 4px !important;
    color: #222222 !important;
    font-size: 13px !important;
}

[data-testid="stFileUploader"] {
    background-color: #FAFAFA;
    border-radius: 6px;
    border: 1.5px dashed #AAAAAA;
    padding: 12px;
}

[data-testid="stChatInput"] {
    border: 1px solid #000000 !important;
    border-radius: 6px !important;
}

[data-testid="stChatMessage"] {
    background-color: #FAFAFA;
    border: 1px solid #EEEEEE;
    border-radius: 6px;
}

.stSuccess > div {
    background-color: #F5F5F5 !important;
    color: #000000 !important;
    border: 1px solid #DDDDDD !important;
    border-radius: 4px !important;
}

.divider {
    border: none;
    border-top: 1px solid #EEEEEE;
    margin: 32px 0;
}

.footer {
    background-color: #000000;
    color: #777777;
    text-align: center;
    padding: 18px;
    font-size: 11px;
    margin-top: 60px;
    letter-spacing: 0.1em;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

p, li, span { color: #222222; }
h1, h2, h3 { color: #000000; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <div class="logo-text">LEGALLITE</div>
    <div class="logo-sub">AI LEGAL DOCUMENT ASSISTANT</div>
</div>
""", unsafe_allow_html=True)

# Flashcards
slogans = [
    "Upload any contract. Understand it instantly.",
    "Speaks your language — Malayalam, Hindi, Tamil and more.",
    "Ask anything about your document.",
    "Your AI legal companion. Always honest. Never a lawyer.",
    "Know what you are signing before you sign it."
]

if "slogan_index" not in st.session_state:
    st.session_state.slogan_index = 0

st.markdown(f"""
<div class="flashcard-section">
    <div class="flashcard-text">{slogans[st.session_state.slogan_index]}</div>
</div>
""", unsafe_allow_html=True)

st.session_state.slogan_index = (st.session_state.slogan_index + 1) % len(slogans)

# Upload section
st.markdown('<div class="section-title">Upload Your Document</div>',
            unsafe_allow_html=True)
st.caption("Supports PDF, JPG and PNG — rental agreements, contracts, notices, offer letters")

uploaded_file = st.file_uploader(
    "",
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
        with st.spinner("Preparing document analysis..."):
            st.session_state.vector_store = create_vector_store(text)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "summary" not in st.session_state:
        with st.spinner("Analyzing document..."):
            st.session_state.summary = summarize_document(text)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # Summary and Risk
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-title">Plain English Summary</div>',
                    unsafe_allow_html=True)
        st.markdown(f'<div class="card">{st.session_state.summary}</div>',
                    unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-title">Risk Flags</div>',
                    unsafe_allow_html=True)
        with st.spinner("Detecting risks..."):
            risks = detect_risks(text)
        st.markdown(f'<div class="risk-card">{risks}</div>',
                    unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # Voice
    st.markdown('<div class="section-title">Listen to Summary</div>',
                unsafe_allow_html=True)

    col_v1, col_v2, col_v3 = st.columns([1, 1, 2])
    with col_v1:
        voice_languages = {
            "English": "en",
            "Malayalam": "ml",
            "Hindi": "hi",
            "Tamil": "ta"
        }
        selected_voice_lang = st.selectbox(
            "Voice language",
            list(voice_languages.keys()),
            key="voice_lang"
        )
    with col_v2:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        if st.button("Generate Audio"):
            with st.spinner("Generating audio..."):
                lang_code = voice_languages[selected_voice_lang]
                audio_text = st.session_state.summary
                if selected_voice_lang != "English":
                    audio_text = translate_text(audio_text, lang_code)
                text_to_speech(audio_text, lang_code, "summary_audio.mp3")
            st.audio("summary_audio.mp3")

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # Translation
    st.markdown('<div class="section-title">Translate Summary</div>',
                unsafe_allow_html=True)

    col_t1, col_t2, col_t3 = st.columns([1, 1, 2])
    with col_t1:
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
    with col_t2:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        translate_clicked = st.button("Translate")

    if translate_clicked:
        with st.spinner("Translating..."):
            translated = translate_text(
                st.session_state.summary,
                languages[selected_lang]
            )
        st.markdown(f'<div class="card">{translated}</div>',
                    unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # Chatbot
    st.markdown('<div class="section-title">Ask About Your Document</div>',
                unsafe_allow_html=True)
    st.caption("Ask anything — the AI answers only from your document.")

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

# Footer
st.markdown("""
<div class="footer">
    2025 LEGALLITE &nbsp;|&nbsp; FOR EDUCATIONAL PURPOSES ONLY &nbsp;|&nbsp;
    NOT LEGAL ADVICE &nbsp;|&nbsp; ALWAYS CONSULT A QUALIFIED LAWYER
</div>
""", unsafe_allow_html=True)