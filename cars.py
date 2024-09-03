from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

def extrair_dados_pagina(page_number):
    url = f"https://exclusivecarregistry.com/list?page={page_number}"
    driver.get(url)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    car_items = soup.find_all('div', class_='car_item')

    dados = []
    for item in car_items:
        texto = item.find('div', class_='texto')
        title = texto.find('p', class_='title').get_text(strip=True)

        strong_tag = texto.find('strong')
        strong_tag_text = strong_tag.get_text(strip=True) if strong_tag else ''

        stats = item.find('div', class_='stats')
        stats_data = []
        for stat in stats.find_all('div', class_='icons_info'):
            alt_text = stat.find('img')['alt'] 
            value = stat.find('p').get_text(strip=True)
            stats_data.append((alt_text, value))

        dados.append({
            'Title': title,
            'Strong Tag Text': strong_tag_text,
            'Stat 1 Alt': stats_data[0][0] if len(stats_data) > 0 else '',
            'Stat 1 Value': stats_data[0][1] if len(stats_data) > 0 else '',
            'Stat 2 Alt': stats_data[1][0] if len(stats_data) > 1 else '',
            'Stat 2 Value': stats_data[1][1] if len(stats_data) > 1 else '',
            'Stat 3 Alt': stats_data[2][0] if len(stats_data) > 2 else '',
            'Stat 3 Value': stats_data[2][1] if len(stats_data) > 2 else '',
            'Stat 4 Alt': stats_data[3][0] if len(stats_data) > 3 else '',
            'Stat 4 Value': stats_data[3][1] if len(stats_data) > 3 else '',
        })

    return dados
# Analisando o site percebi que tinha uma paginação mas ela não era evidente,
# e colocando valores aleatórios vi que tinha mais de 3000 páginas.
page_number = 1
all_data = []

while True: # Fiz esse while mais detalhado para acompanhar a mudança de página.
    print(f"Extraindo dados da página {page_number}...")
    page_data = extrair_dados_pagina(page_number)
    
    if not page_data:
        print("Não há mais dados a serem extraídos. Finalizando.")
        break

    all_data.extend(page_data)
    page_number += 1

driver.quit()

df = pd.DataFrame(all_data)

df.to_excel("car_profiles.xlsx", index=False)
print("Dados salvos em 'car_profiles.xlsx'")
