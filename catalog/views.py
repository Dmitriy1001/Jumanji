from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, redirect

from .forms import ApplicationForm, CompanyForm
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
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.vacancy = vacancy
            application.user = request.user
            application.save()
            return redirect('vacancy_send', vacancy_id)
    else:
        form = ApplicationForm()
    return render(request, 'catalog/vacancy_detail.html', {'vacancy': vacancy, 'form': form})


def vacancy_send(request, vacancy_id):
    return render(request, 'catalog/vacancy_send.html', {'vacancy_id': vacancy_id})


# def mycompany_letsstart(request):
#     return render(request, 'catalog/mycompany_letsstart.html')
#
#
# def mycompany_create(request):
#     return render(request, 'catalog/mycompany_create.html')
#
#
# def mycompany(request):
#     try:
#         company = request.user.company
#         form = CompanyForm(instance=company)
#         return render(request, 'catalog/mycompany.html', {'company': company, 'form': form})
#     except Company.DoesNotExist:
#         return render(request, 'catalog/mycompany_letsstart.html')
#
#
# def my_vacancies(request):
#     return render(request, 'catalog/my_vacancies.html')
#
#
# def my_vacancies_create(request):
#     return render(request, 'catalog/my_vacancies_create.html')
#
#
# def my_vacancy_detail(request, vacancy_id):
#     return render(request, 'catalog/my_vacancy_detail.html')




