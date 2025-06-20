import streamlit as st
import fitz  # PyMuPDF
import numpy as np
import faiss
import requests
from sentence_transformers import SentenceTransformer

# ---- SETUP ----
st.set_page_config(page_title="Study Buddy", page_icon="📘", layout="wide")
MODEL_NAME = "llama3"
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# ---- SIDEBAR NAVIGATION ----
st.sidebar.title("📚 Study Buddy")
page = st.sidebar.radio("", ["Home", "Ask Questions", "About"])

# ---- PAGE: HOME ----

if page == "Home":
    st.title("🏠 Home")
    st.markdown("""
    ## Welcome to **Study Buddy** – Your Personal Offline AI Study Assistant 📚

    **Study Buddy** is a smart, privacy-first assistant designed to help you better understand your study material.  
    With this tool, you can:

    - 📄 **Upload PDF notes** and ask questions directly about their content.
    - 🧠 Get **contextual answers** powered by local Large Language Models (LLMs) using **Ollama (Mistral)** – no internet or API key required.
    - 🔍 Uses **semantic search (FAISS + embeddings)** to extract the most relevant parts of your documents.
    - 🛡️ **Runs entirely offline** for full data privacy – your documents and questions never leave your machine.

    Whether you're preparing for exams, revising notes, or reviewing complex topics,  
    **Study Buddy** is here to support your learning journey — fast, reliable, and secure.
    """)


# ---- PAGE: ASK QUESTIONS ----
elif page == "Ask Questions":
    st.title("❓ Ask Questions from Notes")

    if "processed" not in st.session_state:
        st.session_state.processed = False
    if "chunks" not in st.session_state:
        st.session_state.chunks = []
    if "index" not in st.session_state:
        st.session_state.index = None

    uploaded_file = st.file_uploader("📤 Upload your PDF notes", type="pdf")

    if uploaded_file:
        if st.button("📄 Process PDF"):
            try:
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                text = "".join([page.get_text() for page in doc])

                # Split & embed
                chunks = [text[i:i+500] for i in range(0, len(text), 500)]
                embeddings = embedder.encode(chunks)
                index = faiss.IndexFlatL2(embeddings.shape[1])
                index.add(np.array(embeddings))

                # Store in session
                st.session_state.chunks = chunks
                st.session_state.index = index
                st.session_state.processed = True
                st.success("✅ PDF processed successfully!")
            except Exception as e:
                st.error(f"❌ Error processing PDF: {e}")

    if st.session_state.processed:
        query = st.text_input("🔎 Ask something about your notes:")
        if st.button("💬 Get Answer"):
            if query.strip() == "":
                st.warning("Please enter a question.")
            else:
                st.info("Searching notes...")
                q_embed = embedder.encode([query])
                _, I = st.session_state.index.search(np.array(q_embed), k=3)
                context = "\n\n".join([st.session_state.chunks[i] for i in I[0]])

                prompt = f"Use the following notes to answer:\n\n{context}\n\nQuestion: {query}\nAnswer:"

                with st.spinner("Thinking with Ollama..."):
                    try:
                        res = requests.post(
                            "http://localhost:11434/api/generate",
                            json={"model": MODEL_NAME, "prompt": prompt, "stream": False}
                        )
                        if res.status_code == 200:
                            answer = res.json()["response"]
                            st.success("📘 Answer:")
                            st.markdown(f"> {answer.strip()}")
                        else:
                            st.error("Ollama API Error. Check if the model is running.")
                    except requests.exceptions.ConnectionError:
                        st.error("⚠️ Ollama is not running. Please start it using:\n\n`ollama run llama3`")


# ---- PAGE: ABOUT ----
if page == "About":
    st.title("ℹ️ About")
    st.markdown("""
    ## About Study Buddy 🤖

    **Study Buddy** is a local AI-powered assistant designed to help students interact intelligently with their study materials.  
    It allows users to upload **PDF** files and ask questions directly from their content using a local **LLM (via Ollama)**.  
    The system uses a **RAG (Retrieval-Augmented Generation)** approach for accurate, context-aware answers — all offline and private.

    ### 🔧 Key Technologies:
    - **Ollama (Mistral)** – lightweight local LLM engine.
    - **FAISS** – fast and efficient vector similarity search.
    - **Sentence-transformers** – semantic embeddings for meaningful context.
    - **Flask** – backend logic to manage document parsing and LLM interaction.

    ### 🎯 Features:
    - 100% offline, no external API calls — ideal for privacy-focused environments.
    - Ask questions directly from your study notes with reliable, AI-generated answers.
    - Easily upload, process, and search your documents.

    ---

    ### 👨‍💻 Developer:
    **Himanshu Yadav**  
    MCA Student | AI/ML Enthusiast | [GitHub](https://github.com/Himans30)

    
    ### 🚀 Future Plans:
    - Add multi-language support for diverse learners.
    - Extend file types (e.g., PPT, TXT).
    - Integrate chat memory across sessions.
    - Include voice-based Q&A.

    Thank you for using Study Buddy 🙌  
    Let's make learning smarter, not harder.
    """)

