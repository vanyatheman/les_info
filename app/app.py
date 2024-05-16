import csv

import requests
from bs4 import BeautifulSoup

url = 'https://alestech.ru/factories/tag-48-lesozagotovitelnye-predpriatia?page=2'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

company_links = soup.find_all('a', href=True)

company_links = [link['href'] for link in company_links if '/factory/' in link['href']]
print(company_links)

base_url = 'https://alestech.ru'

def get_company_info(company_url):
    response = requests.get(company_url)
    company_soup = BeautifulSoup(response.content, 'html.parser')
    
    company_name_tag = company_soup.find('h2', class_='red text-left')
    company_name = company_name_tag.get_text(strip=True).replace('Информация о компании «', '').replace('»', '') if company_name_tag else 'N/A'
    
    company_description_div = company_soup.find('div', class_='mb-3 text-left')
    company_description = company_description_div.get_text(strip=True) if company_description_div else 'N/A'
    
    company_info = {
        'name': company_name,
        'url': company_url,
        'description': company_description
    }
    
    return company_info

companies_info = []
for link in company_links:
    full_url = base_url + link
    info = get_company_info(full_url)
    companies_info.append(info)

csv_file_path = 'companies_info.csv'

with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Название предприятия', 'Ссылка на вебсайт компании', 'Описание компании']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    writer.writeheader()
    for company in companies_info:
        writer.writerow({
            'Название предприятия': company['name'],
            'Ссылка на вебсайт компании': company['url'],
            'Описание компании': company['description']
        })

print(f"Данные успешно записаны в файл {csv_file_path}")