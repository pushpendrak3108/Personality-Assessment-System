from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from app2 import views

urlpatterns = [
    path('home/', login_required(TemplateView.as_view(template_name='personality_home.html')), name='personality_home'),
    path('aptitude/test/', views.AptitudeTest.as_view(), name='aptitude_test'),
    path('aptitude/finished/', TemplateView.as_view(template_name='aptitude_finished.html'), name='aptitude_finished'),
    path('test/', views.PersonalityTest.as_view(), name='personality_test'),
    path('completed/', views.PersonalityCompleted.as_view(), name='personality_completed'),

    path('mbti_home/', login_required(views.mbtitest.as_view()), name='mbti_personality_home'),

]
