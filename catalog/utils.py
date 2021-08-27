def make_correct_ending(number, word):
    '''Makes the correct word ending for "вакансия" or "человек" depending on number. The second argument(word) must be "vacancies" or "people"'''
    if number == 0:
        return "Нет вакансий" if word == 'vacancies' else ''
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
    ending = vacancies if word == 'vacancies' else people
    if number not in ('11', '12', '13', '14'):
        return f"{number} {ending[number[-1]]}"
    else:
        return f"{number} вакансий" if word == 'vacancies' else f"{number} человек"


def add_vacancies_number(queryset):
    '''For each instance in the queryset, forms a tuple consisting of this instance and the number of vacancies of this instance'''
    return map(
        lambda cls_obj: (cls_obj, make_correct_ending(cls_obj.vacancies.count(), 'vacancies')),
        queryset,
    )