from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('vacancies/', views.vacancies_list, name='vacancies_list'),
    path(
        'vacancies/cat/<slug:specialty_code>/',
        views.specialty_vacancies_list,
        name='specialty_vacancies_list',
    ),
    path('companies/<int:company_id>/', views.company_detail, name='company_detail'),
    path('vacancies/<int:vacancy_id>/', views.vacancy_detail, name='vacancy_detail'),
    path('vacancies/<int:vacancy_id>/send/', views.vacancy_send, name='vacancy_send'),
    # mycompany
    path('mycompany/letsstart/', views.mycompany_letsstart),
    path('mycompany/create/', views.mycompany_create),
    path('mycompany/', views.mycompany),
    path('mycompany/vacancies/', views.my_vacancies),
    path('mycompany/vacancies/create/', views.my_vacancies_create),
    path('mycompany/vacancies/<int:vacancy_id>/', views.my_vacancy_detail),
    # account
    # path('login/'),
    # path('register/'),
    # path('logout/'),
]
