from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from .models import Profession, Skill
from .serializers import SkillStatsSerializer
from .tasks import search_vacancies


class ProfessionSkillsAPIView(APIView):
    def get(self, request, profession_id):
        try:
            profession = Profession.objects.get(id=profession_id)
        except Profession.DoesNotExist:
            return Response({"error": "Профессия не найдена"}, status=404)

        skills = Skill.objects.filter(vacancies__profession=profession) \
                              .annotate(mention_count=Count('vacancies')) \
                              .order_by('-mention_count')

        serializer = SkillStatsSerializer(skills, many=True)
        return Response({
            "profession": profession.name,
            "skills": serializer.data
        })

class ParseVacanciesAPIView(APIView):
    def post(self, request, profession_id):
        try:
            profession = Profession.objects.get(id=profession_id)
        except Profession.DoesNotExist:
            return Response({"error": "Профессия не найдена"}, status=404)

        search_vacancies.delay(profession_id)
        
        return Response({
            "message": f"Парсинг вакансий для '{profession.name}' запущен в фоне."
        })