from django.urls import URLPattern, path
from . import views

urlpatterns = [
    path('',views.login, name='login'),
    path('signup', views.signup, name='signup')
]