from django.urls import path
from recsapp import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('form/', views.inputForm, name='inputForm'),
    path('submissionsuccessful/', views.submitFilter, name='submitFilter'),
    path('processing/', views.processing, name='processing'),
    path('results/', views.post_processing, name='results'),
]