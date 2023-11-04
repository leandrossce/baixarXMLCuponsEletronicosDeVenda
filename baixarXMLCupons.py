import requests
from urllib.parse import urlparse
import os

#diretório onde serão salvos os XML dos cupons de vendas
diretorio_xml = 'C:\\Users\\WDAGUtilityAccount\\Desktop\\Nova pasta\\aqui\\'

#arquivo que contem as chaves dos XML que serão salvos - as chaves contidas nesse arquivo deverão estar salvas linha a linha, ou seja, uma chave por linha
links_file = 'C:\\Users\\WDAGUtilityAccount\\Desktop\\Nova pasta\\lista.csv'

primeira_parte_url='https://cfe.sefaz.ce.gov.br:8443/portalcfews/mfe/fiscal-coupons/xml/'
segunda_parte_url='?apiKey=eyJhbGciOiJIUzI1NiJ9'

# Função para extrair o nome do arquivo do link
def get_filename_from_url(url):
    # Parseia o URL para extrair o caminho
    parsed_url = urlparse(url)
    # Pega o último componente do caminho para usar como nome do arquivo
    return os.path.basename(parsed_url.path)

# Função para fazer o download do arquivo
def download_file(url):
    try:
        # Faz a requisição ao servidor
        response = requests.get(url, stream=True)
        # Verifica se a requisição foi bem sucedida
        response.raise_for_status()
        
        # Extrai o nome do arquivo do URL
        
        filename = get_filename_from_url(url)
        file_path = os.path.join(diretorio_xml, filename)
        
        # Abre um arquivo local para escrita em modo binário
        with open(file_path, 'wb') as file:
            # Escreve o conteúdo do arquivo em blocos de 1024 bytes
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # Filtra out keep-alive new chunks
                    file.write(chunk)
            print(f"Download completo: {filename}")
    except requests.exceptions.HTTPError as errh:
        print(f"Erro HTTP: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Erro de Conexão: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Erro: {err}")

# Lê o arquivo com os links
def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        chave=[line.strip() for line in file]
        return chave


urls = read_urls_from_file(links_file)

# Faz o download de cada arquivo
for url in urls:
    download_file(primeira_parte_url+url+segunda_parte_url)
