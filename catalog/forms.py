import re

from django import forms
from django.core.exceptions import ValidationError

from catalog.models import Application, Company, Vacancy, Specialty, Resume


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


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = (
            'name',
            'surname',
            'status',
            'salary',
            'specialty',
            'grade',
            'education',
            'experience',
            'portfolio',
        )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'custom-select mr-sm-2'}),
            'salary': forms.TextInput(attrs={'class': 'form-control'}),
            'specialty': forms.Select(attrs={'class': 'custom-select mr-sm-2'}),
            'grade': forms.Select(attrs={'class': 'custom-select mr-sm-2'}),
            'education': forms.Textarea(attrs={'class': 'form-control text-uppercase', 'rows': 4}),
            'experience': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'portfolio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'http://anylink.github.io'}),
        }
        labels = {'salary': 'Ожидаемое вознаграждение'}
