from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_user, name='login'),
    path('profile/', views.main_profile, name='main_profile'),
    path('logout/', views.logout_user, name = 'logout')
]#  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
