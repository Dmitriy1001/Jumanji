import re

from django import template

register = template.Library()


@register.filter
def ending(number, word):
    '''Makes the correct word ending for "вакансия" or "человек" depending on number.
The second argument(word) must be "вакансия" or "человек"'''
    none_value = {'вакансия': 'Нет вакансий', 'человек': ''}
    if not number:
        return none_value[word]
    vacancies = {
        '1': 'вакансия',
        '2': 'вакансии', '3': 'вакансии', '4': 'вакансии',
        '5': 'вакансий', '6': 'вакансий', '7': 'вакансий',
        '8': 'вакансий', '9': 'вакансий', '0': 'вакансий',
    }
    people = {
        '1': 'человек',
        '2': 'человека', '3': 'человека', '4': 'человека',
        '5': 'человек', '6': 'человек', '7': 'человек',
        '8': 'человек', '9': 'человек', '0': 'человек',
    }

    number = str(number)
    ending = vacancies if word == 'вакансия' else people
    if number not in ('11', '12', '13', '14'):
        return f"{number} {ending[number[-1]]}"
    return f"{number} вакансий" if word == 'вакансия' else f"{number} человек"


@register.filter
def bullet(string):
    '''Separates items in a string with " • "'''
    return ' • '.join(re.findall(r'([\w\s]+)[,\s]*', string))
