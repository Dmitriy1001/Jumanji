from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView, UpdateView, ListView, DetailView
from django.utils.decorators import method_decorator

from .forms import ApplicationForm, CompanyForm, VacancyForm
from .models import Vacancy, Specialty, Company
from .decorators import has_not_company, has_company


# JOB SEEKER


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
    return render(request, 'catalog/job_seeker/vacancies_list.html', context)


def specialty_vacancies_list(request, specialty_code):
    try:
        specialty = Specialty.objects.get(code=specialty_code)
    except Specialty.DoesNotExist:
        raise Http404('Рубрика не найдена')
    context = {
        'vacancies_category': specialty.title,
        'vacancies': specialty.vacancies.select_related('specialty').select_related('company'),
    }
    return render(request, 'catalog/job_seeker/vacancies_list.html', context)


def company_detail(request, company_id):
    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        raise Http404('Компания не найдена')
    context = {
        'company': company,
        'vacancies': company.vacancies.select_related('specialty').select_related('company'),
    }
    return render(request, 'catalog/job_seeker/company_detail.html', context)


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
            messages.success(request, f'Отклик на вакансию "{vacancy_id}" отправлен')
            return redirect('vacancy_send', vacancy_id)
    else:
        form = ApplicationForm()
    return render(request, 'catalog/job_seeker/vacancy_detail.html', {'vacancy': vacancy, 'form': form})


@login_required
def vacancy_send(request, vacancy_id):
    msg = f'Отклик на вакансию "{vacancy_id}" отправлен'
    if msg not in [msg.message for msg in request._messages]:
        return redirect('vacancy_detail', vacancy_id)
    return render(request, 'catalog/job_seeker/vacancy_send.html', {'vacancy_id': vacancy_id})


# EMPLOYER


class MyCompanyLetsstart(LoginRequiredMixin, TemplateView):
    template_name = 'catalog/employer/mycompany_letsstart.html'

    # класс отрабатывает только, если у юзера еще нет компании(кастомный декоратор)
    # в следующих классах dispatch прописан в одну строчку, лямбда функцией
    @has_not_company
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class MyCompanyCreate(LoginRequiredMixin, CreateView):
    form_class = CompanyForm
    template_name = 'catalog/employer/mycompany_create.html'
    extra_context = {'page': 'company'}
    dispatch = has_not_company(lambda self, *args, **kwargs: super().dispatch(*args, **kwargs))

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            new_company = form.save(commit=False)
            new_company.owner = request.user
            new_company.save()
            messages.success(request, 'Компания создана')
            return redirect('mycompany')


class MyCompany(LoginRequiredMixin, UpdateView):
    form_class = CompanyForm
    template_name = 'catalog/employer/mycompany.html'
    dispatch = has_company(lambda self, *args, **kwargs: super().dispatch(*args, **kwargs))

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user.company)
        msgs = [msg.message for msg in request._messages]
        msg = msgs[0] if msgs else ''
        return render(request, self.template_name, {'form': form, 'msg': msg, 'page': 'company'})

    def post(self, request, *args, **kwargs):
        company = request.user.company
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Информация о компании обновлена')
            return redirect('mycompany')


class MyCompanyVacancies(LoginRequiredMixin, ListView):
    model = Vacancy
    template_name = 'catalog/employer/mycompany_vacancies.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        return (
                Vacancy.objects.filter(company__owner=self.request.user)
                .annotate(applications_count=Count('applications'))
                .select_related('specialty', 'company')
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['company'] = self.request.user.company
        except User.company.RelatedObjectDoesNotExist:
            context['company'] = None
        context['page'] = 'vacancies'
        return context


class MyCompanyVacancyCreate(LoginRequiredMixin, CreateView):
    form_class = VacancyForm
    template_name = 'catalog/employer/mycompany_vacancies_create.html'
    extra_context = {'page': 'vacancies'}
    dispatch = has_company(lambda self, *args, **kwargs: super().dispatch(*args, **kwargs))

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.company = request.user.company
            vacancy.published_at = date.today()
            vacancy.save()
            messages.success(request, 'Вакансия создана')
            return redirect('mycompany_vacancy_detail', vacancy.id)


class MyCompanyVacancyDetail(LoginRequiredMixin, DetailView):
    model = Vacancy
    pk_url_kwarg = 'vacancy_id'
    form_class = VacancyForm
    template_name = 'catalog/employer/mycompany_vacancy_detail.html'

    def dispatch(self, *args, **kwargs):
        # такая фильтрация нужна для того, чтобы нельзя было редактировать вакансии чужой компании
        try:
            kwargs['vacancy'] = (
                Vacancy.objects.filter(id=kwargs['vacancy_id'], company__owner=self.request.user)
                .select_related('specialty')
                .annotate(applications_count=Count('applications'))
                .prefetch_related('applications')
            )[0]
        except IndexError:
            raise Http404('Вакансия не найдена')
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=kwargs['vacancy'])
        msgs = [msg.message for msg in request._messages]
        msg = msgs[0] if msgs else ''
        context = {
            'form': form,
            'vacancy': kwargs['vacancy'],
            'msg': msg,
            'page': 'vacancies',
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=kwargs['vacancy'])
        if form.is_valid():
            form.save()
            messages.success(request, 'Информация о вакансии обновлена')
            return redirect('mycompany_vacancy_detail', kwargs['vacancy_id'])
        return render(request, self.template_name, {'form': form, 'vacancy': kwargs['vacancy']})



