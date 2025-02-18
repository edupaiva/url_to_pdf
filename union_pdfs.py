import time
import base64
import fitz  # PyMuPDF para unir PDFs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# URLs das páginas a serem convertidas em PDF
urls = [
    "http://localhost:5000/alerta/1",
    "http://localhost:5000/alerta/2"
]

# Configuração do Chrome headless
options = Options()
options.add_argument("--headless")  # Executar sem interface gráfica
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Inicializa o WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

pdf_files = []

for i, url in enumerate(urls, start=1):
    driver.get(url)

    # Espera o carregamento da página
    time.sleep(3)  # Tempo extra para carregar JavaScript, ajustar conforme necessário

    # Configuração de impressão para PDF
    pdf_config = {
        "landscape": False,
        "displayHeaderFooter": False,
        "printBackground": True,  # Inclui gráficos de fundo
        "marginTop": 0, "marginBottom": 0, "marginLeft": 0, "marginRight": 0,
        "paperWidth": 8.27, "paperHeight": 11.69  # A4
    }

    # Gera PDF da página
    pdf = driver.execute_cdp_cmd("Page.printToPDF", pdf_config)

    # Salva o PDF temporário
    pdf_path = f"pagina_{i}.pdf"
    with open(pdf_path, "wb") as f:
        f.write(base64.b64decode(pdf["data"]))
    
    pdf_files.append(pdf_path)

driver.quit()

# **UNIR PDFs**
final_pdf = "alerta_completo.pdf"
pdf_document = fitz.open()

for pdf in pdf_files:
    pdf_document.insert_pdf(fitz.open(pdf))

pdf_document.save(final_pdf)
pdf_document.close()

print(f"PDF final salvo como: {final_pdf}")
