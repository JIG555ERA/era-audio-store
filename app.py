import streamlit as st
import requests
import re
import tempfile
import os
import pyttsx3
import random

# --------------------------------
# Page config
# --------------------------------
st.set_page_config(
    page_title="ERA Audio-Store",
    page_icon="🎧",
    layout="wide"
)

st.markdown(
    """
    <h1 style='text-align:center;'>🎧 ERA Audio-Store</h1>
    <p style='text-align:center; font-size:18px;'>
    Discover • Listen • Enjoy classic books from our Project
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# Sidebar
st.sidebar.header("⚙️ Audio Settings")

rate = st.sidebar.slider("🗣️ Speech Rate", 100, 250, 170)
volume = st.sidebar.slider("🔊 Volume", 0.0, 1.0, 1.0)

st.sidebar.divider()
st.sidebar.markdown("### 🎲 Random Book Picker")

random_id = st.sidebar.number_input(
    "Enter a number (1–100000)",
    min_value=1,
    max_value=100000,
    step=1
)

if st.sidebar.button("🎁 Surprise Me"):
    st.session_state.book_id = str(random_id)

# Main Input
st.markdown("Choose Your Book")

book_id = st.text_input(
    "Enter Book ID",
    value=st.session_state.get("book_id", ""),
    placeholder="Example: 1342 (Pride and Prejudice)"
)

# Fetch Gutenberg TXT
@st.cache_data(show_spinner=True)
def fetch_gutenberg_text(book_id: str):
    urls = [
        f"https://www.gutenberg.org/files/{book_id}/{book_id}.txt",
        f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt",
    ]

    for url in urls:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                return r.text
        except:
            pass
    return None

# Parse Text
def parse_text(raw_text: str):
    data = {
        "title": None,
        "author": None,
        "release_date": None,
        "language": None,
        "credits": None,
        "chapters": {}
    }

    text = raw_text.replace("\r\n", "\n")

    meta_patterns = {
        "title": r"^Title:\s*(.+)$",
        "author": r"^Author:\s*(.+)$",
        "release_date": r"^Release date:\s*(.+)$",
        "language": r"^Language:\s*(.+)$",
        "credits": r"^Credits:\s*(.+)$",
    }

    for k, p in meta_patterns.items():
        m = re.search(p, text, re.IGNORECASE | re.MULTILINE)
        if m:
            data[k] = m.group(1).strip()

    start = re.search(r"\*\*\*\s*START OF .*?EBOOK.*?\*\*\*", text, re.I)
    end = re.search(r"\*\*\*\s*END OF .*?EBOOK.*?\*\*\*", text, re.I)

    if not (start and end):
        return data

    content = text[start.end():end.start()].strip()

    chapter_pattern = re.compile(
        r'^[ \t]*CHAPTER[ \t]+([IVXLCDM]+|\d+)\b.*$',
        re.IGNORECASE | re.MULTILINE
    )

    matches = list(chapter_pattern.finditer(content))

    if not matches:
        data["chapters"]["📖 Full Book"] = {"description": content}
        return data

    for i, match in enumerate(matches):
        start_idx = match.start()
        end_idx = matches[i + 1].start() if i + 1 < len(matches) else len(content)

        block = content[start_idx:end_idx].strip()
        lines = block.splitlines()

        title = lines[0].strip()
        text_body = "\n".join(lines[1:]).strip()

        text_body = re.sub(r'\n{3,}', '\n\n', text_body)
        text_body = re.sub(r'[ \t]+', ' ', text_body)

        data["chapters"][title] = {"description": text_body}

    return data

# TTS
def tts_pyttsx3_to_file(text: str, rate: int, volume: float):
    engine = pyttsx3.init()
    engine.setProperty("rate", rate)
    engine.setProperty("volume", volume)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    path = tmp.name
    tmp.close()

    engine.save_to_file(text, path)
    engine.runAndWait()
    engine.stop()

    return path

# Main Logic
if book_id:
    with st.spinner("📥 Fetching book from database..."):
        raw_text = fetch_gutenberg_text(book_id)

    if not raw_text:
        st.error("❌ Could not fetch this book. Try another number!")
    else:
        book = parse_text(raw_text)

        st.success("✅ Book Loaded Successfully!")

        st.markdown(
            f"""
            ## 📘 {book.get('title', 'Unknown Title')}
            **✍️ Author:** {book.get('author', 'Unknown')}  
            **🗓️ Release Date:** {book.get('release_date', 'Unknown')}  
            **🌐 Language:** {book.get('language', 'Unknown')}
            """
        )

        st.divider()
        st.markdown("## 📚 Chapters")

        for i, (title, ch) in enumerate(book["chapters"].items()):
            with st.expander(title, expanded=(i == 0)):
                text = ch["description"]

                st.text_area(
                    "Chapter Content",
                    value=text,
                    height=350,
                    disabled=True,
                    key=f"text_{i}"
                )

                if st.button(f"🎧 Generate Audio – {title}", key=f"audio_{i}"):
                    with st.spinner("🔊 Generating audio..."):
                        audio_path = tts_pyttsx3_to_file(text, rate, volume)
                        with open(audio_path, "rb") as f:
                            st.audio(f.read(), format="audio/wav")
                        os.remove(audio_path)
