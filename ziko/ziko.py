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

#Парсим данные
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
            sklep_time = sklep.find('td', attrs={'class': 'mp-table-hours'})

            ziko.append({
                'adress': street.text,
                'lation': '-',
                'name': sklep_name.text,
                'phones': tel.text,
                'working_hours': sklep_time.text
            })
        save_json_bs(ziko)

# Сохраняем данные в json
def save_json_bs(ziko):
    with open('ziko_BS.json', 'w', encoding="utf-8") as file:
        try:
            json.dump(ziko, file, ensure_ascii=False, indent=4)
            print('Файл записан')
        except Exception as error:
            print(f'Ошибка - {error}')



# забираем данные через api
def fetch(url, params):
    headers = params['headers']
    if params['method'] == 'GET':
        return requests.get(url, headers=headers)


ziko = fetch("https://www.ziko.pl/wp-admin/admin-ajax.php?action=get_pharmacies", {
    "headers": {
        "accept": "*/*",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"102\", \"Google Chrome\";v=\"102\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest",
        "cookie": "smuuid=1811aa8b478-3b936bcf1086-9c292587-d424c63d-f5038fb1-a119c1e9fa44; cookielawinfo-checkbox-necessary=yes; cookielawinfo-checkbox-non-necessary=yes; viewed_cookie_policy=yes; cli_user_preference=pl-cli-yes-checkbox-necessary-yes-checkbox-non-necessary-yes; CookieLawInfoConsent=eyJ2ZXIiOiIxIiwibmVjZXNzYXJ5IjoidHJ1ZSIsIm5vbi1uZWNlc3NhcnkiOiJ0cnVlIn0=; _ga=GA1.2.909905595.1654009704; _gid=GA1.2.141703070.1654009704; _fbp=fb.1.1654009705530.1609494194; _smvs=SEARCH_ENGINE; PHPSESSID=ccm6hkvopk88l45rgv63mpaf5n; smvr=eyJ2aXNpdHMiOjMsInZpZXdzIjoyMCwidHMiOjE2NTQxMjExMjc3MTUsIm51bWJlck9mUmVqZWN0aW9uQnV0dG9uQ2xpY2siOjAsImlzTmV3U2Vzc2lvbiI6ZmFsc2V9; _gat_UA-7881404-6=1; _gat=1",
        "Referer": "https://www.ziko.pl/lokalizator/",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    },
    "body": None,
    "method": "GET"
})

data = ziko.json()
ziko_json = []
for k, v in data.items():
    #экхемпляр класса
    name = v['title']
    lation = v['lat'], v['lng']
    address = v['address']
    w_hours = v['mp_pharmacy_hours']
    ziko_json.append({
        'address': address,
        'lation': lation,
        'name': name,
        'phones': '-',
        'working_hours': w_hours.replace('<br>', '')
    })



def save_json(ziko_json):
    with open('ziko.json', 'w', encoding='utf-8') as file:
        try:
            json.dump(ziko_json, file, ensure_ascii=False, indent=4)
            print('Файл успешно записан')
        except Exception as errors:
            print(f'Ошибка {errors}')
save_json(ziko_json)



# Добавляем из второго json файла недостоющие данные в первый
with open('ziko_BS.json', 'r', encoding='utf-8') as file_BS:
    data = json.load(file_BS)
with open('ziko.json', 'r', encoding='utf-8') as file:
    data1 = json.load(file)

fin_file = []
for d in data:
    for d1 in data1:
        if d['adress'] == d1['address']:
            d['lation'] = d1['lation']
            fin_file.append(d)

with open('ziko_fin.json', 'w', encoding='utf-8') as fin:
    try:
        json.dump(fin_file, fin, ensure_ascii=False, indent=4)
    except Exception as er:
        print(f'Ошибка {er}')

