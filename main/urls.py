from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="home"),
    path('my_page', views.my_page, name="my_page"),
    path('feed', views.feed, name="feed"),
    path('register', views.RegisterUser.as_view(), name="register"),
    path('login', views.LoginUser.as_view(), name="login"),
    path('logout', views.logout_user, name="logout"),
    path('create_post', views.create_post, name="create_post"),
    path('page/<int:id>', views.enemy_page, name='page'),
    path('friends',views.friends,name='friends')

]
