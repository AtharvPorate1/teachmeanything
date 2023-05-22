from django.urls import path,include
from . import views



app_name = 'sensei'

urlpatterns = [

    path('',views.sensei,name='teacher'),
    path('classroom/',views.my_view,name='classroom'),
    path('completed/',views.success,name='completed'),
    
]
