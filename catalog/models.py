from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Vacancy(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название вакансии')
    specialty = models.ForeignKey(
        'Specialty',
        related_name='vacancies',
        on_delete=models.CASCADE,
        verbose_name='Специализация',
    )
    company = models.ForeignKey(
        'Company',
        related_name='vacancies',
        on_delete=models.CASCADE,
        verbose_name='Компания',
    )
    skills = models.TextField(verbose_name='Навыки')
    description = models.TextField(verbose_name='Текст')
    salary_min = models.PositiveIntegerField(verbose_name='Зарплата от')
    salary_max = models.PositiveIntegerField(verbose_name='Зарплата до')
    published_at = models.DateField(verbose_name='Опубликовано')

    class Meta:
        verbose_name = 'вакансия'
        verbose_name_plural = 'вакансии'
        ordering = ('-published_at',)

    def __str__(self):
        return self.title


class Company(models.Model):
    name = models.CharField(unique=True, max_length=255, verbose_name='Название')
    location = models.CharField(max_length=255, verbose_name='Город')
    logo = models.ImageField(upload_to=settings.MEDIA_COMPANY_IMAGE_DIR, verbose_name='Логотипчик')
    description = models.TextField(verbose_name='Информация о компании')
    employee_count = models.PositiveIntegerField(verbose_name='Количество сотрудников')
    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Владелец')

    class Meta:
        verbose_name = 'компания'
        verbose_name_plural = 'компании'

    def __str__(self):
        return self.name


class Specialty(models.Model):
    code = models.SlugField(unique=True, verbose_name='Код')
    title = models.CharField(unique=True, max_length=255, verbose_name='Название')
    picture = models.ImageField(upload_to=settings.MEDIA_SPECIALITY_IMAGE_DIR, verbose_name='Картинка')

    class Meta:
        verbose_name = 'специализация'
        verbose_name_plural = 'специализации'

    def __str__(self):
        return self.title


class Application(models.Model):
    written_username = models.CharField(max_length=255, verbose_name='Имя')
    written_phone = models.CharField(max_length=255, verbose_name='Телефон')
    written_cover_letter = models.TextField(verbose_name='Сопроводительное письмо')
    vacancy = models.ForeignKey(
        Vacancy,
        related_name='applications',
        on_delete=models.CASCADE,
        verbose_name='Вакансия',
    )
    user = models.ForeignKey(
        User,
        related_name='applications',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )

    class Meta:
        verbose_name = 'отклик'
        verbose_name_plural = 'отклики'

    def __str__(self):
        return f'{self.written_username} откликнулся на "{self.vacancy}"'
