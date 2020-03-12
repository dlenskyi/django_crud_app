from django.urls import path
from . import views


urlpatterns = [
    path('', views.ShopView.as_view(), name='shop-home'),
    path('<pk>/', views.ShopDetailView.as_view(), name='shop-detail'),
    path('edit/<pk>/', views.edit, name='edit-shop'),
    path('shop/add/', views.shopview, name='shop'),
    path('delete/<pk>/', views.delete, name='delete-shop'),
]