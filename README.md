# Hybrid-LLM RAG Explorer 🚀

A high-performance Retrieval-Augmented Generation (RAG) system built to compare and leverage multiple LLM providers. This project demonstrates a modular architecture that can switch between cloud-based inference (Groq/OpenAI) and local privacy-focused models (Ollama/Hugging Face).



## 🧠 The Engineering Logic: Why these tools?

Unlike standard tutorials, this project was built with specific performance trade-offs:

* **Groq (Llama 3.3-70B):** Chosen for **Ultra-low latency inference**. It provides near-instant responses for real-time applications.
* **Ollama (nomic-embed-text):** Used for **Local Embeddings**. This ensures that document vectors are generated on-device, reducing API costs and increasing privacy.
* **FAISS (Facebook AI Similarity Search):** Selected for **Local Vector Storage** due to its high-speed similarity search capabilities without the need for a cloud database subscription.
* **LangChain 1.2.6 (Modular Path):** I implemented the modern decoupled version of LangChain, utilizing `langchain-classic` bridges to maintain stability while using the latest security features.

---

## 🛠️ System Architecture

1.  **Ingestion:** Scrapes web docs (via WebBaseLoader) or parses PDFs (via PyPDF).
2.  **Chunking:** Uses `RecursiveCharacterTextSplitter` to maintain semantic context.
3.  **Vectorization:** Local embedding via Ollama or HuggingFace BGE models.
4.  **Retrieval:** FAISS similarity search identifies the top-K relevant document chunks.
5.  **Generation:** Context-aware response generation via the selected LLM (Groq/OpenAI/Mistral).

---

## 🚀 Key Features

* **Multi-Model Support:** Seamlessly switch between OpenAI, Groq, Ollama, and Hugging Face Hub.
* **Dynamic Context Injection:** A custom ReAct agent logic (Thought -> Action -> Observation) that allows the AI to decide when to search the database.
* **Modern Streamlit UI:** A clean interface for real-time querying with response-time tracking.
