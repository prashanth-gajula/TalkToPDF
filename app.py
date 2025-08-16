import streamlit as st
import tempfile
import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from rag import create_vector_store
from greetings import speak_greeting,tts_synthesize
from whisper import transcribe_audio
from CallingLlm import calling_llm

if "index_id" not in st.session_state:
    st.session_state.index_id = None
if "kb_ready" not in st.session_state:
    st.session_state.kb_ready = False
if "greet_done" not in st.session_state:
    st.session_state.greet_done = False
if "greet_text" not in st.session_state:
    st.session_state.greet_text = None
if "greet_audio" not in st.session_state:
    st.session_state.greet_audio = None
if "audio_play" not in st.session_state:
    st.session_state.audio_play = None
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "transcript" not in st.session_state:
    st.session_state.transcript = None
if "audio_input_complete" not in st.session_state:
    st.session_state.audio_input_complete = None
if "answer_generated" not in st.session_state:
    st.session_state.answer_generated = None
# utils_audio.py
import base64
from streamlit.components.v1 import html

def autoplay_audio(audio_bytes: bytes, mime: str = "audio/mp3"):
    b64 = base64.b64encode(audio_bytes).decode()
    src = f"data:{mime};base64,{b64}"
    html(
        f"""
        <audio autoplay>
        <source src="{src}" type="{mime}">
        </audio>
        """,
        height=0,
    )
    
def load_and_process_documents(uploaded_files) -> List:
    """Load and process uploaded documents"""
    documents = []
    
    for uploaded_file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        try:
            if uploaded_file.name.endswith('.pdf'):
                loader = PyPDFLoader(tmp_file_path)
            else:
                loader = TextLoader(tmp_file_path)
            
            docs = loader.load()
            documents.extend(docs)
        except Exception as e:
            st.error(f"Error loading {uploaded_file.name}: {str(e)}")
        finally:
            os.unlink(tmp_file_path)
    
    return documents

def main():
    st.title("🤖 TalkToPdf")
    st.markdown("Upload documents and to talk to your Documents through OpenAI models!")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        st.header("Upload Documents")
        uploaded_files = st.file_uploader(
            "Choose files",
            accept_multiple_files=True,
            type=['pdf']
        )
        
        if uploaded_files and st.button("Upload Documents"):
            with st.spinner("Processing documents..."):
                try:
                    documents = load_and_process_documents(uploaded_files)
                    
                    if documents:
                        st.session_state.vector_store = create_vector_store(documents)
                        st.success(f"Processed {len(documents)} documents!")
                        st.session_state.kb_ready = True
                        st.session_state.greet_done = False
                    else:
                        st.error("No documents could be processed.")
                except Exception as e:
                    st.error(f"Error processing documents: {str(e)}")
    if st.session_state.kb_ready and not st.session_state.greet_done:
        # Generate only once, then cache in session so it won't re-run every rerun
        text, audio_bytes = speak_greeting()
        st.session_state.greet_text = text
        st.session_state.greet_audio = audio_bytes
        st.session_state.greet_done = True
        # (Optional) If you need UI to update immediately after flags change:
        # st.rerun()

    # ---------- render greeting ----------
    if st.session_state.greet_done and st.session_state.greet_text:
        st.info(st.session_state.greet_text)
        if st.session_state.greet_audio:
            autoplay_audio(st.session_state.greet_audio, mime="audio/mp3")
            st.session_state.audio_play = True

    #taking the input from the user
    if st.session_state.get("greet_done"):
        st.subheader("Speak to your PDF 🎙️")
        audio_in = st.audio_input("Hold to record or click to start/stop")
        if audio_in is not None and st.session_state.get("kb_ready"):
            # 1) Get raw audio bytes
            wav_bytes = audio_in.getvalue()
            st.session_state.transcript = transcribe_audio(wav_bytes)
            st.session_state.audio_input_complete = True
            #print(transcript)
            #st.markdown(f"**You:** {transcript}")
    #passing the input to the llm to refer the rag before answering the question
    if st.session_state.audio_input_complete:
        answer = calling_llm(st.session_state.vector_store,st.session_state.transcript)
        #print(answer)
        #st.markdown(f"**You:** {answer}")
        st.session_state.answer_generated = True
    if st.session_state.answer_generated:
        audio_bytes = tts_synthesize(answer)
        autoplay_audio(audio_bytes, mime="audio/mp3")


if __name__ == "__main__":
    main()