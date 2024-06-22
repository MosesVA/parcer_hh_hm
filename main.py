from classes.engine import HH

"""В этом файле вам необходимо реализовать интерфейс взаимодействия с парсером через консоль
А именно
- 1 предложить пользователю выбрать вакансию для поиска;
- 2 спросить сколько вакансий просмотреть от 20 до 200 c шагом 20 вакансий 
(понадобится дополнительный параметр в __init__) который потом надо будет реализовать в теле метода get_request();
- 3 спросить нужна ли сортировка по зарплате;
- 4 спросить сколько отсортированных вакансий вывести;
- 5 добавить докстринги в файле engine.py;
- 6 (дополнительно) добавить возможные исключения.

Для того чтобы это все работало
вам будет необходимо несколько модифицировать код который находится в пакете classes внутри файла engine.py
"""

user_vacancy_to_search = input('Введите название вакансии для поиска: ')
user_num_of_search = int(input('Сколько вакансий просмотреть?(от 20 до 200 с шагом 20): '))
user_sort = input('Нужна ли сортировка по зарплате?(да/нет): ')

if user_num_of_search % 20 == 0 and 200 >= user_num_of_search > 0:
    hh = HH(user_vacancy_to_search, user_num_of_search)
else:
    hh = HH(user_vacancy_to_search)

if user_sort == 'да':
    user_num_of_sort_vacancy = int(input('Сколько вывести отсортированных вакансий?: '))
    sorted_vacancies = hh.sorting(user_vacancy_to_search, True, hh.get_request(), user_num_of_sort_vacancy)
    for vacancy in sorted_vacancies:
        print(vacancy)
else:
    vacancies = hh.make_json(user_vacancy_to_search, hh.get_request())
    for vacancy in vacancies:
        print(vacancy)
