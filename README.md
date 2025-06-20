
# 📘  Study-Buddy-Ask-Questions-on-Your-Notes

**Study Buddy** is a smart tool that helps you study better.  
You can upload your PDF notes, ask questions about them, and get instant answers — even **without an internet connection**.

It uses local AI models like **LLaMA3** (via Ollama), so everything stays **private** and on your computer.

---

## ✨ What Can It Do?

- 📄 Upload PDF notes
- 🤖 Ask questions in natural language (like "What is machine learning?")
- 🧠 Uses local AI (no API key or internet needed)
- 🔍 Finds the right info from your notes using smart search (FAISS + embeddings)
- 🔐 100% offline – your notes and questions are not sent anywhere

---

## 🧠 How It Works

1. You upload a PDF file (e.g., your class notes).
2. The app splits it into small parts and understands the meaning using **Sentence Transformers**.
3. It builds a smart search index using **FAISS**.
4. When you ask a question, it searches your notes and sends the relevant info to **Ollama** (LLaMA3 model).
5. You get a direct and useful answer.

---

## 📦 Built With

| Tool | Use |
|------|-----|
| [Streamlit](https://streamlit.io/) | For creating the web app |
| [Ollama](https://ollama.com/) | To run AI models locally |
| Sentence Transformers (`all-MiniLM-L6-v2`) | To understand text |
| FAISS | To search similar chunks of text |
| PyMuPDF (fitz) | To read text from PDF files |

---

## 💻 How to Run the App (Step-by-Step)

### ✅ 1. Install Python

Make sure you have Python 3.8 or newer.  
You can download it from [https://www.python.org/downloads/](https://www.python.org/downloads/)

---

### ✅ 2. Install Ollama

Download and install Ollama:  
🔗 [https://ollama.com/download](https://ollama.com/download)

---

### ✅ 3. Download the AI Model

Open your terminal or command prompt and run:

```bash
ollama pull llama3
