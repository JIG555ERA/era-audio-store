# 🎧 ERA Audio-Store  
### *Turn Classic Books into Immersive Audio Experiences*

ERA Audio-Store is an interactive **Streamlit web app** that lets users **discover, read, and listen** to classic books from **Project Gutenberg**.  
Pick a book manually — or let fate decide with a **random book generator** 🎲 — and enjoy high-quality **text-to-speech audio** chapter by chapter.

---

## 🌟 Features

- 📚 **Book Discovery**
  - Fetch any Project Gutenberg book using its ID
  - 🎲 Random Book Picker (1–100000) for a surprise read
- 🧠 **Smart Parsing**
  - Extracts Title, Author, Release Date, Language, Credits
  - Chapter-wise segmentation
- 🎧 **Audio Experience**
  - Convert chapters to WAV audio
  - Adjustable speech rate & volume
  - Instant playback inside the app
- 🎨 **Clean & Fun UI**
  - Card-based layout
  - Expandable chapters
  - Sidebar audio controls
  - Smooth loading spinners & status messages

---

## 🛠️ Installation & Running Instructions

### Prerequisites
- **Python 3.8+**
- **pip**
- Internet connection (for fetching books)

Check Python version:
```bash
python --version

git clone https://github.com/JIG555ERA/era-audio-store.git
cd era-audio-store

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

streamlit run app.py



