import json
import requests
from bs4 import BeautifulSoup


# Сохраняем нашу html страничку
# def save_html():
#     url = 'https://www.ziko.pl/lokalizator/'
#     headers = {
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                       'Chrome/102.0.5005.63 Safari/537.36',
#         'accept': '*/*'
#     }
#     r = requests.get(url, headers)
#     if r.status_code == 200:
#         with open('ziko_BS.html', 'w', encoding='utf-8') as file:
#             file.write(r.text)
# save_html()

#Парсин данные
def get_context():
    with open('ziko_bs.html', 'r') as file:
        data = file.read()
        page = BeautifulSoup(data, 'html.parser')
        all_sklep = page.find('tbody', attrs={'class': 'mp-pharmacies-table-elements clearfix'})
        sklep_list = all_sklep.find_all('tr')


        ziko = []
        for sklep in sklep_list:
            sklep_name = sklep.find('span', attrs={'class': 'mp-pharmacy-head'})
            sklep_adress = sklep.find('td', attrs={'class': 'mp-table-address'})
            tel = sklep_adress.next.next.next.next.next.next.next
            street = sklep_adress.next
            street_addition = street.next.next
            city = street.next.next.next.next
            sklep_time = sklep.find('td', attrs={'class': 'mp-table-hours'})

            ziko.append({
                'adress': (street.text + street_addition.text + city.text),
                'lation': '-',
                'name': sklep_name.text,
                'phones': tel.text,
                'working_hours': sklep_time.text
            })

        save_json(ziko)


#Сохраняем данные в json
def save_json(ziko):
    with open('ziko_BS.json', 'w', encoding="utf-8") as file:
        try:
            json.dump(ziko, file, ensure_ascii=False, indent=4)
            print('Файл записан')
        except Exception as error:
            print(f'Ошибка - {error}')

get_context()
