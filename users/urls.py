from django.urls import path
from .views import signUp, logIn, logOut, walletUpdate
from django.views.generic import TemplateView

urlpatterns =[
    path('signup/', signUp, name='sign_up'),
    path('login/', logIn, name='login'),
    path('profile/', TemplateView.as_view(template_name='users/user_profile.html'), name='profile'),
    path('wallet/', TemplateView.as_view(template_name='users/wallet.html'), name='wallet'),
    path('add_balance/', walletUpdate, name='update_balance'),
    path('logout/', logOut, name='logout')
]