import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

uf_to_state_name = {
    "AC": "Acre", "AL": "Alagoas", "AP": "Amapá", "AM": "Amazonas", "BA": "Bahia",
    "CE": "Ceará", "DF": "Distrito Federal", "ES": "Espírito Santo", "GO": "Goiás",
    "MA": "Maranhão", "MT": "Mato Grosso", "MS": "Mato Grosso do Sul", "MG": "Minas Gerais",
    "PA": "Pará", "PB": "Paraíba", "PR": "Paraná", "PE": "Pernambuco", "PI": "Piauí",
    "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte", "RS": "Rio Grande do Sul",
    "RO": "Rondônia", "RR": "Roraima", "SC": "Santa Catarina", "SP": "São Paulo",
    "SE": "Sergipe", "TO": "Tocantins"
}

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    return driver

def fetch_lawyer_data(name: str, uf: str) -> dict:
    driver = get_driver()
    url = "https://cna.oab.org.br/"
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 20)

        name_field = wait.until(EC.presence_of_element_located((By.ID, "txtName")))
        name_field.send_keys(name)

        uf_upper = uf.upper()
        if uf_upper not in uf_to_state_name:
            return {"error": f"UF '{uf}' é inválida."}

        state_name = uf_to_state_name[uf_upper]
        option_text = f"Conselho Seccional - {state_name}"

        uf_select_element = wait.until(EC.presence_of_element_located((By.ID, "cmbSeccional")))
        uf_select = Select(uf_select_element)
        uf_select.select_by_visible_text(option_text)

        search_button = driver.find_element(By.ID, "btnFind")
        search_button.click()

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#divResult .row")))
        except TimeoutException:
            not_found_element = driver.find_element(By.ID, "textResult")
            if "não retornou nenhum resultado" in not_found_element.text:
                return {"error": "Advogado não encontrado."}
            else:
                raise TimeoutException("A página não carregou resultados nem a mensagem de erro esperada.")

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        first_result = soup.find("div", class_="row")
        
        nome_div = first_result.find(class_="rowName")
        nome = nome_div.find_all('span')[-1].text.strip() if nome_div else "Não informado"

        tipo_div = first_result.find(class_="rowTipoInsc")
        categoria = tipo_div.find_all('span')[-1].text.strip() if tipo_div else "Não informado"

        insc_div = first_result.find(class_="rowInsc")
        oab = insc_div.find_all('span')[-1].text.strip() if insc_div else "Não informado"

        uf_div = first_result.find(class_="rowUf")
        uf_seccional = uf_div.find_all('span')[-1].text.strip() if uf_div else "Não informado"
        
        return {
            "oab": oab,
            "nome": nome,
            "uf": uf_seccional,
            "categoria": categoria,
            "data_inscricao": "Não disponível na listagem",
            "situacao": "Não disponível na listagem"
        }

    except TimeoutException:
        return {"error": "A página demorou muito para responder ou um elemento não foi encontrado (Timeout)."}
    except Exception as e:
        return {"error": f"Ocorreu um erro inesperado: {str(e)}"}
    finally:
        driver.quit()