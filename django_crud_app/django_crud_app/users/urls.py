from django.urls import path

from . import views

urlpatterns = [
    path('', views.LoggedInView.as_view(), name='loggedin'),
    path('<pk>/', views.UserDetailView.as_view(), name='detail'),
    path('edit/<pk>/', views.edit, name='edit'),
    path('user/add/', views.userview, name='user'),
    path('delete/<pk>/', views.delete, name='delete'),
]