from django.db.models import Count
from django.http import Http404
from django.shortcuts import render

from . import utils
from .models import Vacancy, Specialty, Company


def index(request):
    specialties = Specialty.objects.annotate(vacancies_count=Count('vacancies'))
    companies = Company.objects.annotate(vacancies_count=Count('vacancies'))
    for specialty in specialties:
        specialty.vacancies_count = utils.make_correct_ending(specialty.vacancies_count, 'vacancies')
    for company in companies:
        company.vacancies_count = utils.make_correct_ending(company.vacancies_count, 'vacancies')

    context = {'specialties': specialties, 'companies': companies}
    return render(request, 'catalog/index.html', context)


def vacancies_list(request):
    vacancies = Vacancy.objects.all().select_related('company').select_related('specialty')
    context = {
        'vacancies_category': 'Все вакансии',
        'vacancies_count': utils.make_correct_ending(len(vacancies), 'vacancies'),
        'vacancies': vacancies,
    }
    return render(request, 'catalog/vacancies_list.html', context)


def specialty_vacancies_list(request, specialty_code):
    try:
        specialty = Specialty.objects.get(code=specialty_code)
    except Specialty.DoesNotExist:
        raise Http404
    vacancies = specialty.vacancies.all().select_related('specialty').select_related('company')
    context = {
        'vacancies_category': specialty.title,
        'vacancies_count': utils.make_correct_ending(len(vacancies), 'vacancies'),
        'vacancies': vacancies,
    }
    return render(request, 'catalog/vacancies_list.html', context)


def company_detail(request, company_id):
    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        raise Http404
    vacancies = company.vacancies.all().select_related('specialty').select_related('company')
    context = {
        'company': company,
        'vacancies_count': utils.make_correct_ending(len(vacancies), 'vacancies'),
        'vacancies': vacancies,
    }
    return render(request, 'catalog/company_detail.html', context)


def vacancy_detail(request, vacancy_id):
    # try:
    #     vacancy = Vacancy.objects.get(id=vacancy_id)
    # except Vacancy.DoesNotExist:
    #     raise Http404

    vacancy = (
        Vacancy.objects.filter(id=vacancy_id).select_related('specialty').select_related('company')
    ) # так на два запроса в бд меньше
    try:
        vacancy = vacancy[0]
    except Vacancy.DoesNotExist:
        raise Http404
    context = {
        'vacancy': vacancy,
        'employee_count': utils.make_correct_ending(vacancy.company.employee_count, 'people')
    }
    return render(request, 'catalog/vacancy_detail.html', context)
