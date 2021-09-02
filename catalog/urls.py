from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('vacancies/', views.vacancies_list, name='vacancies_list'),
    path(
        'vacancies/cat/<str:specialty_code>/',
        views.specialty_vacancies_list,
        name='specialty_vacancies_list'
    ),
    path('companies/<int:company_id>/', views.company_detail, name='company_detail'),
    path('vacancies/<int:vacancy_id>/', views.vacancy_detail, name='vacancy_detail'),
]