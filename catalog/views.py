from django.http import Http404
from django.shortcuts import render
from .models import Vacancy, Specialty, Company

from . import utils


def index(request):
    context = {
        'specialties': utils.add_vacancies_number(Specialty.objects.all()),
        'companies': utils.add_vacancies_number(Company.objects.all())
    }
    return render(request, 'catalog/index.html', context)


def vacancies_list(request):
    vacancies = Vacancy.objects.all()
    context = {
        'vacancies_category': 'Все вакансии',
        'vacancies_count': utils.make_correct_ending(vacancies.count(), 'vacancies'),
        'vacancies': vacancies,
    }
    return render(request, 'catalog/vacancies_list.html', context)


def specialty_vacancies_list(request, specialty_code):
    try:
        specialty = Specialty.objects.get(code=specialty_code)
    except Specialty.DoesNotExist:
        raise Http404
    vacancies = specialty.vacancies.all()
    context = {
        'vacancies_category': specialty.title,
        'vacancies_count': utils.make_correct_ending(vacancies.count(), 'vacancies'),
        'vacancies': vacancies,
    }
    return render(request, 'catalog/vacancies_list.html', context)


def company_detail(request, company_id):
    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        raise Http404
    vacancies = company.vacancies.all()
    context = {
        'company': company,
        'vacancies_count': utils.make_correct_ending(vacancies.count(), 'vacancies'),
        'vacancies': vacancies,
    }
    return render(request, 'catalog/company_detail.html', context)


def vacancy_detail(request, vacancy_id):
    try:
        vacancy = Vacancy.objects.get(id=vacancy_id)
    except Vacancy.DoesNotExist:
        raise Http404
    context = {
        'vacancy': vacancy,
        'employee_count': utils.make_correct_ending(vacancy.company.employee_count, 'people')
    }
    return render(request, 'catalog/vacancy_detail.html', context)
