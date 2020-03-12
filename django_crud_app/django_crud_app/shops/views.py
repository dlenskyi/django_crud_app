from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from rest_framework.generics import get_object_or_404
from users.forms import AuthForm
from .forms import ShopForm

from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Shop


# Additional permissions to check whether user is staff, root or has a particular permission
def is_superuser(user):
    return user.is_superuser


# home view for shops
class ShopView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'shops/index.html'
    context_object_name = 'shop_list'

    def test_func(self):

        return is_superuser(self.request.user)

    def handle_no_permission(self):
        form = AuthForm
        return render(self.request, 'registration/login.html', {'form': form, 'next': '/loggedin'})

    def get_queryset(self):
        return Shop.objects.all()


# Detail view (view shop details)
class ShopDetailView(LoginRequiredMixin, DetailView):
    model = Shop
    template_name = 'shops/shop-detail.html'


# New shop view (Create new shop)
@login_required
@permission_required('auth.add_shop')
def shopview(request):
    if request.method == 'POST':
        form = ShopForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shop-home')
        else:
            return render(request, 'shops/shop.html', {'form': form})
    form = ShopForm()
    return render(request, 'shops/shop.html', {'form': form})


# Edit shop
@login_required
@permission_required('auth.change_shop')
def edit(request, pk, template_name='shops/edit.html'):
    shop = get_object_or_404(Shop, pk=pk)
    form = ShopForm(request.POST or None, instance=shop)
    if form.is_valid():
        form.save()
        return redirect('shop-home')
    return render(request, template_name, {'form': form})


# Delete shop
@login_required
@permission_required('auth.delete_shop')
def delete(request, pk, template_name='shops/confirm_delete.html'):
    shop = get_object_or_404(Shop, pk=pk)
    if request.method == 'POST':
        shop.delete()
        return redirect('shop-home')
    return render(request, template_name, {'object': shop})
