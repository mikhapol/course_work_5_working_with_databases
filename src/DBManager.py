import psycopg2


class DBManager:
    def __init__(self, params):
        self.params = params

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """Получает список всех компаний и количество вакансий у каждой компании"""

        conn = psycopg2.connect(dbname='head_hunter_bd', **self.params)

        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT employer_name, COUNT(*) AS qty_vacancies FROM vacancies
                    JOIN employers USING(employer_id)
                    GROUP BY employer_name
                    ORDER BY qty_vacancies DESC
                    """
                )
                result = cur.fetchall()
        conn.close()
        return result

    def get_all_vacancies(self):
        """Получает список всех вакансий (название вакансии, название компании, зп, ссылка)"""

        conn = psycopg2.connect(dbname='head_hunter_bd', **self.params)

        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT vacancy_name, employer_name, (salary_from + salary_to) / 2 AS salary, url 
                    FROM vacancies
                    JOIN employers USING(employer_id)
                    ORDER BY salary DESC
                    """
                )
                result = cur.fetchall()
        conn.close()
        return result

    def get_avg_salary(self) -> int:
        """Получает среднюю зарплату по вакансиям"""

        conn = psycopg2.connect(dbname='head_hunter_bd', **self.params)

        with conn:
            with conn.cursor() as cur:
                cur.execute('SELECT AVG((salary_from + salary_to)/2) FROM vacancies')
                result = cur.fetchone()
        conn.close()
        return round(int(result[0]))

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зп выше средней по всем вакансиям"""

        conn = psycopg2.connect(dbname='head_hunter_bd', **self.params)

        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT vacancy_name, (salary_from + salary_to) / 2 AS salary, url 
                    FROM vacancies
                    WHERE (salary_from + salary_to) / 2 > {self.get_avg_salary()}
                    ORDER BY salary DESC
                    """
                )
                result = cur.fetchall()
        conn.close()
        return result

    def get_vacancies_with_keyword(self, keyword: str):
        """Получает список всех вакансий, в названии которых содержится ключевое слово"""

        conn = psycopg2.connect(dbname='head_hunter_bd', **self.params)

        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT vacancy_name, salary_from, salary_to, url FROM vacancies 
                    WHERE vacancy_name LIKE '%{keyword}%'
                    """
                )
                result = cur.fetchall()
        conn.close()
        return result
