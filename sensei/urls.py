from django.urls import path,include
from . import views

urlpatterns = [

    path('',views.sensei),
    path('classroom/',views.my_view,name='classroom'),
    
]
