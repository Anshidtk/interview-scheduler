from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('login_user', views.LoginUserView.as_view(), name='login_user'),
    path('logout', views.logout_user, name='logout'),
    path('index', views.index, name='index'),
    path('add_users', views.add_users, name='add_users'),
    path('save_user', views.SaveUserView.as_view(), name='save_user'),
    path('save_available_time', views.SaveAvailableTimeView.as_view(), name='save_available_time'),
    path('search_available_times', views.SearchAvailableTimesView.as_view(), name='search_available_times'),
]