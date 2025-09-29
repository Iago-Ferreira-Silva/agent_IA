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

# Função de resposta
def model_response(user_query, chat_history, model_class):
    if model_class == "hf_hub":
        llm = model_hf_hub()
        supports_stream = False
    elif model_class == "openai":
        llm = model_openai()
        supports_stream = True
    elif model_class == "ollama":
        llm = model_ollama()
        supports_stream = True

    system_prompt = """
        Você é um assistente prestativo e está respondendo perguntas gerais. Responda em {language}.
    """
    language = "português"

    if model_class.startswith("hf"):
        user_prompt = "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n{input}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
    else:
        user_prompt = "{input}"

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", user_prompt)
    ])

    chain = prompt_template | llm | StrOutputParser()

    if supports_stream:
        return chain.stream({
            "chat_history": chat_history,
            "input": user_query,
            "language": language
        })
    else:
        return chain.invoke({
            "chat_history": chat_history,
            "input": user_query,
            "language": language
        })
    
# Histórico de conversa
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [AIMessage(content="Olá, sou o seu assistente virtual! Como posso ajudar você?")]

# Entrada do usuário
user_query = st.chat_input("Digite sua mensagem aqui...")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        resp = model_response(user_query, st.session_state.chat_history, model_class)

        if hasattr(resp, "__iter__") and not isinstance(resp, str):
            # Streaming: acumula os chunks
            collected = ""
            for chunk in resp:
                collected += chunk
                st.write(chunk)
            final_resp = collected
        else:
            # Resposta direta
            final_resp = resp
            st.write(final_resp)

    # Garante que sempre seja string
    st.session_state.chat_history.append(AIMessage(content=str(final_resp)))