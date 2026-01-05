import os
import requests
from langchain_core.tools import tool
from dotenv import load_dotenv
from langchain_cloudflare.chat_models import ChatCloudflareWorkersAI
from langchain.agents import AgentType, initialize_agent

load_dotenv()

@tool
def fetch_oab(name: str, uf: str) -> dict:

    api_url = "http://scraper-api:8000/fetch_oab"
    try:
        response = requests.post(api_url, json={"name": name, "uf": uf})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        return f"Erro ao chamar a API: {e.response.status_code} - {e.response.text}"
    except requests.exceptions.RequestException as e:
        return f"Erro de conexão com a API: {str(e)}"

# Configuração do Agente
tools = [fetch_oab]

llm = ChatCloudflareWorkersAI(
    model="@cf/meta/llama-3-8b-instruct",
    cloudflare_account_id=os.getenv("CF_ACCOUNT_ID"),
    cloudflare_api_token=os.getenv("CF_API_TOKEN"),
)


# Criação do Agente 
agent_executor = initialize_agent(
    tools,
    llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True 
)
def run_agent_query(question: str):
    """Executa uma pergunta através do agente LLM."""
    print(f"\n[PERGUNTA]: {question}")
    result = agent_executor.run(question)
    print(f"\n[RESPOSTA]: {result}")

if __name__ == "__main__":
    run_agent_query("Qual o número da OAB e a categoria de Lucas Augusto Capilé Pinotti no Mato Grosso do Sul (MS)?")
    run_agent_query("Qual a previsão do tempo para hoje em Campo Grande?")