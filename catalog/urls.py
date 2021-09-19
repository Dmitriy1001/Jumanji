from django.urls import path

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
    path('companies/<int:company_id>/', views.CompanyVacancyList.as_view(), name='company_detail'),
    path('vacancies/<int:vacancy_id>/', views.VacancyDetail.as_view(), name='vacancy_detail'),
    path('vacancies/<int:vacancy_id>/send/', views.VacancySend.as_view(), name='vacancy_send'),

    # EMPLOYER
    path('mycompany/letsstart/', views.MyCompanyLetsstart.as_view(), name='mycompany_letsstart'),
    path('mycompany/create/', views.MyCompanyCreate.as_view(), name='mycompany_create'),
    path('mycompany/', views.MyCompany.as_view(), name='mycompany'),
    path('mycompany/vacancies/', views.MyCompanyVacancyList.as_view(), name='mycompany_vacancies'),
    path('mycompany/vacancies/create/', views.MyCompanyVacancyCreate.as_view(), name='my_vacancies_create'),
    path(
        'mycompany/vacancies/<int:vacancy_id>/',
        views.MyCompanyVacancyDetail.as_view(),
        name='mycompany_vacancy_detail',
    ),
]
