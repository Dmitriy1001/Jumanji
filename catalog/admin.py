from django.contrib import admin

from .models import Vacancy, Company, Specialty, Application


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'specialty', 'company', 'published_at')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'employee_count', 'owner')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('description', 'written_username', 'written_phone', 'vacancy', 'user')
    readonly_fields = ('description',)

    def description(self, application):
        return f'отклик пользователя {application.written_username} на "{application.vacancy}"'


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('title', 'code')
    readonly_fields = ('title', 'code')



