from django.urls import path
from .views import signUp, logIn, logOut
from django.views.generic import TemplateView

urlpatterns =[
    path('signup/', signUp, name='sign_up'),
    path('login/', logIn, name='login'),
    path('profile/', TemplateView.as_view(template_name='users/user_profile.html'), name='profile'),
    path('logout/', logOut, name='logout')
]