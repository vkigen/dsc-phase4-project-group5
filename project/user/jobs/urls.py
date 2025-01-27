from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [
    path("", views.home, name="home"),  # Form submission page
    path("results/", views.results, name="results"),  # Results display page
    path('process_data/', views.process_data, name='process_data'),
]
