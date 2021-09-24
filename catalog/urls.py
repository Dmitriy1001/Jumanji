from django.urls import path

from . import job_seeker_views, employer_views


urlpatterns = [
    path('', job_seeker_views.Index.as_view(), name='index'),

    # JOB_SEEKER
    path('vacancies/', job_seeker_views.VacancyList.as_view(), name='vacancies_list'),
    path(
        'vacancies/cat/<slug:specialty_code>/',
        job_seeker_views.SpecialtyVacancyList.as_view(),
        name='specialty_vacancies_list',
    ),
    path('companies/<int:company_id>/', job_seeker_views.CompanyVacancyList.as_view(), name='company_vacancies_list'),
    path('vacancies/<int:vacancy_id>/', job_seeker_views.VacancyDetail.as_view(), name='vacancy_detail'),
    path('vacancies/<int:vacancy_id>/send/', job_seeker_views.VacancySend.as_view(), name='vacancy_send'),
    path('search/', job_seeker_views.Search.as_view(), name='search'),
    path('myresume/letsstart/', job_seeker_views.MyResumeLetsstart.as_view(), name='myresume_letsstart'),
    path('myresume/create/', job_seeker_views.MyResumeCreate.as_view(), name='myresume_create'),
    path('myresume/', job_seeker_views.MyResumeUpdate.as_view(), name='myresume_update'),

    # EMPLOYER
    path('mycompany/letsstart/', employer_views.MyCompanyLetsstart.as_view(), name='mycompany_letsstart'),
    path('mycompany/create/', employer_views.MyCompanyCreate.as_view(), name='mycompany_create'),
    path('mycompany/', employer_views.MyCompanyUpdate.as_view(), name='mycompany_update'),
    path('mycompany/vacancies/', employer_views.MyCompanyVacancyList.as_view(), name='mycompany_vacancies_list'),
    path(
        'mycompany/vacancies/create/',
        employer_views.MyCompanyVacancyCreate.as_view(),
        name='mycompany_vacancy_create',
    ),
    path(
        'mycompany/vacancies/<int:vacancy_id>/',
        employer_views.MyCompanyVacancyUpdate.as_view(),
        name='mycompany_vacancy_update',
    ),
]
