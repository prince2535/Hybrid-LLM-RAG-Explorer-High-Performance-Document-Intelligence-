from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langserve import add_routes
import uvicorn
import os
from langchain_community.llms import Ollama
from dotenv import load_dotenv

load_dotenv()

# Logic: Ensure your .env has HUGGINGFACEHUB_API_TOKEN
os.environ['HUGGINGFACEHUB_API_TOKEN'] = os.getenv("HUGGINGFACEHUB_API_TOKEN")

app = FastAPI(title="Langchain Server", version="1.0")



# 1. Ollama Model (Local)
ollama_llm = Ollama(model="llama2")

# --- PROMPTS ---
prompt_essay = ChatPromptTemplate.from_template("Write an essay about {topic} in 100 words")
prompt_poem = ChatPromptTemplate.from_template("Write a poem for a 5-year-old child about {topic}")

# --- ROUTES ---
add_routes(app, prompt_essay | ollama_llm, path="/essay")
add_routes(app, prompt_poem | ollama_llm, path="/poem")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)