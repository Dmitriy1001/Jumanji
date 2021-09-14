import re
from django import forms
from django.core.exceptions import ValidationError

from catalog.models import Application, Company, Vacancy, Specialty


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('written_username', 'written_phone', 'written_cover_letter')

    def clean_written_phone(self):
        written_phone = self.cleaned_data['written_phone']
        if not re.match(r'^[\d\(\)\-\s+]+$', written_phone):
            raise ValidationError('Неверный формат номера')
        return written_phone


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'logo', 'location', 'description', 'employee_count')


class VacancyForm(forms.ModelForm):
    specialty = forms.ModelChoiceField(queryset=Specialty.objects.all())
    class Meta:
        model = Vacancy
        fields = ('title', 'specialty', 'salary_min', 'salary_max', 'skills', 'description')

