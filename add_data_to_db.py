import logging
import os
from datetime import date, datetime

import django

# Эти строки  нужно прописать до импорта из приложения,
# иначе бросает django.core.exceptions.ImproperlyConfigured
env = os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jumanji.settings')
django.setup()
if env:
    # Такая конструкция нужна, чтобы flake не ругался, что импорты не наверху
    from catalog import data
    from catalog.models import Vacancy, Company, Specialty


#  ПОРЯДОК ДЕЙСТВИЙ:
# 1. Копируем данные в catalog/data.py
# 2. Выполняем python add_data_to_db.py
# 3. Смотрим логи в models.log


logging.basicConfig(
    level=logging.INFO,
    filename='models.log',
    format='%(levelname)s: %(message)s',
)


def make_date_obj(published_date: str):
    year, month, day = map(int, published_date.split('-'))
    return date(year, month, day)


def add_vacancy(vacancies):
    for vacancy in vacancies:
        if not Vacancy.objects.select_related('company').select_related('specialty').filter(
                title=vacancy['title'], published_at=make_date_obj(vacancy['posted']),
        ):
            new_vacancy = Vacancy.objects.create(
                title=vacancy['title'],
                specialty=Specialty.objects.get(code=vacancy['specialty']),
                company=Company.objects.get(
                    name=list(
                        filter(lambda company: company['id'] == vacancy['company'], data.companies),
                    )[0]['title'],
                ),  # В data.py id у компаний зафиксированы, но в реальности они могут поменяться,
                    # например, если компания будет удалена, а потом снова добавлена в бд,
                    # поэтому здесь лучше брать по имени, которое уникально(unique=True)
                skills=vacancy['skills'],
                description=vacancy['description'],
                salary_min=int(vacancy['salary_from']),
                salary_max=int(vacancy['salary_to']),
                published_at=make_date_obj(vacancy['posted']),
            )
            logging.info(f'Vacancy "{new_vacancy}" added to database')
        else:
            logging.error(
                f'Job with title \"{vacancy["title"]}\" and date \"{vacancy["posted"]}\" already exists in database',
            )


def add_company(companies):
    for company in companies:
        if not Company.objects.filter(name=company['title']):
            new_company = Company.objects.create(
                name=company['title'],
                location=company['location'],
                logo='https://place-hold.it/100x60',
                description=company['description'],
                employee_count=int(company['employee_count']),
            )
            logging.info(f'Company "{new_company}" added to the database')
        else:
            logging.error(f'There is already a company named \"{company["title"]}\" in database')


def add_speciality(specialities):
    for speciality in specialities:
        if not Specialty.objects.filter(code=speciality['code']):
            new_specialty = Specialty.objects.create(
                code=speciality['code'],
                title=speciality['title'],
                picture='https://place-hold.it/100x60',
            )
            logging.info(f'Specialty "{new_specialty}" added to the database')
        else:
            logging.error(f'There is already a specialization in the database with the code \"{speciality["code"]}\"')


def main():
    current_datetime = datetime.today().strftime('%d-%b-%Y %H:%M:%S')
    with open('models.log', 'a') as log:
        log.write(f'{"-"*21}\n{current_datetime}\n')
    add_speciality(data.specialties)
    add_company(data.companies)
    add_vacancy(data.jobs)


if __name__ == '__main__':
    main()
