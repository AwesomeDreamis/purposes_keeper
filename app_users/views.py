from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .forms import RegisterForm, ProfileEditForm
from .models import Profile, FriendRequest
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
import logging

logger = logging.getLogger(__name__)


class Login(LoginView):
    """Представление логина"""
    template_name = 'users/login.html'


class Logout(LogoutView):
    """Представление разлогина"""
    next_page = '/'


class RegisterView(View):
    """Представление регистрации"""

    def get(self, request):
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user,
            )
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            # to_email = form.clean_email()
            # from_email = 'awesomedreamis@gmail.com'
            # subject = 'Подтверждение электронной почты'
            # message = 'Перейдите по ссылке, чтобы подтвердить электронную почту'
            # send_mail(subject, message, from_email, [to_email], fail_silently=False)

            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'email or username is already taken ')
            return redirect('register')


class ProfileView(View, UserPassesTestMixin):
    """Представление просмотра профиля"""

    def get(self, request, pk):
        if not self.request.user.id == pk:
            raise PermissionDenied

        user_data = User.objects.get(id=pk)
        profile_data = user_data.profile
        user_form = RegisterForm(instance=user_data)
        profile_form = RegisterForm(instance=profile_data)

        if not request.user == user_data:
            raise PermissionDenied()

        return render(request, 'users/profile.html', context={'user_form': user_form,
                                                              'profile_form': profile_form,
                                                              'user': user_data,
                                                              'profile': profile_data,
                                                              'profile_id': pk,
                                                              })


class ProfileUpdateView(View):
    """Представление редактирования профиля"""

    def get(self, request, profile_id):
        if not self.request.user.id == profile_id:
            raise PermissionDenied

        user = request.user
        user_profile = get_object_or_404(Profile, user=user)
        default_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email,
            'profile_img': user_profile.profile_img,
            'profile_head_img': user_profile.profile_head_img,

        }

        form = ProfileEditForm(default_data)

        return render(request, 'users/profile_edit.html', {'form': form, 'user': user})

    def post(self, request, profile_id):
        if not self.request.user.id == profile_id:
            raise PermissionDenied

        user = request.user
        user_profile = get_object_or_404(Profile, user=user)
        form = ProfileEditForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.username = form.cleaned_data['username']
                old_email = user.email
                user.email = form.cleaned_data['email']

                if form.cleaned_data['profile_img']:
                    user_profile.profile_img = form.cleaned_data['profile_img']
                if form.cleaned_data['profile_head_img']:
                    user_profile.profile_head_img = form.cleaned_data['profile_head_img']

                if user.email == old_email\
                        or not User.objects.filter(email=user.email).exists():
                    user.save()
                    user_profile.save()
                    return redirect('profile', profile_id)
                else:
                    raise
            except:
                return redirect('profile_edit', profile_id)
        else:
            return redirect('profile_edit', profile_id)


class FriendsView(ListView):
    """Представление страницы с друзьями"""

    model = User
    context_object_name = 'friends'
    template_name = 'users/friends.html'
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user

        if self.request.GET.get('search'):
            query = self.request.GET.get('search')
            queryset = User.objects.filter(username__icontains=query)
        else:
            queryset = user.profile.friends.all()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(FriendsView, self).get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), 20)
        page_number = self.request.GET.get('page')
        if self.request.GET.get('search'):
            context['search'] = True

        friends_requests = FriendRequest.objects.filter(to_user=self.request.user)
        context['friends_requests'] = friends_requests
        requests_to_me = []
        for submit in friends_requests:
            requests_to_me.append(submit.from_user)
        context['requests_to_me'] = requests_to_me

        friends_submits = FriendRequest.objects.filter(from_user=self.request.user)
        potential_friends = []
        for submit in friends_submits:
            potential_friends.append(submit.to_user)
        context['friends_submits'] = potential_friends

        context['data'] = paginator.get_page(page_number)
        context['user'] = self.request.user
        return context


class SendFriendRequest(View):
    """отправка запроса для добавления в друзья"""
    def post(self, request):
        from_user = request.user
        to_user_id = request.POST.get('user_id')
        to_user = User.objects.get(id=to_user_id)
        friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
        if created:
            return redirect('friends')
        else:
            friend_request.delete()
            return redirect('friends')


def accept_friend_request(request, request_id):
    """Принимает запрос в друзья"""
    friend_request = FriendRequest.objects.get(id=request_id)
    if friend_request.to_user == request.user:
        friend_request.to_user.profile.friends.add(friend_request.from_user)
        friend_request.from_user.profile.friends.add(friend_request.to_user)
        friend_request.delete()
        return redirect('friends')
    else:
        return redirect('friends')


def decline_friend_request(request, request_id):
    """Отклоняет запрос в друзья"""
    friend_request = FriendRequest.objects.get(id=request_id)
    if friend_request.to_user == request.user:
        friend_request.delete()
        return redirect('friends')
    else:
        return redirect('friends')
