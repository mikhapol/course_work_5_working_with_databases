from src.DBManager import DBManager
from src.config import config
from src.functions import get_request, save_vacancies_to_db, parsing_vacancies, create_database


def main():
    keyword = 'Python'
    database_name = 'hh_bd'
    params = config()

    # Получение вакансий по keyword.
    hh_vacancies = parsing_vacancies(get_request(keyword))

    # Создание БД database_name с таблицей и колонами.
    create_database(database_name, params)

    # Сохранение полученных вакансий в БД.
    save_vacancies_to_db(database_name, hh_vacancies, params)

    dbmanager = DBManager(database_name, params)

    print('Приветствую, выберите действие.')

    while True:

        print("""
        1 - Список employer и количество vacancies.
        2 - Список vacancies с указанием названия employer, vacancies, salary и URL на вакансию.
        3 - Средняя ЗП
        4 - Список vacancies, у которых salary выше средней.
        5 - Найти вакансии по ключевому слову.
            """)
        user_answer = input('Ваш выбор: ')

        if user_answer == '1':
            emp_info = dbmanager.get_companies_and_vacancies_count()
            for i in emp_info:
                print(i)

        elif user_answer == '2':
            all_vac = dbmanager.get_all_vacancies()
            for i in all_vac:
                print(i)

        elif user_answer == '3':
            print(f"Средняя ЗП: {dbmanager.get_avg_salary()}")

        elif user_answer == '4':
            vac = dbmanager.get_vacancies_with_higher_salary()
            for item in vac:
                print(item)

        elif user_answer == '5':
            keyword = input('Введите ключевое слово: ')
            vac = dbmanager.get_vacancies_with_keyword(keyword)
            for item in vac:
                print(item)
        else:
            print("Такого варианта нет")

        print("Продолжить?")
        answer = input("Y/N: ").upper()
        if answer == 'N':
            print("!!Пока!!")
            break


if __name__ == '__main__':
    main()
