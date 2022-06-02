import json
import requests


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
            json.dump(ziko, file, ensure_ascii=False, indent=4)
            print('Файл успешно записан')
        except Exception as errors:
            print(f'Ошибка {errors}')


save_json(ziko_json)
