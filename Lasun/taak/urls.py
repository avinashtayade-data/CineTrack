from django.urls import path
from .import views

#localhost:8000/taak
#localhost:8000/chai/order
urlpatterns = [
    path('',views.all_taak,name='all_taak'),
    path('<int:taak_id>/',views.taak_detail,name='taak_detail'),
]
