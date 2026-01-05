# Agente de Consulta OAB com LLM

## 🎯 Objetivo

Este projeto é uma solução completa para consultar dados de advogados no Cadastro Nacional dos Advogados (CNA) da OAB e interagir com esses dados por meio de um agente de Inteligência Artificial. A aplicação combina técnicas de Web Scraping, uma API REST e um agente LLM (Large Language Model) para responder perguntas em linguagem natural.

## ✨ Funcionalidades

*  **Web Scraper com Selenium:** Um scraper robusto que navega pelo site da OAB, preenche o formulário de busca e extrai os dados dos resultados.
*  **API REST com FastAPI:** Uma API que expõe os dados do scraper através de um endpoint `POST /fetch_oab`, com validação de dados e tratamento de erros.
*  **Agente Inteligente com LangChain:** Um agente LLM que utiliza modelos da Cloudflare para interpretar perguntas em português, decidir quando usar a ferramenta de busca e formular respostas claras para o usuário.
*  **Containerização com Docker:** A aplicação é totalmente containerizada, garantindo um ambiente de execução consistente e facilitando a instalação.

## 🛠️ Tecnologias Utilizadas

*  **Backend:** Python 3.11, FastAPI, Uvicorn  
*  **Web Scraping:** Selenium, Beautiful Soup  
*  **IA e LLMs:** LangChain, LangChain Cloudflare  
* **Containerização:** Docker, Docker Compose
*  **Outros:** python-dotenv, requests  

## 🚀 Instalação e Execução

Para rodar este projeto localmente, você precisará ter o Docker e o Docker Compose instalados.

### 1. Clone o Repositório

```bash
git clone [https://github.com/bax7os/alfaneo-test](https://github.com/bax7os/alfaneo-test)
cd teste-alfenio-legal-ai
```

### 2. Configure as Variáveis de Ambiente

Este projeto precisa de credenciais para acessar a API de IA da Cloudflare. Crie um arquivo chamado `.env` na raiz do projeto.

```bash
touch .env
```

Abra o arquivo `.env` e adicione seu Account ID e seu API Token da Cloudflare, como no exemplo abaixo:

```env
# Arquivo .env
CF_ACCOUNT_ID=seu_account_id_aqui
CF_API_TOKEN=seu_api_token_aqui
```

  * **`CF_ACCOUNT_ID`**: Pode ser encontrado na página inicial do seu dashboard Cloudflare.
  * **`CF_API_TOKEN`**: Deve ser criado em "My Profile" \> "API Tokens" com a permissão `Workers AI (Read)`.

### 3. Suba os Contêineres

 Com o Docker em execução, utilize o Docker Compose para construir as imagens e iniciar os serviços:

```bash
docker-compose up --build
```

Os serviços serão iniciados, e o agente começará a processar as perguntas no log do terminal.

## ⚙️ Como Usar

A aplicação foi desenhada para ser interativa através do agente e também para permitir consultas diretas à API.

### Usando o Agente LLM

 O agente é executado automaticamente ao iniciar o contêiner `llm-agent` . Ele processará as perguntas definidas no final do arquivo `agent/agent.py`. Você verá a cadeia de pensamentos ("chain") e a resposta final no log do seu terminal.

 **Exemplos de perguntas processadas :**

1.  `Qual o número da OAB e a categoria de Lucas Augusto Capilé Pinotti no Mato Grosso do Sul (MS)?` (usa a ferramenta)
2.  `Qual a previsão do tempo para hoje em Corumbá?` (não usa a ferramenta e responde que não sabe)

### Usando a API Diretamente (via `curl`)

Você pode testar o endpoint de scraping diretamente.  Abra um **novo terminal** (enquanto o `docker-compose` está rodando) e use o seguinte comando `curl` :

```bash
curl -X POST "http://localhost:8000/fetch_oab" \
-H "Content-Type: application/json" \
-d '{"name": "Lucas Augusto Capilé Pinotti", "uf": "MS"}'
```

A resposta esperada é um JSON com os dados do advogado:

```json
{
  "oab": "27000",
  "nome": "LUCAS AUGUSTO CAPILÉ PINOTTI",
  "uf": "MS",
  "categoria": "Advogado(a)",
  "data_inscricao": "Não disponível na listagem",
  "situacao": "Não disponível na listagem"
}
```

*(Nota: O número da OAB acima é apenas um exemplo.)*

## 🎬 Demonstração
[Vídeo - DRIVE ](https://drive.google.com/file/d/1z5Mxp7TbiGBReAwHy4646gcdrF3rhvy5/view?usp=sharing)
## 📁 Estrutura do Projeto

```
.
├── agent/
│   └── agent.py          # Lógica do agente LLM com LangChain
├── scraper/
│   └── scraper.py        # Lógica do Web Scraper com Selenium
├── .env                  # Arquivo para credenciais (não versionado)
├── docker-compose.yml    # Orquestração dos serviços Docker
├── Dockerfile            # Definição da imagem Docker da aplicação
├── main.py               # Arquivo da API com FastAPI
├── requirements.txt      # Dependências Python do projeto
└── README.md             # Esta documentação
```

````

