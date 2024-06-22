import requests
import json
from abc import ABC, abstractmethod


class Engine(ABC):
    """Класс шаблон"""

    @abstractmethod
    def get_request(self):
        pass


class HH(Engine):
    """Класс парсера данных с сайта hh.ru"""
    vacancies_all = []
    vacancies_dicts = []

    def __init__(self, vacancy, num_of_vacancy=20):
        self.vacancy = vacancy
        self.num_of_vacancy = num_of_vacancy

    def get_request(self):
        """Метод получения данных с сайта hh.ru. Реализована проверка url и если она прошла успешно
        метод сохраняет вакансии в словарь vacancy_dict и возвращает его"""
        for num in range(1):
            url = 'https://api.hh.ru/vacancies'
            params = {
                'text': self.vacancy,
                'areas': 113,
                'per_page': self.num_of_vacancy,
                'page': num,
                'only with salary': True
            }
            response = requests.get(url, params=params)
            info = response.json()
            if info is None:
                return "Данны не получены!"
            elif 'errors' in info:
                return info['errors'][0]['value']
            elif info['found'] == 0:
                return "Нет вакансий"
            else:
                for vacancy in range(self.num_of_vacancy):
                    self.vacancies_all.append(vacancy)
                    if info['items'][vacancy]['salary'] is not None \
                            and info['items'][vacancy]['salary']['currency'] == 'RUR':
                        vacancy_dict = {'employer': info['items'][vacancy]['employer']['name'],
                                        'name': info['items'][vacancy]['name'],
                                        'url': info['items'][vacancy]['alternate_url'],
                                        'requirement': info['items'][vacancy]['snippet']['requirement'],
                                        'salary_from': info['items'][vacancy]['salary']['from'],
                                        'salary_to': info['items'][vacancy]['salary']['to']}
                        if vacancy_dict['salary_from'] is None:
                            vacancy_dict['salary_from'] = "не указано"
                        elif vacancy_dict['salary_to'] is None:
                            vacancy_dict['salary_to'] = "не указано"
                        self.vacancies_dicts.append(vacancy_dict)
        return self.vacancies_dicts

    @staticmethod
    def make_json(filename, vacancies_dicts):
        """Метод принимает имя файла и словарь полученных вакансий. Редактирует в читабельный вид
        и записывает их в файл формата .json. Возвращает список вакансий"""
        vacancies_list = []
        for vacancy in vacancies_dicts:
            vacancies_list.append(f"""
        Наниматель: {vacancy['employer']}
        Вакансия: {vacancy['name']}
        Описание/Требования: {vacancy['requirement']}
        Заработная плата от {vacancy['salary_from']} до {vacancy['salary_to']}
        Ссылка на вакансию: {vacancy['url']}""")
        with open(f"{filename}_hh_ru.json", 'w', encoding='utf-8') as file:
            json.dump(vacancies_dicts, file, indent=2, ensure_ascii=False)
        return vacancies_list

    @staticmethod
    def sorting(filename, type_of_sort, vacancies: dict, num_of_vacancies=None):
        """Метод принимает имя файла, тип сортировки, словарь вакансий и кол-во вакансий(по желанию).
        Метод сортирует вакансии по выбранному типу сортировки, редактирует их в читабельный вид и записывает в файл
        формата .json. Возвращает список вакансий"""
        count = 0
        vacancies_list = []
        vacancies_sort = sorted(vacancies, key=lambda vacancy: vacancy['salary_from'], reverse=type_of_sort)
        if num_of_vacancies:
            for vacancy in vacancies_sort:
                vacancies_list.append(f"""
            Наниматель: {vacancy['employer']}
            Вакансия: {vacancy['name']}
            Описание/Требования: {vacancy['requirement']}
            Заработная плата от {vacancy['salary_from']} до {vacancy['salary_to']}
            Ссылка на вакансию: {vacancy['url']}""")
                count += 1
                if count == num_of_vacancies:
                    break
        with open(f'{filename}_sorted_vacancies.json', 'w', encoding='utf-8') as file:
            json.dump(vacancies_sort, file, indent=2, ensure_ascii=False)
        return vacancies_list


"""Пример работы"""
# vacancy_to_search = "маляр"
# hh = HH(vacancy_to_search)
# my_vacancies = hh.get_request()
# print(hh.make_json(vacancy_to_search, my_vacancies))
# sorted_vacancies = hh.sorting(vacancy_to_search, True, my_vacancies)
# for vacancy in sorted_vacancies:
#     print(vacancy)
