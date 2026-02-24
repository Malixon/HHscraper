from django.urls import path
from .views import ProfessionSkillsAPIView, ParseVacanciesAPIView

urlpatterns = [
    path('professions/<int:profession_id>/skills/', ProfessionSkillsAPIView.as_view()),
    path('professions/<int:profession_id>/parse/', ParseVacanciesAPIView.as_view()),
]