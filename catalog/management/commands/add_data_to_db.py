import logging
import logging.config
from datetime import datetime

import pytz
from django.core.management.base import BaseCommand

from catalog import data
from catalog.models import Vacancy, Specialty, Company


custom_logger = logging.getLogger('add_data_logger')


class Command(BaseCommand):
    def handle(self, *args, **options):
        current_datetime = datetime.today().strftime('%d-%b-%Y %H:%M:%S')
        with open('catalog/management/add_data_to_db.log', 'a') as log:
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
                custom_logger.info(f'Specialty "{new_specialty}" added to database')
            else:
                custom_logger.error(
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
                custom_logger.info(f'Company "{new_company}" added to database')
            else:
                custom_logger.error(f'Company with name \"{company["title"]}\" already exists in database')

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
                    ),  # ?? data.py id ?? ???????????????? ??????????????????????????, ???? ?? ???????????????????? ?????? ?????????? ????????????????????,
                        # ????????????????, ???????? ???????????????? ?????????? ??????????????, ?? ?????????? ?????????? ?????????????????? ?? ????,
                        # ?????????????? ?????????? ?????????? ?????????? ???? ??????????, ?????????????? ??????????????????(unique=True)
                    skills=vacancy['skills'],
                    description=vacancy['description'],
                    salary_min=int(vacancy['salary_from']),
                    salary_max=int(vacancy['salary_to']),
                    published_at=self.make_date_obj(vacancy['posted']),
                )
                custom_logger.info(f'Vacancy "{new_vacancy}" added to database')
            else:
                custom_logger.error(
                    (
                        f'Vacancy with title \"{vacancy["title"]}\" and date \"{vacancy["posted"]}\" '
                        f'already exists in database'
                    ),
                )

    def make_datetime_obj(self, published_at: str):
        year, month, day = map(int, published_at.split('-'))
        return datetime(year, month, day, tzinfo=pytz.timezone('Europe/Moscow'))


logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s',
        },
        'file': {
            'format': '%(name)-12s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': 'catalog/management/add_data_to_db.log',
        },
    },
    'loggers': {
        'add_data_logger': {
            'level': 'INFO',
            'handlers': ['console', 'file'],
            'propagate': True,
        },
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['file'],
        },
    },
})
