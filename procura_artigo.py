import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import requests
import json
import os
from instagrapi import Client
from instagrapi.exceptions import ClientError
from selenium.webdriver.common.by import By

#calling secret variables
USUARIO = os.environ.get("USUARIO")
SENHA = os.environ.get("SENHA")

try:
    cl = Client(request_timeout=7)
    cl.login(USUARIO, SENHA)
    print('bot logado')
except ClientError as e:
    if e.status_code == 403:
        print(f"Error during login: {e}")
        print("Exiting script due to 403 Forbidden error.")
        exit()
    else:
        print('bot deslogado')
        pass

url = 'https://pubmed.ncbi.nlm.nih.gov/'
termo_pesquisa = 'Religiosity OR Spirituality'

# Realiza uma pesquisa no PubMed
params = {'term': termo_pesquisa,
          'sort': 'date'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
response = requests.get(url, params=params, headers=headers)

if response.status_code == 200:
    # Parseia a página usando BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontra o link do último artigo
    link_ultimo_artigo = soup.find('a', class_='docsum-title')['href']

    # Configura o WebDriver do Selenium para capturar a tela
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(f"user-agent={headers['User-Agent']}")
    driver = webdriver.Chrome(options=chrome_options)

    # Atraso antes de acessar a página do artigo
    time.sleep(2)


    response_artigo = requests.get('https://pubmed.ncbi.nlm.nih.gov' + link_ultimo_artigo)
    if response_artigo.status_code == 200:
        soup_artigo = BeautifulSoup(response_artigo.text, 'html.parser')

        # Extrai informações desejadas (exemplo: título e abstract)
        titulo = soup_artigo.find('h1', class_='heading-title').text.strip()
        abstract = soup_artigo.find('div', class_='abstract-content').text.strip()

        # Imprime as informações
        print(f'Title: {titulo}\nAbstract: {abstract}')

        insta_string = f""" {titulo}

{abstract}"""


    else:
        print(f'Erro ao acessar o artigo: {response_artigo.status_code}')

    # Acessa a página do artigo usando o WebDriver
    driver.get('https://pubmed.ncbi.nlm.nih.gov' + link_ultimo_artigo)

    # Atraso antes de rolar a página
    time.sleep(2)

    # Rola a página para baixo
    driver.find_element(By.TAG_NAME,'body').send_keys(Keys.DOWN + Keys.DOWN + Keys.DOWN)

    # Atraso antes de capturar a tela
    time.sleep(5)

    # Captura a tela e salva como uma imagem
    driver.save_screenshot('screenshot.png')

    # Imprime as informações
    print(f'Imagem da tela capturada e salva como screenshot.png')

    # Fechar o WebDriver
    driver.quit()

else:
    print(f'Erro na pesquisa PubMed: {response.status_code}')


max_retries = 3
retry_count = 0

while retry_count < max_retries:
    try:
        cl.photo_upload('screenshot.png', insta_string)
        print("foto publicada no insta")
        break  # Break the loop if upload is successful
    except ClientError as e:
        print(f"Error during photo upload: {e}")
        retry_count += 1
        if retry_count < max_retries:
            print(f"Retrying... (Attempt {retry_count}/{max_retries})")
            if "403" in str(e):  # Check if the error message contains "403"
                print("Exiting script due to 403 Forbidden error.")
                break  # Break the loop if 403 Forbidden error occurs during upload
        else:
            print("Max retries reached. Photo upload failed.")
