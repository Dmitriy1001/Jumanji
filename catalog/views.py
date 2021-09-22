from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView, UpdateView, ListView, DetailView

from .mixins import HasCompanyMixin, HasNotCompanyMixin
from .forms import ApplicationForm, CompanyForm, VacancyForm
from .models import Vacancy, Specialty, Company


# JOB SEEKER


class Index(TemplateView):
    template_name = 'catalog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specialties'] = Specialty.objects.annotate(vacancies_count=Count('vacancies'))
        context['companies'] = Company.objects.annotate(vacancies_count=Count('vacancies'))
        return context


class VacancyList(ListView):
    queryset = Vacancy.objects.select_related('company', 'specialty')
    context_object_name = 'vacancies'
    template_name = 'catalog/job_seeker/vacancies_list.html'
    extra_context = {'vacancies_category': 'Все вакансии'}


class SpecialtyVacancyList(VacancyList):
    def get_queryset(self):
        try:
            self.kwargs['specialty'] = (
                Specialty.objects.get(code=self.kwargs['specialty_code'])
            )
        except Specialty.DoesNotExist:
            raise Http404('Рубрика не найдена')
        return self.kwargs['specialty'].vacancies.select_related('specialty', 'company')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancies_category'] = self.kwargs['specialty'].title
        return context


class CompanyVacancyList(VacancyList):
    def get_queryset(self):
        try:
            self.kwargs['company'] = Company.objects.get(id=self.kwargs['company_id'])
        except Company.DoesNotExist:
            raise Http404('Компания не найдена')
        return self.kwargs['company'].vacancies.select_related('specialty', 'company')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.kwargs['company']
        context['vacancies_category'] = self.kwargs['company'].name
        return context


class VacancyDetail(DetailView):
    form_class = ApplicationForm
    template_name = 'catalog/job_seeker/vacancy_detail.html'

    def get_object(self, queryset=None):
        try:
            vacancy = (
                Vacancy.objects.select_related('specialty', 'company')
                .get(id=self.kwargs['vacancy_id'])
            )
        except Vacancy.DoesNotExist:
            raise Http404('Вакансия не найдена')
        return vacancy

    @method_decorator(login_required)
    def post(self, request, **kwargs):
        vacancy_id = kwargs['vacancy_id']
        vacancy = self.get_object()
        form = self.form_class(request.POST)
        if form.is_valid():
            new_application = form.save(commit=False)
            new_application.vacancy = vacancy
            new_application.user = request.user
            new_application.save()
            messages.success(request, f'Отклик на вакансию "{vacancy_id}" отправлен')
            return redirect('vacancy_send', vacancy_id)
        context = {'form': form, 'vacancy': vacancy}
        return render(request, self.template_name, context)


class VacancySend(LoginRequiredMixin, TemplateView):
    template_name = 'catalog/job_seeker/vacancy_send.html'

    def dispatch(self, *args, **kwargs):
        vacancy_id = kwargs['vacancy_id']
        msg = f'Отклик на вакансию "{vacancy_id}" отправлен'
        if msg not in [msg.message for msg in self.request._messages]:
            return redirect('vacancy_detail', vacancy_id)
        return super().dispatch(*args, **kwargs)


class Search(ListView):
    template_name = 'catalog/job_seeker/search.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        query = self.request.GET.get('s')
        query = query.strip() if query else ''
        if query:
            return Vacancy.objects.select_related('company', 'specialty').filter(
                Q(title__icontains=query) |
                Q(skills__icontains=query) |
                Q(description__icontains=query)
            )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('s')
        return context


# EMPLOYER


class MyCompanyLetsstart(LoginRequiredMixin, HasNotCompanyMixin, TemplateView):
    template_name = 'catalog/employer/mycompany_letsstart.html'


class MyCompanyCreate(LoginRequiredMixin, HasNotCompanyMixin, CreateView):
    form_class = CompanyForm
    template_name = 'catalog/employer/mycompany.html'
    extra_context = {'page': 'company', 'info': 'Создание компании'}

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            new_company = form.save(commit=False)
            new_company.owner = request.user
            new_company.save()
            messages.success(request, 'Компания создана')
            return redirect('mycompany_update')
        context = self.extra_context
        context['form'] = form
        return render(request, self.template_name, context)


class MyCompanyUpdate(LoginRequiredMixin, HasCompanyMixin, UpdateView):
    form_class = CompanyForm
    template_name = 'catalog/employer/mycompany.html'
    extra_context = {'page': 'company', 'info': 'Информация о компании'}

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user.company)
        msgs = [msg.message for msg in request._messages]
        msg = msgs[0] if msgs else ''
        context = self.extra_context
        context['form'] = form
        context['msg'] = msg
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        company = request.user.company
        form = self.form_class(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Информация о компании обновлена')
            return redirect('mycompany_update')
        context = self.extra_context
        context['form'] = form
        return render(request, self.template_name, context)


class MyCompanyVacancyList(LoginRequiredMixin, ListView):
    model = Vacancy
    template_name = 'catalog/employer/mycompany_vacancies_list.html'
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


class MyCompanyVacancyCreate(LoginRequiredMixin, HasCompanyMixin, CreateView):
    form_class = VacancyForm
    template_name = 'catalog/employer/mycompany_vacancy.html'
    extra_context = {'page': 'vacancies', 'title': 'Создание вакансии'}

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = self.extra_context
        context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.company = request.user.company
            vacancy.published_at = date.today()
            vacancy.save()
            messages.success(request, 'Вакансия создана')
            return redirect('mycompany_vacancy_update', vacancy.id)
        context = self.extra_context
        context['form'] = form
        return render(request, self.template_name, context)


class MyCompanyVacancyUpdate(LoginRequiredMixin, UpdateView):
    form_class = VacancyForm
    template_name = 'catalog/employer/mycompany_vacancy.html'

    def get_object(self, queryset=None):
        vacancy_id = self.kwargs['vacancy_id']
        try:
            vacancy = (
                Vacancy.objects.prefetch_related('applications')
                .select_related('specialty')
                .annotate(applications_count=Count('applications'))
                .get(id=vacancy_id, company__owner=self.request.user)
                # такая фильтрация нужна для того, чтобы нельзя было редактировать вакансии чужой компании
            )
        except Vacancy.DoesNotExist:
            raise PermissionDenied('Вы не можете редактировать вакансии чужой компании.')
        return vacancy

    def get(self, request, *args, **kwargs):
        vacancy = self.get_object()
        form = self.form_class(instance=vacancy)
        msgs = [msg.message for msg in request._messages]
        msg = msgs[0] if msgs else ''
        context = {
            'form': form,
            'vacancy': vacancy,
            'msg': msg,
            'page': 'vacancies',
            'title': vacancy.title,
        }
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        vacancy = self.get_object()
        form = self.form_class(request.POST, instance=vacancy)
        if form.is_valid():
            form.save()
            messages.success(request, 'Информация о вакансии обновлена')
            return redirect('mycompany_vacancy_update', kwargs['vacancy_id'])
        context = {
            'form': form,
            'vacancy': vacancy,
            'page': 'vacancies',
            'title': vacancy.title,
        }
        return render(request, self.template_name, context)
