from django.contrib import admin

from .models import Vacancy, Company, Specialty, Application, Resume


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'specialty', 'company', 'published_at')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'employee_count', 'owner')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'written_phone', 'vacancy')
    readonly_fields = ('title',)

    @admin.display(description='Заголовок')
    def title(self, application):
        return f'{application.written_username} откликнулся на "{application.vacancy}"'


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('title', 'code')


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'specialty', 'grade', 'portfolio')
    readonly_fields = ('title',)

    @admin.display(description='Заголовок')
    def title(self, resume):
        return f'Резюме пользователя {resume.user}'
