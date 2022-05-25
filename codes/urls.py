from django.urls import path
from . import views

app_name = 'codes'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/', views.FirstFactorAuthenticationView.as_view(), name='login_first'),
    path('login/second', views.SecondFactorAuthenticationView.as_view(), name='login_second'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('register/second', views.RegisterVerifyView.as_view(), name='register-verify')
]
