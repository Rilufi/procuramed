import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import os
from instagrapi import Client
from instagrapi.exceptions import ClientError
from selenium.webdriver.common.by import By
import google.generativeai as genai
import sys

# Chamando variáveis secretas
USUARIO = os.environ.get("USUARIO")
SENHA = os.environ.get("SENHA")
tele_user = os.environ.get("TELE_USER")
TOKEN = os.environ["TELEGRAM_TOKEN"]
GOOGLE_API_KEY=os.environ["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# Logando no Insta
try:
    cl = Client(request_timeout=7)
    cl.login(USUARIO, SENHA)
    print('Bot logado')
except ClientError as e:
    if e.status_code == 403:
        print(f"Erro durante o login: {e}")
        print("Exiting script due to 403 Forbidden error.")
        bot.send_message(tele_user, 'procuramed com problema pra logar')
        sys.exit()
    else:
        print('Bot deslogado')
        bot.send_message(tele_user, 'procuramed com problema pra logar')
        sys.exit()

# Realiza uma pesquisa no PubMed
url = 'https://pubmed.ncbi.nlm.nih.gov/'
termo_pesquisa = '(spirituality OR religiosity) AND (medical practice OR medical education)'

params = {'term': termo_pesquisa, 'sort': 'date'}
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
        print(f'Título: {titulo}\nAbstract: {abstract}')

        model = genai.GenerativeModel('gemini-pro')

        # Função para gerar conteúdo traduzido usando o modelo GenAI
        def gerar_traducao(prompt):
            response = model.generate_content(prompt)
            # Verifique se a resposta contém candidatos e se a lista não está vazia
            if response.candidates and len(response.candidates) > 0:
                if response.candidates[0].content.parts and len(response.candidates[0].content.parts) > 0:
                    return response.candidates[0].content.parts[0].text
                else:
                    print("Nenhuma parte de conteúdo encontrada na resposta.")
            else:
                print(f"Nenhum candidato válido encontrado, tentando novamente...")

        # Combinar o título e o abstract em um único prompt
        prompt_combinado = f"Given the following scientific text from a reputable source (Pubmed) in English, translate it accurately and fluently into grammatically correct Brazilian Portuguese while preserving the scientific meaning:\n{titulo}\n{abstract}"

        try:
            traducao_combinada = gerar_traducao(prompt_combinado)
            # Separe a tradução combinada em título e abstract
            titulo_traduzido, abstract_traduzido = traducao_combinada.split('\n', 1)

            # Use as traduções na string do Instagram
            insta_string = f"{titulo_traduzido}\n\n{abstract_traduzido}"
            print(insta_string)


            if len(insta_string) > 2200:
                gerar_traducao(f"Faça um resumo de até 2200 caracteres do seguinte texto científico:{insta_string}")
   
        # Se não conseguir traduzir, poste em inglês
        except AttributeError:
            insta_string = f"{titulo}\n\n{abstract}"
            print(insta_string)
                if len(insta_string) > 2200:
                    insta_string = f"{titulo}"

    else:
        print(f'Erro ao acessar o artigo: {response_artigo.status_code}')

    # Acessa a página do artigo usando o WebDriver
    driver.get('https://pubmed.ncbi.nlm.nih.gov' + link_ultimo_artigo)

    # Atraso antes de rolar a página
    time.sleep(2)

    # Rola a página para baixo
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.DOWN + Keys.DOWN + Keys.DOWN)

    # Atraso antes de capturar a tela
    time.sleep(5)

    # Captura a tela e salva como uma imagem
    driver.save_screenshot('screenshot.png')

    # Imprime as informações
    print(f'Imagem da tela capturada e salva como screenshot.png')

    # Fechar o WebDriver
    driver.quit()

    # Caminho para o arquivo de texto onde a legenda será salva
    legenda_arquivo = 'legenda.txt'


    # Verifica se a legenda atual é diferente da legenda anterior
    with open(legenda_arquivo, 'r') as file:
        legenda_anterior = file.read().strip()

    # Comparar a legenda atual com a legenda anterior
    if insta_string.strip() == legenda_anterior:
        print("A legenda é igual à anterior. Não há novos artigos para publicar.")
        sys.exit()  # Sai do script porque não há artigos novos
    else:
        # Salva a legenda atual no arquivo de texto
        with open(legenda_arquivo, 'w') as file:
            file.write(insta_string.strip())
    
    # Tentativa de upload da foto com a legenda
    max_retries = 3
    retry_count = 0

    while retry_count < max_retries:
        try:
            # Tentativa de upload com a legenda
            cl.photo_upload('screenshot.png', insta_string)
            print("Foto publicada no Instagram")
            break  # Encerra o loop se o upload for bem-sucedido
        except ClientError as e:
            print(f"Erro durante o upload da foto: {e}")
            retry_count += 1
            if retry_count < max_retries:
                print(f"Tentativa {retry_count}/{max_retries}")

                # Verificar se o erro é devido à legenda muito longa
                if "Caption too long" in str(e):
                    print("Legenda muito longa. Tentando com o título.")
                    # Tentativa de upload com a legenda do título
                    cl.photo_upload('screenshot.png', titulo_string)
                    print("Foto publicada no Instagram usando o título.")
                    break  # Encerra o loop se o upload for bem-sucedido
                elif "403" in str(e):  # Verifica se a mensagem de erro contém "403"
                    print("Encerrando o script devido ao erro 403 Forbidden.")
                    break  # Encerra o loop se ocorrer erro 403 Forbidden durante o upload
        else:
            print("Número máximo de tentativas alcançado. Falha no upload da foto.")

else:
    print(f'Erro na pesquisa PubMed: {response.status_code}')
