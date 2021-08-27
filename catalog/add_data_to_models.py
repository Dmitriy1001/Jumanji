import time
from datetime import date

from . import data
from .models import Vacancy, Company, Specialty


def make_date_obj(published_date: str):
    year, month, day = map(int, published_date.split('-'))
    return date(year, month, day)


def add_vacancy(vacancies):
    for vacancy in vacancies:
        new_vacancy = Vacancy.objects.create(
            title=vacancy['title'],
            specialty=Specialty.objects.get(code=vacancy['specialty']),
            company=Company.objects.get(id=vacancy['company']),
            skills=vacancy['skills'].replace(', ', ' • '),
            description=vacancy['description'],
            salary_min=int(vacancy['salary_from']),
            salary_max=int(vacancy['salary_to']),
            published_at=make_date_obj(vacancy['posted'])
        )
        print(f'Vacancy "{new_vacancy}" added to the database')
        time.sleep(1)


def add_company(companies):
    for company in companies:
        if not Company.objects.filter(name=company['title']):
            new_company = Company.objects.create(
                name=company['title'],
                location=company['location'],
                logo='https://place-hold.it/100x60',
                description=company['description'],
                employee_count=int(company['employee_count'])
            )
            print(f'Company "{new_company}" added to the database')
        else:
            print(f'There is already a company named \"{company["title"]}\" in the database')
        time.sleep(1)


def add_speciality(specialities):
    for speciality in specialities:
        if not Specialty.objects.filter(code=speciality['code']):
            new_specialty = Specialty.objects.create(
                code=speciality['code'],
                title=speciality['title'],
                picture='https://place-hold.it/100x60',
            )
            print(f'Specialty "{new_specialty}" added to the database')
        else:
            print(f'There is already a specialization in the database with the code \"{speciality["code"]}\"')
        time.sleep(1)


def main():
    print('-------\nAdding specialties')
    add_speciality(data.specialties)
    print('-------\nAdding companies')
    add_company(data.companies)
    print('-------\nAdding vacancies')
    add_vacancy(data.jobs)
    print('-------')


if __name__ == '__main__':
    main()