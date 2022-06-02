import json
import re

import requests


# Сохраняем нашу html страничку
def save_html():
    url = 'https://monomax.by/map'
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 '
                      'Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    r = requests.get(url, headers)
    if r.status_code == 200:
        with open('monomah.html', 'w', encoding='utf-8') as file:
            file.write(r.text)
save_html()


# Находим используя ругялрные выражения в нашем html нужные нам данные
def get_content():
    with open('monomah.html', 'r', encoding='utf-8') as file:
        data = file.read()
        pattern = re.compile("\[(\d{2}\.\d+), (\d{2}\.\d+)\],\n\n\s+\{\n\s+balloonContentHeader: \'([^']+)\',"
                         "\n\s+balloonContentBody: 'Телефон: (\+\d+)\s+'")

    result = pattern.findall(data)
    monomah = []

    for r in result:
        monomah.append({
            'adress': r[2],
            'lation': [r[0],r[1]],
            'name': 'Мономах',
            'phones': r[3]
        })

    save_json(monomah)


# Записываем данные в json
def save_json(monomah):
    with open('monomah.json', 'w') as file:
        try:
            json.dump(monomah, file, ensure_ascii=False, indent=4)
            print('Файл записан')
        except Exception as errors:
            print(f'Ошибка: {errors}')

get_content()
