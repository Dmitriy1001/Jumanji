import logging
from datetime import date, datetime

from django.core.management.base import BaseCommand

from catalog import data
from catalog.models import Vacancy, Specialty, Company


logging.basicConfig(
    level=logging.INFO,
    filename='catalog/models.log',
    format='%(levelname)s: %(message)s',
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        current_datetime = datetime.today().strftime('%d-%b-%Y %H:%M:%S')
        with open('catalog/models.log', 'a') as log:
            log.write(f'{"-" * 21}\n{current_datetime}\n')
        self.add_speciality(data.specialties)
        self.add_company(data.companies)
        self.add_vacancy(data.jobs)

    def add_speciality(self, specialities):
        for speciality in specialities:
            if not Specialty.objects.filter(code=speciality['code']):
                new_specialty = Specialty.objects.create(
                    code=speciality['code'],
                    title=speciality['title'],
                    picture='https://place-hold.it/100x60',
                )
                logging.info(f'Specialty "{new_specialty}" added to database')
            else:
                logging.error(
                    f'Specialty with the code \"{speciality["code"]}\" already exists in database',
                )

    def add_company(self, companies):
        for company in companies:
            if not Company.objects.filter(name=company['title']):
                new_company = Company.objects.create(
                    name=company['title'],
                    location=company['location'],
                    logo='https://place-hold.it/100x60',
                    description=company['description'],
                    employee_count=int(company['employee_count']),
                )
                logging.info(f'Company "{new_company}" added to database')
            else:
                logging.error(f'Company with name \"{company["title"]}\" already exists in database')

    def add_vacancy(self, vacancies):
        for vacancy in vacancies:
            if not Vacancy.objects.select_related('company').select_related('specialty').filter(
                    title=vacancy['title'], published_at=self.make_date_obj(vacancy['posted']),
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
                    published_at=self.make_date_obj(vacancy['posted']),
                )
                logging.info(f'Vacancy "{new_vacancy}" added to database')
            else:
                logging.error(
                    (
                        f'Vacancy with title \"{vacancy["title"]}\" and date \"{vacancy["posted"]}\" '
                        f'already exists in database'
                    ),
                )

    def make_date_obj(self, published_date: str):
        year, month, day = map(int, published_date.split('-'))
        return date(year, month, day)
