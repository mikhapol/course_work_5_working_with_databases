--Удаляем БД если она существует и создаем заново

DROP DATABASE IF EXISTS head_hunter_bd;
CREATE DATABASE head_hunter_bd

--создаем таблицу по работодателям

CREATE TABLE IF NOT EXISTS employers
(
employer_id int PRIMARY KEY,
employer_name varchar(100),
hh_url varchar(100)
);

--создаем таблицу по вакансиям

CREATE TABLE IF NOT EXISTS vacancies
(
vacancy_id int PRIMARY KEY,
vacancy_name varchar(100),
employer_id int REFERENCES employers(employer_id) ON DELETE CASCADE,
salary_from int,
salary_to int,
city varchar(100),
url varchar(100)
);