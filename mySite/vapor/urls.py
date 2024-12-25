from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path('', views.GameListView.as_view(), name='index'),
    path('<slug:slug>',views.GameView.as_view(),name='game-detail'),
    path('api/getGames',views.game_list_api),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),


]
