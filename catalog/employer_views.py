from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import CreateView, TemplateView, UpdateView, ListView

from .forms import CompanyForm, VacancyForm
from .mixins import HasCompanyMixin, HasNotCompanyMixin
from .models import Vacancy, Company


# EMPLOYER(MYCOMPANY) PART


class MyCompanyLetsstart(LoginRequiredMixin, HasNotCompanyMixin, TemplateView):
    template_name = 'catalog/employer/mycompany_letsstart.html'


class MyCompanyCreate(LoginRequiredMixin, HasNotCompanyMixin, CreateView):
    form_class = CompanyForm
    template_name = 'catalog/employer/mycompany.html'
    success_url = reverse_lazy('mycompany_update')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Компания создана')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        msgs = [msg.message for msg in self.request._messages]
        context['msg'] = msgs[0] if msgs else ''
        context.update({'page': 'company', 'info': 'Создание компании'})
        return context


class MyCompanyUpdate(LoginRequiredMixin, HasCompanyMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'catalog/employer/mycompany.html'
    success_url = reverse_lazy('mycompany_update')

    def get_object(self, queryset=None):
        if self.request.method == 'POST':
            messages.success(self.request, 'Информация о компании обновлена')
        return self.request.user.company

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        msgs = [msg.message for msg in self.request._messages]
        context['msg'] = msgs[0] if msgs else ''
        context.update({'page': 'company', 'info': 'Информация о компании'})
        return context


class MyCompanyVacancyList(LoginRequiredMixin, ListView):
    model = Vacancy
    template_name = 'catalog/employer/mycompany_vacancies_list.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
<<<<<<< HEAD
        self.kwargs['user'] = self.request.user
        return (
            Vacancy.objects.filter(company__owner=self.kwargs['user'])
            .annotate(applications_count=Count('applications'))
            .select_related('specialty', 'company')
            .order_by('-published_at')
=======
        return (
                Vacancy.objects.filter(company__owner=self.request.user)
                .annotate(applications_count=Count('applications'))
                .select_related('specialty', 'company')
                .order_by('-published_at')
>>>>>>> 1dcc37a317c65f609d67136a0d47e9cf296d4d1a
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
<<<<<<< HEAD
            company = self.kwargs['user'].company
=======
            company = self.request.user.company
>>>>>>> 1dcc37a317c65f609d67136a0d47e9cf296d4d1a
        except User.company.RelatedObjectDoesNotExist:
            company = None
        context.update({'company': company, 'page': 'vacancies'})
        return context


class MyCompanyVacancyCreate(LoginRequiredMixin, HasCompanyMixin, CreateView):
    form_class = VacancyForm
    template_name = 'catalog/employer/mycompany_vacancy.html'

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        form.instance.published_at = timezone.now()
        messages.success(self.request, 'Вакансия создана')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mycompany_vacancy_update', args=[self.object.id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        msgs = [msg.message for msg in self.request._messages]
        context['msg'] = msgs[0] if msgs else ''
        context.update({'page': 'vacancies', 'title': 'Создание вакансии'})
        return context


class MyCompanyVacancyUpdate(LoginRequiredMixin, UpdateView):
    model = Vacancy
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
            raise PermissionDenied('Вы можете редактировать вакансии только своей компании.')
        if self.request.method == 'POST':
            messages.success(self.request, 'Информация о вакансии обновлена')
        return vacancy

    def get_success_url(self):
        return reverse('mycompany_vacancy_update', args=[self.object.id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vacancy = self.object
        msgs = [msg.message for msg in self.request._messages]
        context['msg'] = msgs[0] if msgs else ''
        context.update({'page': 'vacancies', 'title': vacancy.title})
        return context
