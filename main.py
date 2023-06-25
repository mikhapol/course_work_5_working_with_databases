from src.DBManager import DBManager
from src.config import config
from src.functions import employers_info, all_vacancies, vacancies_with_higher_salary, search_vacancies_by_keyword, \
    create_database, get_employers_data, get_vacancies_data, save_employers_to_db, save_vacancies_to_db


def main():
    params = config()
    create_database('head_hunter_bd', params)
    dbmanager = DBManager(params)
    list_employers = get_employers_data()
    list_vacancies = get_vacancies_data()

    # сохраняем в бд данные по работодателям
    save_employers_to_db(list_employers, params)

    # сохраняем в бд данные по вакансиям
    save_vacancies_to_db(list_vacancies, params)

    print('Какую информацию необходимо получить из БД?')
    print("""Возможные варианты:
1 - Список работодателей и количество их вакансий
2 - Список всех вакансий
3 - Средняя зарплата по всем вакансиям
4 - Список вакансий за зарплатой выше средней
5 - Найти вакансии по ключевому слову
6 - Стоп
    """)
    while True:
        user_answer = input('Введите число: ')
        if user_answer == '1':
            employers_info(dbmanager)
        elif user_answer == '2':
            all_vacancies(dbmanager)
        elif user_answer == '3':
            print(f'Средняя зарплата по вакансиям: {dbmanager.get_avg_salary()} рублей в месяц')
        elif user_answer == '4':
            vacancies_with_higher_salary(dbmanager)
        elif user_answer == '5':
            search_vacancies_by_keyword(dbmanager)
        elif user_answer == '6':
            break
        else:
            print('Некорректный ввод')


if __name__ == '__main__':
    main()
