from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name = 'logout'),

    path('profile/', views.profile, name='profile'),
    path('create_finance_settlement/', views.create_finance_settlement, name='create_finance_settlement'),
]#  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
