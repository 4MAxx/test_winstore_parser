from django.urls import path
from win_store_parser.views import home

urlpatterns = [
    path('', home, name='home'),
]