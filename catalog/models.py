from django.db import models


class Vacancy(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название вакансии')
    specialty = models.ForeignKey(
        'Specialty',
        related_name='vacancies',
        on_delete=models.CASCADE,
        verbose_name='Специализация'
    )
    company = models.ForeignKey(
        'Company',
        related_name='vacancies',
        on_delete=models.CASCADE,
        verbose_name='Компания'
    )
    skills = models.TextField(verbose_name='Навыки')
    description = models.TextField(verbose_name='Текст')
    salary_min = models.PositiveIntegerField(verbose_name='Зарплата от')
    salary_max = models.PositiveIntegerField(verbose_name='Зарплата до')
    published_at = models.DateField(verbose_name='Опубликовано')

    class Meta:
        verbose_name = 'вакансия'
        verbose_name_plural = 'вакансии'

    def __str__(self):
        return self.title


class Company(models.Model):
    name = models.CharField(unique=True, max_length=255, verbose_name='Название')
    location = models.CharField(max_length=255, verbose_name='Город')
    logo = models.URLField(default='https://place-hold.it/100x60', verbose_name='Логотипчик')
    description = models.TextField(verbose_name='Информация о компании')
    employee_count = models.PositiveIntegerField(verbose_name='Количество сотрудников')

    class Meta:
        verbose_name = 'компания'
        verbose_name_plural = 'компании'

    def __str__(self):
        return self.name




class Specialty(models.Model):
    code = models.SlugField(unique=True, verbose_name='Код')
    title = models.CharField(max_length=255, verbose_name='Название')
    picture = models.URLField(default='https://place-hold.it/100x60', verbose_name='Картинка')

    class Meta:
        verbose_name = 'специализация'
        verbose_name_plural = 'специализации'

    def __str__(self):
        return self.title