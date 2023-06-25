-- Создание БД, если она уже создана, тогда удалить её и создать заново.

DROP DATABASE IF EXISTS head_hunter_bd;
CREATE DATABASE head_hunter_bd

-- Создаем таблицу по работодателям
--создаем таблицу по вакансиям

CREATE TABLE IF NOT EXISTS vacancies
(
vacancy_id int PRIMARY KEY,
vacancy_name varchar(100),
employer_id int,
salary_from int,
salary_to int,
city varchar(100),
url varchar(100)
);



