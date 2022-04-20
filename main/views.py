from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
# Create your views here.
from .forms import RegisterUserForm, LoginUserForm, PostForm, RequestForm
from .models import *


class PostView(ListView):
    model = Post
    template_name = "main/index.html"
    extra_context = {'title': "Главная страница"}


def index(request):
    posts = Post.objects.all()
    data = {
        'posts': posts,
        'name': request.user.username,
        'post_count': posts.count()  # FIXME
    }
    return render(request, 'main/home.html', data)

@login_required
def my_page(request):
    cur_user = request.user.id
    posts = Post.objects.filter(author_id=cur_user).order_by('-time_create')
    data = {

        'posts': posts,
        'name': request.user.username,
        # 'post_count': posts.count()  # FIXME
    }
    return render(request, 'main/my_page.html', data)

@login_required

def enemy_page(request, id):
    cur_user = id
    posts = Post.objects.filter(author_id=cur_user).order_by('-time_create')
    data = {

        'posts': posts,
        'name': User.objects.get(pk=cur_user).username
        # 'post_count': posts.count()  # FIXME
    }
    return render(request, 'main/page.html', data)

@login_required
def feed(request):
    posts = Post.objects.all().order_by('-time_create')
    return render(request, 'main/feed.html', {'posts':posts} )




class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        return dict(list(context.items()))

    def form_valid(self, form):
        user1 = form.save()
        profile = Profile(user=user1)
        profile.save()
        login(self.request, user1)
        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        return dict(list(context.items()))

    def get_success_url(self):
        return reverse_lazy('my_page')


def logout_user(request):
    logout(request)
    return redirect('login')



def create_post(request):
    error = ''
    cur_user = request.user
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            post.author = Profile.objects.get(pk=cur_user.id)
            post.save()
            return redirect('my_page')
        else:
            error = "Форма была неверной"

    form = PostForm()
    data = {
        'form': form,
        'error':error
    }
    return render(request, 'main/create_post.html',data)


def create_request(request):
    error = ''
    cur_user = request.user
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            request = form.save()
            request.from_user = Profile.objects.get(pk=cur_user.id)
            request.save()
            return redirect('my_page')
        else:
            error = "Форма была неверной"

    form = RequestForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'main/create_post.html', data)


def find_friends(id):
    fr = Friend.objects.all()
    friends_array = []
    fr1 = Friend.objects.filter(friend1=id)
    fr2 = Friend.objects.filter(friend2=id)
    for f in fr1:
        friends_array.append(f.friend2.id)
    for f in fr2:
        friends_array.append(f.friend1.id)
    return friends_array

def friends(request):
    cur_user = request.user
    fr = Friend.objects.all()
    friends_array = find_friends(cur_user.id)
    friends_names = []

    for i in friends_array:
        friends_names.append((User.objects.get(pk=i).username,i))

    for i in friends_names:
        print(i)



    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():

            uzver = form.cleaned_data['user']

            will_add = User.objects.get(username=uzver)

            if find_friends(will_add.id).count(cur_user.id) == 0 and will_add.id != cur_user.id:
                a = Friend(friend1=Profile.objects.get(pk=cur_user.pk), friend2=Profile.objects.get(pk=will_add.pk))
                a.save()
            return redirect('friends')
        else:
            error = "Форма была неверной"

    form = RequestForm(request.POST)

    data = {
        'friends': friends_names,
        'form':form,

    }

    return render(request, 'main/friends.html',data)