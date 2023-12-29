import requests
import os
import sys
from urllib.parse import urljoin
from bs4 import BeautifulSoup

if len(sys.argv) != 3:
    print("Uso: script.py <url> <ruta de destino>")
    sys.exit(1)

url = sys.argv[1]
folder_path = sys.argv[2]

def get_js_files(url):
    try:
        response = requests.get(url)
        # Verifica que la petición fue exitosa y que el contenido es HTML
        if response.status_code == 200 and 'text/html' in response.headers.get('Content-Type', ''):
            soup = BeautifulSoup(response.text, 'html.parser')
            script_tags = soup.find_all('script')
            js_files = [tag.get('src') for tag in script_tags if tag.get('src') and tag.get('src').endswith('.js')]
            return js_files
        else:
            print(f"Error {response.status_code}: No se pudo encontrar la página o el contenido no es HTML.")
            sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la petición: {e}")
        sys.exit(1)

def download_files(urls, folder_path):
    if not os.path.isdir(folder_path):
        os.makedirs(folder_path)

    for url in urls:
        file_name = os.path.basename(url)
        file_path = os.path.join(folder_path, file_name)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                    print(f"Archivo {file_name} descargado en {file_path}")
            else:
                print(f"Error {response.status_code}: No se pudo descargar el archivo {url}")
        except requests.exceptions.RequestException as e:
            print(f"Error al descargar {url}: {e}")

js_files = get_js_files(url)
if js_files:
    js_files_full_urls = [urljoin(url, js_file) for js_file in js_files]
    download_files(js_files_full_urls, folder_path)
else:
    print("No se encontraron archivos .js en la página.")
