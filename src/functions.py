import psycopg2
import requests


def get_request(keyword, page=0):
    response = requests.get("https://api.hh.ru/vacancies", params={"text": keyword, "page": page, "per_page": 1})
    return response.json()['items']


def get_salary(vac):
    salary = [0, 0]
    if vac['salary'] and vac['salary']['from']:
        salary[0] = vac['salary']['from']

    if vac['salary'] and vac['salary']['to']:
        salary[1] = vac['salary']['to']
    return salary


def parsing_vacancies(api_response):
    vacancies = []
    for vac in api_response:
        salary_from, salary_to = get_salary(vac)
        vacancy = {'vacancy_id': vac['id'],
                   'vacancy_name': vac['name'],
                   'employer_id': vac['employer']['id'],
                   'salary_from': salary_from,
                   'salary_to': salary_to,
                   'city': vac['area']['name'],
                   'url': vac['alternate_url']
                   }
        vacancies.append(vacancy)
    return vacancies


def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц для сохранения данных."""

    conn = psycopg2.connect(database='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(database=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_id int PRIMARY KEY,
                vacancy_name varchar(200),
                employer_id int,
                salary_from int,
                salary_to int,
                city varchar(100),
                url varchar(100)
            )
        """)

    conn.commit()
    conn.close()


def save_vacancies_to_db(database_name: str, list_vacancies: list, params: dict) -> None:
    """Записываем инфо по вакансиям в БД"""

    conn = psycopg2.connect(database=database_name, **params)
    with conn:
        with conn.cursor() as cur:
            for vacancy in list_vacancies:
                cur.execute('INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (
                    vacancy['vacancy_id'],
                    vacancy['vacancy_name'],
                    vacancy['vacancy_city'],
                    vacancy['vacancy_url'],
                    vacancy['salary_from'],
                    vacancy['salary_to'],
                    vacancy['employer_name'],
                    vacancy['employer_id']
                ))
            conn.close()
