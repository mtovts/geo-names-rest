## HTTP-сервер для предоставления информации по географическим объектам.
Данные взяты [из географической базы данных GeoNames](http://download.geonames.org/export/dump/RU.zip).

Описание формата данных можно найти в [readme.txt](readme.txt).

---

Реализованный сервер предоставляет REST API сервис со следующими методами:
1.	Метод принимает идентификатор geonameid и возвращает информацию о городе.
#### Пример:
Обратившись к http://127.0.0.1:8000/info?geonameid=451747, получим ответ:
```
{'admin1 code': '77',
 'asciiname': 'Zyabrikovo',
 'country code': 'RU',
 'dem': '204',
 'feature class': 'P',
 'feature code': 'PPL',
 'geonameid': '451747',
 'latitude': '56.84665',
 'longitude': '34.7048',
 'modification date': '2011-07-09',
 'name': 'Zyabrikovo',
 'population': '0',
 'timezone': 'Europe/Moscow'}
```
2.	Метод принимает страницу и количество отображаемых на странице городов и возвращает список городов с их информацией. 
#### Пример:
Обратившись к http://127.0.0.1:8000/page/3?per_page=5, получим ответ:
```
{'admin1 code': {'10': '77', '11': '77', '12': '77', '13': '77', '14': '77'},
 'asciiname': {'10': "Zamush'ye",
               '11': "Zaleden'ye",
               '12': 'Urochishche Zakaznik',
               '13': "Zador'ye",
               '14': "Zabolot'ye"},
 'country code': {'10': 'RU', '11': 'RU', '12': 'RU', '13': 'RU', '14': 'RU'},
 'dem': {'10': '182', '11': '278', '12': '219', '13': '224', '14': '190'},
 'feature class': {'10': 'P', '11': 'P', '12': 'L', '13': 'P', '14': 'P'},
 'feature code': {'10': 'PPL',
                  '11': 'PPLQ',
                  '12': 'LCTY',
                  '13': 'PPL',
                  '14': 'PPL'},
 'geonameid': {'10': '451757',
               '11': '451758',
               '12': '451759',
               '13': '451760',
               '14': '451761'},
 'latitude': {'10': '57.22984',
              '11': '57.12851',
              '12': '56.89212',
              '13': '56.85239',
              '14': '56.74771'},
 'longitude': {'10': '34.77983',
               '11': '34.26788',
               '12': '34.56952',
               '13': '34.49864',
               '14': '34.84792'},
 'modification date': {'10': '2011-07-09',
                       '11': '2011-07-09',
                       '12': '2011-07-09',
                       '13': '2011-07-09',
                       '14': '2011-07-09'},
 'name': {'10': 'Zamush’ye',
          '11': 'Zaleden’ye',
          '12': 'Urochishche Zakaznik',
          '13': 'Zador’ye',
          '14': 'Zabolot’ye'},
 'population': {'10': '0', '11': '0', '12': '0', '13': '0', '14': '0'},
 'timezone': {'10': 'Europe/Moscow',
              '11': 'Europe/Moscow',
              '12': 'Europe/Moscow',
              '13': 'Europe/Moscow',
              '14': 'Europe/Moscow'}}
```
3.	Метод принимает названия двух городов (на русском языке) и получает информацию о найденных городах. А также дополнительно: какой из них расположен севернее, одинаковая ли у них временная зона и на сколько часов они различаются. Когда несколько городов имеют одно и то же название, неоднозначность разрешается выбором города с большим населением. Если население совпадает, берется первый попавшийся.
#### Пример:
Обратившись к http://127.0.0.1:8000/cities?city1=Томск&city2=Москва, получим ответ:
```
[{'admin1 code': '75',
  'asciiname': 'Tomsk',
  'country code': 'RU',
  'dem': '141',
  'feature class': 'S',
  'feature code': 'HTL',
  'geonameid': '10232663',
  'latitude': '56.46118',
  'longitude': '84.98842',
  'modification date': '2015-04-22',
  'name': 'Tomsk',
  'population': '0',
  'timezone': 'Asia/Tomsk'},
 {'admin1 code': '00',
  'alternatenames': 'Moscow River,Moskva,Москва',
  'asciiname': 'Moskva',
  'country code': 'RU',
  'dem': '98',
  'feature class': 'H',
  'feature code': 'STM',
  'geonameid': '524895',
  'latitude': '55.0759',
  'longitude': '38.844',
  'modification date': '2012-01-17',
  'name': 'Moskva',
  'population': '0',
  'timezone': 'Europe/Moscow'},
 {'northernmost_geonameid': '10232663', 'same_tz': false, 'tz_difference': 4.0}]
```

# Запуск

1. Клонировать репозиторий
2. Установить зависимости командой
`pip install -r requirements.txt`
3. Запустить script.py
`python3 script.py`
