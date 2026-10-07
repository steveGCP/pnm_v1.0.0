from django.urls import path
from . import views

#Define a list of URL patterns

urlpatterns=[
    path('', views.index, name = "index"),
    path('login/', views.login, name = "login"), 
    path('signUp/', views.signUp, name ="signUp"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('matching/', views.start_matching, name= "matchmakin_results")
]
