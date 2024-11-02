from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home-page'),
    path('register/', views.register,name='register-page'),
    path('login/', views.user_login, name='login-page'),
    path('logout/', views.LogoutView, name='logout'),
    path('delete/<str:name>/', views.DeleteTask, name='delete-page'),
    path('update/<str:name>/', views.Update, name='update'),

]