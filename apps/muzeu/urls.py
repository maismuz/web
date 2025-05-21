from apps.muzeu.views import *
from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
<<<<<<< HEAD
    
=======
>>>>>>> origin/develop
]
