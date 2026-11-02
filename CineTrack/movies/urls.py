from django.urls import path
from .import views

urlpatterns = [
path('', views.home, name='home'),
path('add/', views.add_movie, name='add_movie'),
path('<int:movie_id>/', views.movie_detail, name='movie_detail'),
path('<int:movie_id>/edit/', views.edit_movie, name='edit_movie'),
path('<int:movie_id>/delete/', views.delete_movie, name='delete_movie'),
path('register/', views.register, name='register'),
path('verify-otp/', views.verify_otp, name='verify_otp'),
path('resend-otp/', views.resend_otp, name='resend_otp'),
]
