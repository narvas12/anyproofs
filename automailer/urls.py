from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('accounts/profile/', profile_view, name='profile'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('binance_deposit/', binance_deposit, name='binance_deposit'),
    path('binance_withdrawal/', binance_withdrawal, name='binance_withdrawal'),
    path('blockchain_withdrawal/', blockchain_withdrawal, name='blockchain_withdrawal'),
    path('blockchain_recieve/', blockchain_recieve, name='blockchain_recieve'),
    # path('blockchain_withdrawal/', blockchain_withdrawal, name='blockchain_withdrawal'),
]


    
