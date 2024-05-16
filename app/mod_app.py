import requests
from bs4 import BeautifulSoup
import csv

base_url = 'https://alestech.ru/factories/tag-48-lesozagotovitelnye-predpriatia?page='

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

def get_company_links(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    company_links = soup.find_all('a', href=True)
    company_links = [link['href'] for link in company_links if '/factory/' in link['href']]
    
    return company_links

csv_file_path = 'companies_info.csv'

with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Название предприятия', 'Ссылка на вебсайт компании', 'Описание компании']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for page_number in range(23):
        page_url = base_url + str(page_number+1)
        company_links = get_company_links(page_url)
        
        if not company_links:
            break
        
        for link in company_links:
            full_url = 'https://alestech.ru' + link
            info = get_company_info(full_url)
            writer.writerow({
                'Название предприятия': info['name'],
                'Ссылка на вебсайт компании': info['url'],
                'Описание компании': info['description']
            })
        
        print(f"Обработана страница {page_number}")

print(f"Данные успешно записаны в файл {csv_file_path}")
