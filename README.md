# Upload de Foto no Instagram a partir de Artigo no PubMed

## Visão Geral

Este script obtém informações sobre o artigo mais recente sobre Religiosidade ou Espiritualidade no PubMed, captura uma captura de tela da primeira página do artigo e a carrega no Instagram. Ele trata situações em que a legenda padrão é muito longa, tentando com uma legenda mais curta usando o título do artigo.

## Requisitos

Os requisitos se encontram todos em requirements.txt, sendo possível instalá-los com `pip install -r requirements.txt`, de qualquer forma são eles:

- Python 3.x
- Biblioteca Instagrapi (`pip install instagrapi`)
- Selenium (`pip install selenium`)
- Requests (`pip install requests`)
- BeautifulSoup (`pip install beautifulsoup4`)


## Uso

1. Configure suas credenciais do Instagram como variáveis de ambiente: `USUARIO` e `SENHA`.
2. Execute o script: `python procura_artigo.py`

## Configuração

Ajuste as variáveis e parâmetros do script de acordo com suas necessidades específicas. Por exemplo, você pode modificar o termo de pesquisa no PubMed ou alterar as tentativas de repetição para o upload da foto.

termo_pesquisa = 'Religiosity OR Spirituality' (qualquer termo ou combinação booleana de termos)
max_retries = 3 (quantas tentativas você deseja)


# Instagram Photo Upload from PubMed Article

## Overview

This script fetches information about the latest article on Religiosity or Spirituality from PubMed, captures a screenshot of the article's first page, and uploads it to Instagram. It handles situations where the default caption is too long by trying with a shorter caption using the article's title.

## Requirements

All requirements can be found in requirements.txt, you can install with `pip install -r requirements.txt`, nevertheless they are:

- Python 3.x
- Instagrapi library (`pip install instagrapi`)
- Selenium (`pip install selenium`)
- Requests (`pip install requests`)
- BeautifulSoup (`pip install beautifulsoup4`)

## Usage

1. Set up your Instagram credentials as environment variables: `USUARIO` and `SENHA`.
2. Run the script: `python procura_artigo.py`

## Configuration

Adjust the script variables and parameters to meet your specific needs. For instance, you can modify the search term on PubMed or change the retry attempts for photo upload.

termo_pesquisa = 'Religiosity OR Spirituality' (any term or boolean combination of terms)
max_retries = 3 (or the number you want)
