import requests

BASE_URL_USER = 'http://127.0.0.1:8000/api/user'
BASE_URL_LOGIN = 'http://127.0.0.1:8000/api/login'
BASE_URL_ADV = 'http://127.0.0.1:8000/api/advertisement'


# #Создаем юзера
# data = requests.post(f"{BASE_URL_USER}",
#                      json={"name": "user3", "password": "11111111"})
# print(data.status_code)
# print(data.json())
#
# data = requests.post(f"{BASE_URL_USER}",
#                      json={"name": "user4", "password": "22222222"})
# print(data.status_code)
# print(data.json())
#
# #Создаем токены
# data = requests.post(f"{BASE_URL_LOGIN}",
#                      json={"name": "user3", "password": "11111111"})
# print(data.status_code)
# print(data.json())
# token1=data.json()["token"]
#
# data = requests.post(f"{BASE_URL_LOGIN}",
#                      json={"name": "user4", "password": "22222222"})
# print(data.status_code)
# print(data.json())
# token2=data.json()["token"]
#
#
# #Создаем объявление
# data = requests.post(f"{BASE_URL_ADV}", json={
#     "title": "Куплю",
#     "description": "Автомобиль",
#     "price": 100000.20,
#     "author": "Иванов"
#     },
#     headers={"checked-token": token1}
# )
# print(data.status_code)
# print(data.json())

# #Получаем нужное объявление
# data = requests.get(f"{BASE_URL_ADV}/1")
# print(data.status_code)
# print(data.json())

#Изменяем объявление
# data = requests.patch(f"{BASE_URL_ADV}/1", json={
#     "title": "Продам",
#     "description": "Новый автомобиль",
#     "price": 200000.20,
#     "author": "Иванов"
#     },
#     headers={"checked-token": token1}
# )
# print(data.status_code)
# print(data.json())

# # Ищем нужные объявления (заголовок+описание)
# search_query = "Куплю"
# data = requests.get(f"{BASE_URL_ADV}", params={"query_string": search_query})
# print(data.url)
# print(data.status_code)
# print(data.json())
#

