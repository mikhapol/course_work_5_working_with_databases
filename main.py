from src.DBManager import DBManager
from src.config import config
from src.functions import get_request, save_vacancies_to_db, parsing_vacancies


def main():
    # Получение вакансий
    hh_vacancies = parsing_vacancies(get_request('Python'))

    params = config()
    save_vacancies_to_db('hh_bd', hh_vacancies, params)

    dbanager = DBManager('hh_bd', params)

    print('Привет, что будем выводить?')
    print("""
1 - Список всех компаний и количество вакансий у каждой компании
2 - Список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
3 - Среднюю зарплату по вакансиям
4 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям
5 - Список всех вакансий, в названии которых содержатся переданные в метод 
    """)
    while True:
        user_answer = input('Введи число: ')

        if user_answer == '1':
            emp_info = dbanager.get_companies_and_vacancies_count()
            for i in emp_info:
                print(i)

        elif user_answer == '2':
            all_vac = dbanager.get_all_vacancies()
            for i in all_vac:
                print(i)

        elif user_answer == '3':
            print(f"Средняя зарплата по вакансии: {dbanager.get_avg_salary()}")

        elif user_answer == '4':
            vac = dbanager.get_vacancies_with_higher_salary()
            for item in vac:
                print(item)

        elif user_answer == '5':
            keyword = input('Введите ключевое слово: ')
            vac = dbanager.get_vacancies_with_keyword(keyword)
            for item in vac:
                print(item)
        else:
            print("Такого варианта нет")

        print("Продолжить работу?")
        answer = input("Y/N")
        if answer == 'N':
            print("Пока")
            break


if __name__ == '__main__':
    main()
