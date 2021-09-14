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
    list_display = ('title', 'written_username', 'written_phone', 'vacancy', 'user')
    readonly_fields = ('title', 'user')

    @admin.display(description='Заголовок')
    def title(self, application):
        return f'{application.written_username} откликнулся на "{application.vacancy}"'

    def save_model(self, request, application, form, change):
        if not change:
            application.user = request.user
        application.save()


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('title', 'code')
    readonly_fields = ('title', 'code')



