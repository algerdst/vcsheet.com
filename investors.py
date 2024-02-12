import time

import requests
from bs4 import BeautifulSoup as bs
import csv



url = "https://www.vcsheet.com/investors?a9fc7870_page=1"


payload = {}
headers = {
  'authority': 'www.vcsheet.com',
  'accept': '*/*',
  'accept-language': 'ru,en;q=0.9',
  'cookie': '_ga=GA1.1.625228123.1700572654; _ga_D2KNTC8QQB=GS1.1.1700572654.1.1.1700573357.0.0.0',
  'referer': 'https://www.vcsheet.com/investors',
  'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "YaBrowser";v="23"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.660 YaBrowser/23.9.5.660 Yowser/2.5 Safari/537.36'
}

def parse():
    page=1
    investors=[]
    columns = ['first_name', 'last_name', 'role', 'company', 'email', 'website', 'twitter',
               'linkedin', 'crunchbase', 'description', 'location', 'notable_investments', 'check_size_range',
               'rounds_their_fund_invests_in', 'sectors_their_fund_invests_in', 'geographies'
               ]
    with open('investors.csv', 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(columns)
        while True:
            if page==1:
                link=url
            else:
                link = f"https://www.vcsheet.com/investors?a9fc7870_page={page}"
            response=requests.get(link,headers=headers)
            soup=bs(response.text, 'lxml')
            blocks=soup.findAll('div', class_='list-item')
            if blocks==[]:
                print('Сбор данных окончен')
                return
            print(f"Страница номер {page}")

            for block in blocks:
                profile_link='https://www.vcsheet.com'+block.findNext('a', class_='full-click')['href']
                response=requests.get(profile_link,headers=headers)
                soup=bs(response.text, 'lxml')
                full_name=soup.find('h1', class_='profile-heading').text.split()
                first_name=full_name[0]
                try:
                    last_name = full_name[1]
                except:
                    last_name = ''
                wrapping=soup.find('div', class_='wrapping').text.split('@')
                role=wrapping[0]
                company=wrapping[1]
                email=soup.find('a',class_='email')['href'].replace('mailto:','')
                website=soup.find('a',class_='link-out-button')['href']
                twitter=soup.find('a',class_='twitter')['href']
                linkedin=soup.find('a',class_='linkedin')['href']
                crunchbase=soup.find('a',class_='crunchbase')['href']
                description=soup.find('div',class_='short-bio').text
                quick_view_grid=soup.find('div', class_='quick-view-grid')
                location=quick_view_grid.findAll('div',class_='quick-view-row')[0].findNext('div',class_='quick-deal-response').text
                notable_investments_list=quick_view_grid.find('div',class_='w-dyn-list').findAll('div', class_='w-dyn-item')
                notable_investments="\n".join([text.text for text in notable_investments_list])
                check_size_range_list = quick_view_grid.findAll('div', class_='quick-view-row')[2].findNext('div',class_='w-dyn-list').findAll('div', class_='w-dyn-item')
                check_size_range="\n".join([text.text for text in check_size_range_list])
                rounds_their_fund_invests_in_list = quick_view_grid.findAll('div', class_='quick-view-row')[3].findNext('div',class_='w-dyn-list').findAll('div', class_='w-dyn-item')
                rounds_their_fund_invests_in = "\n".join([text.text for text in rounds_their_fund_invests_in_list])
                sectors_their_fund_invests_in_list = quick_view_grid.findAll('div', class_='quick-view-row')[5].findNext('div',class_='w-dyn-list').findAll('div', class_='w-dyn-item')
                sectors_their_fund_invests_in= "\n".join([text.text for text in sectors_their_fund_invests_in_list])
                geographies_list = quick_view_grid.findAll('div', class_='quick-view-row')[6].findNext('div',class_='w-dyn-list').findAll('div', class_='w-dyn-item')
                geographies = "\n".join([text.text for text in geographies_list])
                writer.writerow([first_name,last_name,role,company,email,website,twitter,
                                 linkedin,crunchbase,description,location,notable_investments,check_size_range,
                                 rounds_their_fund_invests_in,sectors_their_fund_invests_in,geographies
                                 ])
                print(first_name)
                print(last_name)
                time.sleep(0.5)
                investor=str(full_name)+company
                if investor not in investors:
                    investors.append(investor)
            page+=1
            print(f'Собрано {len(investors)} инвесторов')

if __name__ == '__main__':
    parse()
