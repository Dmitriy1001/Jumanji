from django.contrib import admin

from .models import Vacancy, Company, Specialty


admin.site.register(Vacancy)
admin.site.register(Company)
admin.site.register(Specialty)