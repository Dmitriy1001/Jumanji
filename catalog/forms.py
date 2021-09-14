from django import forms

from catalog.models import Application, Company, Vacancy, Specialty


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('written_username', 'written_phone', 'written_cover_letter')


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'logo', 'location', 'description', 'employee_count')


class VacancyForm(forms.ModelForm):
    specialty = forms.ModelChoiceField(queryset=Specialty.objects.all())
    class Meta:
        model = Vacancy
        fields = ('title', 'specialty', 'salary_min', 'salary_max', 'skills', 'description')

