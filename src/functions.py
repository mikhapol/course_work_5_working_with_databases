import psycopg2
import requests


def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц для сохранения данных."""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employers (
                employer_id int PRIMARY KEY,
                employer_name varchar(100),
                hh_url varchar(100)
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_id int PRIMARY KEY,
                vacancy_name varchar(100),
                employer_id int REFERENCES employers(employer_id) ON DELETE CASCADE,
                salary_from int,
                salary_to int,
                city varchar(100),
                url varchar(100)
            )
        """)

    conn.commit()
    conn.close()


def get_employers_data() -> list:
    """Получаем с hh инфо по работодателям"""

    list_employers = []
    for i in range(30, 35):  # номера страниц выбраны рандомно
        params = {
            'area': 113,  # Поиск по России
            'page': i,
            'per_page': 100,  # максимум 100
            'only_with_vacancies': True,
        }
        response = requests.get('https://api.hh.ru/employers', params=params)
        employers_data = response.json()['items']

        for employer in employers_data:
            emp = {'employer_id': employer['id'],
                   'employer_name': employer['name'],
                   'url': employer['url']
                   }
            list_employers.append(emp)
    return list_employers


def get_vacancies_data() -> list:
    """Получаем инфо о вакансиях работодателей"""

    list_vacancies = []

    list_employers_id = []
    for item in get_employers_data():
        list_employers_id.append(item['employer_id'])

    for i in range(0, 20):
        params = {
            'area': 113,  # Поиск по России
            'page': i,
            'per_page': 100,  # максимум 100
            'employer_id': list_employers_id,
            'only_with_salary': True,  # только с зп
            'currency': 'RUR'
        }
        response = requests.get('https://api.hh.ru/vacancies', params=params)
        vacancies_data = response.json()['items']

        for vacancy in vacancies_data:

            if not vacancy['salary']['from']:
                salary_from = 0
            else:
                salary_from = vacancy['salary']['from']

            if not vacancy['salary']['to']:
                salary_to = 0
            else:
                salary_to = vacancy['salary']['to']

            vac = {'vacancy_id': vacancy['id'],
                   'vacancy_name': vacancy['name'],
                   'employer_id': vacancy['employer']['id'],
                   'salary_from': salary_from,
                   'salary_to': salary_to,
                   'city': vacancy['area']['name'],
                   'url': vacancy['alternate_url']
                   }
            list_vacancies.append(vac)
    return list_vacancies


def save_employers_to_db(list_employers: list, params: dict) -> None:
    """Записываем инфо по работодателям в БД"""

    conn = psycopg2.connect(dbname='head_hunter_bd', **params)
    with conn:
        with conn.cursor() as cur:
            for employer in list_employers:
                cur.execute('insert into employers values (%s, %s, %s)', (
                    employer['employer_id'],
                    employer['employer_name'],
                    employer['url']

                ))
    conn.close()


def save_vacancies_to_db(list_vacancies: list, params: dict) -> None:
    """Записываем инфо по вакансиям в БД"""

    conn = psycopg2.connect(dbname='head_hunter_bd', **params)
    with conn:
        with conn.cursor() as cur:
            for vacancy in list_vacancies:
                cur.execute('insert into vacancies values (%s, %s, %s, %s, %s, %s, %s)', (
                    vacancy['vacancy_id'],
                    vacancy['vacancy_name'],
                    vacancy['employer_id'],
                    vacancy['salary_from'],
                    vacancy['salary_to'],
                    vacancy['city'],
                    vacancy['url']
                ))
    conn.close()


def employers_info(dbmanager):
    """Выводит работодателей и количество вакансий"""

    employers = dbmanager.get_companies_and_vacancies_count()
    for item in employers:
        print(item)


def all_vacancies(dbmanager):
    """Выводит все вакансии"""

    vacancies = dbmanager.get_all_vacancies()
    for item in vacancies:
        print(item)


def vacancies_with_higher_salary(dbmanager):
    """Выводит все вакансии с ЗП выше средней"""

    vacancies_with_higher_avg_salary = dbmanager.get_vacancies_with_higher_salary()
    for item in vacancies_with_higher_avg_salary:
        print(item)


def search_vacancies_by_keyword(dbmanager):
    """Выводит вакансии с ключевым словом"""

    keyword = input('Введите ключевое слово для поиска вакансий\n')
    filtered_vacancies = dbmanager.get_vacancies_with_keyword(keyword)
    for item in filtered_vacancies:
        print(item)
