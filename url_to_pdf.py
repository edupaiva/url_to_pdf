import time
import base64
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configuração do Chrome headless
options = Options()
options.add_argument("--headless")  # Executar sem interface gráfica
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Inicializa o WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Acessa a página desejada
url = "http://localhost:5000/alerta/1"
driver.get(url)

# Espera a página estar completamente carregada
WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")

# Espera o elemento do mapa carregar (se houver um elemento específico)
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "map")))
    time.sleep(5)  # Tempo extra para garantir que o JS renderizou tudo
except:
    print("Aviso: O elemento do mapa pode não ter sido carregado totalmente.")

# Gera o PDF sem margens e com gráficos de fundo
pdf_config = {
    "landscape": False,  # True para orientação paisagem
    "displayHeaderFooter": False,  # Remove cabeçalho e rodapé automáticos do Chrome
    "printBackground": True,  # Ativa gráficos de segundo plano (background)
    "marginTop": 0, "marginBottom": 0, "marginLeft": 0, "marginRight": 0,  # Zera as margens
    "paperWidth": 8.27, "paperHeight": 11.69  # Tamanho A4 (padrão do Chrome)
}

pdf = driver.execute_cdp_cmd("Page.printToPDF", pdf_config)

# Decodifica Base64 e salva o arquivo corretamente
pdf_bytes = base64.b64decode(pdf["data"])
with open("saida.pdf", "wb") as f:
    f.write(pdf_bytes)

driver.quit()
print("PDF salvo com sucesso!")
