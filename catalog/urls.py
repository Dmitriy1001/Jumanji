from django.urls import path, re_path

from . import views


urlpatterns = [
    # JOB_SEEKER
    path('', views.Index.as_view(), name='index'),
    path('vacancies/', views.VacancyList.as_view(), name='vacancies_list'),
    path(
        'vacancies/cat/<slug:specialty_code>/',
        views.SpecialtyVacancyList.as_view(),
        name='specialty_vacancies_list',
    ),
    path('companies/<int:company_id>/', views.CompanyVacancyList.as_view(), name='company_vacancies_list'),
    path('vacancies/<int:vacancy_id>/', views.VacancyDetail.as_view(), name='vacancy_detail'),
    path('vacancies/<int:vacancy_id>/send/', views.VacancySend.as_view(), name='vacancy_send'),
    path('search/', views.Search.as_view(), name='search'),
    # path('myresume/letsstart/'),
    # path('myresume/create/'),
    # path('myresume/'),

    # EMPLOYER
    path('mycompany/letsstart/', views.MyCompanyLetsstart.as_view(), name='mycompany_letsstart'),
    path('mycompany/create/', views.MyCompanyCreate.as_view(), name='mycompany_create'),
    path('mycompany/', views.MyCompanyUpdate.as_view(), name='mycompany_update'),
    path('mycompany/vacancies/', views.MyCompanyVacancyList.as_view(), name='mycompany_vacancies_list'),
    path('mycompany/vacancies/create/', views.MyCompanyVacancyCreate.as_view(), name='mycompany_vacancy_create'),
    path(
        'mycompany/vacancies/<int:vacancy_id>/',
        views.MyCompanyVacancyUpdate.as_view(),
        name='mycompany_vacancy_update',
    ),
]
