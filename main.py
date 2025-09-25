import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace

from dotenv import load_dotenv

load_dotenv()

# Configurações do Streamlit
st.set_page_config(page_title="Seu assistente virtual 🤖", page_icon="🤖")
st.title("Seu assistente virtual 🤖")

# Escolha do modelo
model_class = "hf_hub"  # "hf_hub", "openai", "ollama"

# Funções de carregamento dos modelos
def model_hf_hub(model="meta-llama/Meta-Llama-3-8B-Instruct", temperature=0.1):
    endpoint = HuggingFaceEndpoint(
        repo_id=model,
        temperature=temperature,
        max_new_tokens=512
    )
    return ChatHuggingFace(llm=endpoint)

def model_openai(model="gpt-4o-mini", temperature=0.1):
    return ChatOpenAI(model=model, temperature=temperature)

def model_ollama(model="phi3", temperature=0.1):
    return ChatOllama(model=model, temperature=temperature)