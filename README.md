# 🤖 AGENTE DE CONSULTA OAB COM LLM

# 🎯 OBJETIVO

Este projeto é uma solução completa para consultar dados de advogados no Cadastro Nacional dos Advogados (CNA) da OAB e interagir com esses dados por meio de um agente de Inteligência Artificial. A aplicação combina técnicas de Web Scraping, uma API REST e um agente LLM (Large Language Model) para responder perguntas em linguagem natural.

# ✨ FUNCIONALIDADES

WEB SCRAPER COM SELENIUM: Um scraper robusto que navega pelo site da OAB, preenche o formulário de busca e extrai os dados dos resultados de forma automatizada.

API REST COM FASTAPI: Interface que expõe as capacidades do scraper através de um endpoint POST /fetch_oab, com validação rigorosa de dados (Pydantic) e tratamento de erros.

AGENTE INTELIGENTE COM LANGCHAIN: Agente que utiliza modelos da Cloudflare para interpretar intenções em português, decidir autonomamente o uso da ferramenta de busca (Function Calling) e formular respostas contextualizadas.

CONTAINERIZAÇÃO COM DOCKER: Implementação baseada em microsserviços totalmente containerizados, garantindo paridade entre ambientes de desenvolvimento e produção.

# 🛠️ TECNOLOGIAS UTILIZADAS

BACKEND: Python 3.11, FastAPI, Uvicorn

WEB SCRAPING: Selenium, Beautiful Soup

IA E LLMS: LangChain, Cloudflare Workers AI

INFRAESTRUTURA: Docker, Docker Compose

OUTROS: Python-dotenv, Requests, Pydantic

# 🚀 INSTALAÇÃO E EXECUÇÃO

Para rodar este projeto, é necessário possuir o Docker e o Docker Compose instalados.


CONFIGURE AS VARIÁVEIS DE AMBIENTE Crie um arquivo .env na raiz do projeto:

Bash

touch .env
Adicione suas credenciais da Cloudflare:

Snippet de código

CF_ACCOUNT_ID=seu_account_id_aqui
CF_API_TOKEN=seu_api_token_aqui
SUBIDA DOS CONTÊINERES

Bash

docker-compose up --build

# ⚙️ COMO USAR

AGENTE LLM: O processo é automático. Ao iniciar o contêiner llm-agent, ele processa as perguntas definidas em agent/agent.py. O log exibirá o raciocínio da "chain" até a resposta final.

API DIRETAMENTE: Você pode realizar chamadas diretas via terminal:

Bash

curl -X POST "http://localhost:8000/fetch_oab" \
-H "Content-Type: application/json" \
-d '{"name": "Lucas Augusto Capilé Pinotti", "uf": "MS"}'
🎬 DEMONSTRAÇÃO [Link para o Vídeo no Drive]

# 📁 ESTRUTURA DO PROJETO

Plaintext

.
├── AGENT/                # Lógica do agente inteligente (LangChain)

├── SCRAPER/              # Motor de busca e automação (Selenium)

├── .ENV                  # Variáveis sensíveis (não versionado)

├── DOCKER-COMPOSE.YML    # Orquestração de microsserviços

├── DOCKERFILE            # Imagem Docker da aplicação

├── MAIN.PY               # Ponto de entrada da API FastAPI

├── REQUIREMENTS.TXT      # Dependências do ecossistema Python

└── README.MD             # Documentação técnica

# 🎬 Demonstração
https://github.com/user-attachments/assets/c5ca5c45-264e-4b7c-bf76-8b2771650e97



Desenvolvido por George Emannuel Guedes de Carvalho
