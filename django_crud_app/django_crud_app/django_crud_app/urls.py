from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from users.views import auth_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shops/', include('shops.urls')),
    path('', RedirectView.as_view(url='login/', permanent=True)),
]

#  Add Django site authentication urls (for, logout, password management) and custom login view
urlpatterns += [
    path('login/', auth_view, name='custom_login'),
    path('accounts/', include('django.contrib.auth.urls')),
]

# Url for list of users
urlpatterns += [
    path('loggedin/', include('users.urls')),
]
