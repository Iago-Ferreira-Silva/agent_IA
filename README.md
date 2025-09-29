<h1 align="center">🤖 Assistente Virtual</h1>

<p align="center">
  Um <strong>chatbot multimodelo</strong> desenvolvido em <code>Python</code> com <code>Streamlit</code> e <code>LangChain</code>, que permite conversar com diferentes LLMs (OpenAI, HuggingFace e Ollama).<br/>
  Ideal para estudos, prototipagem e integração de modelos de linguagem em aplicações reais.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white"/>
  <img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white"/>
  <img src="https://img.shields.io/badge/HuggingFace-FCC624?style=for-the-badge&logo=huggingface&logoColor=black"/>
  <img src="https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white"/>
</p>

***

## ✨ FUNCIONALIDADES:

- 💬 Interface de chat em tempo real com **Streamlit**.  
- 🔄 Suporte a múltiplos backends de LLM (OpenAI, HuggingFace, Ollama).  
- ⚡ Respostas em **streaming** (quando suportado).  
- 📝 Histórico de conversa persistente durante a sessão.  
- 🎛️ Configuração de **temperatura** e **máximo de tokens** via interface.  
- 🌍 Respostas em português (ou no idioma configurado).  

***

## 📁 ESTRUTURA DE PASTAS:

```bash
agent_IA/
├── main.py
├── requirements.txt
├── .env
├── .gitignore
│
└── README.md

```

***

## 🛠️ TECNOLOGIAS UTILIZADAS:

- `Python`: Linguagem principal do projeto.
- `Streamlit`: Framework para criação da interface web.
- `LangChain`: Orquestração de prompts e integração com LLMs.
- `OpenAI API`: Modelos GPT (opcional).
- `Hugging Face Hub`: Modelos como Llama 3, Mistral, Falcon, Gemma.
- `Ollama`: Execução de modelos localmente.
- `dotenv`: Gerenciamento de variáveis de ambiente.
- `Torch`: Backend necessário para alguns modelos HuggingFace.

***

## 🚧 DIFICULDADES ENCONTRADAS:

- ⚠️ Limite de créditos na API da OpenAI.
- 🔄 Diferenças entre modelos que suportam streaming e os que não suportam.
- 🧩 Ajuste de prompts para compatibilidade entre backends diferentes.
- 🛠️ Tratamento de erros de API e mensagens amigáveis ao usuário.

***

## 🚀 COMO RODAR O PROJETO LOCALMENTE:

### 1. Clone o repositório:

```bash
git clone https://github.com/Iago-Ferreira-Silva/agent_IA.git
```
### 2. Acesse o diretório do projeto:

```bash
cd agent_IA
```
### 3. Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 4. Instale as dependências:

```bash
pip install -r requirements.txt
```
### 5. Configure suas chaves no arquivo .env:

```bash
OPENAI_API_KEY=your_openai_api_key
HUGGINGFACEHUB_API_TOKEN=your_hf_token
```

### 6. Execute a aplicação:

```bash
streamlit run main.py
```

### 7. Acesse no navegador:

```bash
http://localhost:8501
```

***

## 📌 STATUS DO PROJETO:
![Badge Concluído](https://img.shields.io/static/v1?label=STATUS&message=CONCLU%C3%8DDO&color=brightgreen&style=for-the-badge)

***
