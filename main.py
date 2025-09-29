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

# ==============================
# Sidebar de Configuração
# ==============================
st.sidebar.header("⚙️ Configurações")

model_class = st.sidebar.selectbox(
    "Escolha o modelo:",
    ["openai", "hf_hub", "ollama"],
    index=1
)

temperature = st.sidebar.slider("Temperatura", 0.0, 1.0, 0.1, 0.05)
max_tokens = st.sidebar.slider("Máx. tokens", 128, 2048, 512, 64)

# ==============================
# Funções de carregamento dos modelos
# ==============================
def model_hf_hub(model="meta-llama/Meta-Llama-3-8B-Instruct", temperature=0.1, max_tokens=512):
    endpoint = HuggingFaceEndpoint(
        repo_id=model,
        temperature=temperature,
        max_new_tokens=max_tokens
    )
    return ChatHuggingFace(llm=endpoint)

def model_openai(model="gpt-4o-mini", temperature=0.1, max_tokens=512):
    return ChatOpenAI(model=model, temperature=temperature, max_tokens=max_tokens)

def model_ollama(model="phi3", temperature=0.1, max_tokens=512):
    return ChatOllama(model=model, temperature=temperature)

# ==============================
# Função de resposta
# ==============================
def model_response(user_query, chat_history, model_class, temperature, max_tokens):
    if model_class == "hf_hub":
        llm = model_hf_hub(temperature=temperature, max_tokens=max_tokens)
        supports_stream = False
    elif model_class == "openai":
        llm = model_openai(temperature=temperature, max_tokens=max_tokens)
        supports_stream = True
    elif model_class == "ollama":
        llm = model_ollama(temperature=temperature, max_tokens=max_tokens)
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

# ==============================
# Histórico de conversa
# ==============================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [AIMessage(content="Olá, sou o seu assistente virtual! Como posso ajudar você?")]

# Exibir histórico
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

# ==============================
# Entrada do usuário
# ==============================
user_query = st.chat_input("Digite sua mensagem aqui...")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        try:
            resp = model_response(user_query, st.session_state.chat_history, model_class, temperature, max_tokens)

            if hasattr(resp, "__iter__") and not isinstance(resp, str):
                # Streaming: acumula os chunks
                collected = ""
                placeholder = st.empty()
                for chunk in resp:
                    collected += chunk
                    placeholder.markdown(collected)
                final_resp = collected
            else:
                # Resposta direta
                final_resp = resp
                st.write(final_resp)

        except Exception as e:
            final_resp = f"⚠️ Ocorreu um erro: {e}"
            st.error(final_resp)

    # Garante que sempre seja string
    st.session_state.chat_history.append(AIMessage(content=str(final_resp)))