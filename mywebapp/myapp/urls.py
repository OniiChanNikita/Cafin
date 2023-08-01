from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name = 'logout'),

    path('profile/', views.profile, name='profile'),
    path('profile/<slug:slug_username>', views.profile_users, name='profile_users'),
    
    path('search_users/', views.search_users, name='search_users'),
    path('create_finance_settlement/', views.create_finance_settlement, name='create_finance_settlement'),
    path('finance_tables/', views.finance_tables, name = 'finance_tables'),
    path('finance_tables/<slug:slug_financesettlement>/', views.open_finance_settlement, name = 'open_finance_settlement'),
    path('delete_operating/<int:element_id>/', views.delete_operating, name='delete_operating'),
    path('delete_table/<int:element_id_table>/', views.delete_table, name='delete_table'),
    path('modify_table/<slug:slug_financesettlement>/', views.modify_table, name='modify_table'),

    path('chat/', views.list_chat_box, name='list_chat_box'),
    path('create_redirect_chat/<str:slug_username>/', views.create_chat_or_redirect, name='create_chat_or_redirect'),
    path('chat/<slug:slug_num>/', views.chat_box, name='chat_box'),
]

if settings.DEBUG == False:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

