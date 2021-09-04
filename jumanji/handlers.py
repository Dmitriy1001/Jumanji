from django.shortcuts import render


def handler404(request, exception):
    title = 'Страница не найдена'
    msg = exception.args[0]
    if isinstance(msg, str):
        msg += '.  Страница, которую вы ищете, была удалена или никогда не существовала.'
    else:
        msg = 'Страница которую вы ищете была удалена или никогда не существовала.'
    return render(request, 'page404.html', {'title': title, 'msg': msg})


def handler500(request):
    title = 'Ошибка сервера'
    msg = 'Простите за неудобства, мы уже работаем, чтобы исправить это.'
    return render(request, 'page500.html', {'title': title, 'msg': msg})
