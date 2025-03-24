import os
import requests
import zipfile
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL da página
URL = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

# Cria o diretório de downloads
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def get_pdf_links(url):
    """PEga os links do Anexo 1 e Anexo 2."""
    response = requests.get(url)
    response.raise_for_status()  # Se tiver um erro na resposta HTTP, ele levanta uma exceção
    soup = BeautifulSoup(response.text, "html.parser")

    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]  # Não converte mais para minúsculas

        # Verifica se é um link para os Anexos I ou II
        if ".pdf" in href and ("Anexo_I" in href or "Anexo_II" in href):
            absolute_url = urljoin(url, href)  # Faz o link ser absoluto
            links.append(absolute_url)

    return links

def download_pdfs(links):
    """Baixa os PDFs e salva na pasta downloads."""
    pdf_paths = []
    for link in links:
        filename = os.path.join(DOWNLOAD_DIR, os.path.basename(link))

        try:
            response = requests.get(link)
            response.raise_for_status()  # Levanta erro se a requisição falhar
            with open(filename, "wb") as file:
                file.write(response.content)
            pdf_paths.append(filename)
            print(f"Baixado: {filename} ({len(response.content)} bytes)")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao baixar {link}: {e}")

    return pdf_paths

def zip_files(files, output_filename="downloads/anexos.zip"):
    """Compacta os PDFs em um arquivo ZIP."""
    if not files:
        print("Nenhum arquivo para compactar.")
        return

    with zipfile.ZipFile(output_filename, "w") as zipf:
        for file in files:
            zipf.write(file, os.path.basename(file))
    print(f"Arquivos compactados em {output_filename}")

if __name__ == "__main__":
    print("Buscando links de PDFs...")
    pdf_links = get_pdf_links(URL)

    if not pdf_links:
        print("Nenhum PDF encontrado.")
    else:
        print(f"{len(pdf_links)} PDFs encontrados.")
        pdf_files = download_pdfs(pdf_links)
        zip_files(pdf_files)
