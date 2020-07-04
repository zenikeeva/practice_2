from django.urls import path
from model2 import view

urlpatterns = [
    path('', view.index, name=''),
    path('facescount', view.facescount, name=''),
]
