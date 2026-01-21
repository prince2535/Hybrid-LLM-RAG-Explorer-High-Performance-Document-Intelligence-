import streamlit as st
import os
import time
from dotenv import load_dotenv

# 1. Logic: Fix the 'USER_AGENT' at the VERY TOP
os.environ["USER_AGENT"] = "MyBrowser/1.0"

# 2. Logic: Modern imports for version 1.2.6
from langchain_groq import ChatGroq
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate

# 3. Logic: USE THE CLASSIC BRIDGE (This is the fix for your error)
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain

load_dotenv()

## Load the Groq API key
groq_api_key = os.environ.get('GROQ_API_KEY')

if not groq_api_key:
    st.error("❌ GROQ_API_KEY missing in .env!")
    st.stop()

# 4. Logic: Vector Database Setup
if "vectors" not in st.session_state:
    with st.spinner("Loading technical documentation..."):
        st.session_state.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        st.session_state.loader = WebBaseLoader("https://docs.smith.langchain.com/")
        st.session_state.docs = st.session_state.loader.load()

        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs[:50])
        st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)

st.title("Stravo")

# 5. Logic: Initialize Mixtral Model
# NEW (Working):
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.3-70b-versatile")

prompt_template = ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided context only.
    <context>
    {context}
    </context>
    Question: {input}
    """
)

# 6. Logic: Create the Retrieval Pipeline
document_chain = create_stuff_documents_chain(llm, prompt_template)
retriever = st.session_state.vectors.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

user_prompt = st.text_input("Input your prompt here")

if user_prompt:
    start_time = time.process_time()
    response = retrieval_chain.invoke({"input": user_prompt})

    st.write(f"⏱️ Response time: {time.process_time() - start_time:.2f} seconds")
    st.write(response['answer'])

    with st.expander("Document Similarity Search"):
        for i, doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("--------------------------------")