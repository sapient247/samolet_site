from django.contrib import admin
from django.urls import path
from company import views as company_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from company import views as company_views

urlpatterns = [
    path('delete_news/<int:news_id>/', company_views.delete_news, name='delete_news'),
    path('add_news/', company_views.add_news, name='add_news'),
    path('admin/', admin.site.urls),
    path('', company_views.home, name='home'),
    path('projects/', company_views.projects, name='projects'),
    path('news/', company_views.news, name='news'),
    path('sitemap/', company_views.sitemap_view, name='sitemap'),
    path('feedback/', company_views.feedback, name='feedback'),
    path('accounts/register/', company_views.register, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('accounts/profile/', company_views.profile, name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'company.views.custom_404'

