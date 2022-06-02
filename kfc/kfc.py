import json

with open('data.json', 'r', encoding='utf8') as file:
    data = json.load(file)

# print(data['searchResults'][0]['storePublic']['title']['ru'])
# print(data['searchResults'][0]['storePublic']['contacts']['streetAddress']['ru'])
# print(data['searchResults'][0]["storePublic"]['contacts']['"contacts": ']['number'])
# print(data['searchResults'][0]['storePublic']['contacts']['coordinates']['geometry']['coordinates'])
# print(data['searchResults'][0]["storePublic"]['openingHours']['regularDaily'])

# Сравниваем время
def get_time(days):
    all_data = []
    for day in days:
        if all_data:
            for data in all_data:
                if day['timeFrom'] == data[0]['timeFrom'] and day['timeTill'] == data[0]['timeTill']:
                    data.append(day)
                    break
                all_data.append([day])
        else:
            all_data.append([day])

    result = []
    for data in all_data:
        result.append(f'{data[0]["weekDayName"]} - {data[-1]["weekDayName"]}: {data[0]["timeFrom"]} -'
                      f' {data[0]["timeTill"]}')
    return result

# Изменяем json и сохраняем нужный нам формат
def main():
    kfc_file = []
    for d in data['searchResults']:
        time = d["storePublic"]['openingHours']['regularDaily']
        try:
            kfc_file.append({
                'adress': d["storePublic"]['contacts']['streetAddress']['ru'],
                'latlon': d['storePublic']['contacts']['coordinates']['geometry']['coordinates'],
                'name': d['storePublic']['title']['ru'],
                'phones': d["storePublic"]['contacts']['phone']['number'],
                'time': get_time(time)
            })
        except:
            kfc_file.append({
                'adress': '-',
                'latlon': '-',
                'name': '-',
                'phones': '-',
            })

    with open('kfc.json', 'w') as file:
        json.dump(kfc_file, file, ensure_ascii=False, indent=4)
        print('Файл успешно записан')

if __name__ == "__main__":
    main()

