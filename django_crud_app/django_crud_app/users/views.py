from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from rest_framework.generics import get_object_or_404
from .forms import AddUserForm, EditUserForm, AuthForm

from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Permission
from django.views.generic import ListView, DetailView
from django.contrib import auth


# Custom login view
def auth_view(request):
    form = AuthForm()
    if request.POST:
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        next_link = request.session['next'] = request.GET.get('next', '')

        if username is not None and password is not None:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    if not next_link:
                        if is_superuser(user) or is_staff(user) or is_permitted(user, 'view_user'):
                            return HttpResponseRedirect('/loggedin')
                        return render(request, 'registration/login.html', {'form': form, 'next': '/loggedin'})
            else:
                form.errors['not_match'] = 'Your username and password didn\'t match. Please try again'

    return render(request, 'registration/login.html', {'form': form})


# Additional permissions to check whether user is staff, root or has a particular permission
def is_superuser(user):
    return user.is_superuser


def is_staff(user):
    return user.is_staff


def is_permitted(user, codename):
    permission = Permission.objects.filter(user=user, codename=codename)
    return bool(len(permission))


# home view for users.
class LoggedInView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'users/loggedin.html'
    context_object_name = 'user_list'

    def test_func(self):

        return is_superuser(self.request.user) or is_permitted(self.request.user, 'view_user')

    def handle_no_permission(self):
        form = AuthForm
        return render(self.request, 'registration/login.html', {'form': form, 'next': '/loggedin'})

    def get_queryset(self):
        return User.objects.all()


# Detail view (view user detail)
class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user-detail.html'


# New user view (Create new user)
@login_required
@permission_required('auth.add_user')
def userview(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('loggedin')
        else:
            print(form.errors)
            return render(request, 'users/user.html', {'form': form})
    form = AddUserForm()
    return render(request, 'users/user.html', {'form': form})


# Edit user
@login_required
@permission_required('auth.change_user')
def edit(request, pk, template_name='users/edit.html'):
    user = get_object_or_404(User, pk=pk)
    form = EditUserForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('loggedin')
    return render(request, template_name, {'form': form})


# Delete user
@login_required
@permission_required('auth.delete_user')
def delete(request, pk, template_name='users/confirm_delete.html'):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('loggedin')
    return render(request, template_name, {'object': user})
