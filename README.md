# TalkToPDF 🎤📖🤖🔊

**TalkToPDF** is an AI-powered application that lets you **talk to your PDFs**.  
Just ask a question with your voice, and the system will:  
1. Convert your speech into text,  
2. Retrieve answers from the document using RAG (Retrieval-Augmented Generation),  
3. Generate a response with an LLM, and  
4. Speak the answer back to you.  

---

## 🚀 How It Works

1. **🎤 Voice Input** – Speak your question into the microphone.  
   - Example: *“What are the key points of this research paper?”*  

2. **📝 Speech-to-Text (Whisper)** –  
   - OpenAI’s **Whisper** model transcribes your voice into text.  

3. **📖 Context Retrieval (RAG)** –  
   - The transcribed text is passed to a **RAG pipeline**.  
   - Relevant passages from the PDF are retrieved as context.  

4. **🤖 Answer Generation (LLM)** –  
   - An **LLM (e.g., GPT)** uses your query + context to generate an answer.  

5. **🔊 Text-to-Speech (OpenAI TTS)** –  
   - The answer is converted back to **natural speech** using OpenAI’s TTS.  

6. **🎧 Voice Output** –  
   - You hear the answer spoken back to you.  

---

## 🏗️ System Architecture

```
🎤 Voice Input
      |
      v
📝 Whisper (Speech-to-Text)
      |
      v
📖 RAG (PDF Search & Retrieval)
      |
      v
🤖 LLM (Answer Generation)
      |
      v
🔊 TTS (Text-to-Speech)
      |
      v
🎧 Voice Output
```

---

## 🔍 Technologies Used

- **Whisper (OpenAI)** – Converts voice into text  
- **RAG (Retrieval-Augmented Generation)** – Searches PDF documents  
- **LLM (OpenAI GPT models)** – Generates human-like responses  
- **TTS (OpenAI)** – Converts text to natural-sounding speech  
- **Python / Streamlit** – Backend & user interface  

---

## 💡 Key Features

- **Hands-Free Research** → Ask questions without manually reading PDFs  
- **Accessibility** → Great for users who prefer listening over reading  
- **Productivity** → Speeds up knowledge extraction  
- **Education & Research** → Summarize and query complex material instantly  

---

## 🌍 Use Cases

- **Students** → Summarize textbooks & research papers  
- **Professionals** → Extract key points from reports  
- **Researchers** → Quickly navigate dense academic material  
- **General Users** → Turn any PDF into an interactive assistant  

---

## 📌 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/prashanth-gajula/TalkToPDF.git
cd TalkToPDF
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app.py
```

---

## 📌 Conclusion

**TalkToPDF** turns static PDFs into **interactive, conversational experiences**.  
With Whisper, RAG, LLMs, and TTS, you don’t just read documents—you **talk to them**.  
