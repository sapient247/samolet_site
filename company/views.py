from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import FeedbackForm, CustomUserCreationForm, NewsForm, LoginForm
from django.contrib.auth.decorators import user_passes_test
from .models import News, Feedback

# Главная
def home(request):
    return render(request, 'home.html')

# Проекты (демо-данные)
def projects(request):
    projects = [
        {'name': 'ЖК Лайково', 'description': 'Современный жилой комплекс.', 'image_url': '/static/img/project1.jpg'},
        {'name': 'ЖК Томилино', 'description': 'Комфорт и доступность.', 'image_url': '/static/img/project2.jpg'},
    ]
    return render(request, 'projects.html', {'projects': projects})

# Новости (демо-данные)
def news(request):
    news_list = News.objects.all().order_by('-date')  # Загружаем новости из базы
    return render(request, 'news.html', {'news': news_list})

def delete_news(request, news_id):
    news_item = get_object_or_404(News, id=news_id)
    news_item.delete()
    return redirect('add_news')  # возвращаемся обратно к форме

# Обратная связь
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})

# Регистрация
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def custom_404(request, exception):
    return render(request, '404.html', status=404)

from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    messages = Feedback.objects.filter(email=request.user.email)
    return render(request, 'profile.html', {'messages': messages})

def sitemap(request):
    return render(request, 'sitemap.html')

# Функция для проверки, является ли пользователь администратором
def is_admin_user(user):
    return user.is_superuser  # Проверка, если это администратор

# Применяем декоратор для ограничения доступа
@user_passes_test(is_admin_user)
def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Сохраняем новость
            return redirect('add_news')  # Перенаправляем на страницу добавления новости
    else:
        form = NewsForm()  # Для GET-запроса создаем пустую форму

    # Получаем все новости для отображения
    news_list = News.objects.all().order_by('-date')  # Загружаем новости из базы данных

    # Получаем все обращения из базы данных
    feedback_list = Feedback.objects.all().order_by('-id')  # Получаем все записи в таблице Feedback

    return render(request, 'add_news.html', {'form': form, 'news_list': news_list, 'feedback_list': feedback_list})

# Представление для страницы входа
def login_view(request):
    if request.user.is_authenticated:
        return redirect('add_news')  # Если пользователь уже вошел, перенаправляем к add_news

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if is_admin_user(user):  # Проверка, если это админ
                    return redirect('add_news')
                else:
                    return redirect('home')  # Если это не админ, перенаправляем на главную страницу
            else:
                form.add_error(None, "Неверный логин или пароль")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})
from django.shortcuts import render

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)
