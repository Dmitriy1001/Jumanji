from django.db.models import Count
from django.http import Http404
from django.shortcuts import render

from .models import Vacancy, Specialty, Company


def index(request):
    context = {
        'specialties': Specialty.objects.annotate(vacancies_count=Count('vacancies')),
        'companies': Company.objects.annotate(vacancies_count=Count('vacancies')),
    }
    return render(request, 'catalog/index.html', context)


def vacancies_list(request):
    context = {
        'vacancies_category': 'Все вакансии',
        'vacancies': Vacancy.objects.select_related('company').select_related('specialty'),
    }
    return render(request, 'catalog/vacancies_list.html', context)


def specialty_vacancies_list(request, specialty_code):
    try:
        specialty = Specialty.objects.get(code=specialty_code)
    except Specialty.DoesNotExist:
        raise Http404('Рубрика не найдена')
    context = {
        'vacancies_category': specialty.title,
        'vacancies': specialty.vacancies.select_related('specialty').select_related('company'),
    }
    return render(request, 'catalog/vacancies_list.html', context)


def company_detail(request, company_id):
    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        raise Http404('Компания не найдена')
    context = {
        'company': company,
        'vacancies': company.vacancies.select_related('specialty').select_related('company'),
    }
    return render(request, 'catalog/company_detail.html', context)


def vacancy_detail(request, vacancy_id):
    try:
        vacancy = (
            Vacancy.objects.select_related('specialty').select_related('company').get(id=vacancy_id)
        )
    except Vacancy.DoesNotExist:
        raise Http404('Вакансия не найдена')
    return render(request, 'catalog/vacancy_detail.html', {'vacancy': vacancy})
