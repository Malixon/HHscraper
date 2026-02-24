import requests
from celery import shared_task
from django.db import transaction
from .models import Profession, Vacancy, Skill


HEADERS = {'User-Agent': 'HHScraper/1.0 (your_email@example.com)'}

@shared_task
def process_single_vacancy(hh_vacancy_id, profession_id):
    
    url = f'https://api.hh.ru/vacancies/{hh_vacancy_id}'
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        return f"Ошибка получения вакансии {hh_vacancy_id}"

    data = response.json()
    profession = Profession.objects.get(id=profession_id)
    

    with transaction.atomic():
        vacancy, created = Vacancy.objects.get_or_create(
            hh_id=hh_vacancy_id,
            defaults={'title': data.get('name', 'Без названия'), 'profession': profession}
        )
        

        if not created:
            return f"Вакансия {hh_vacancy_id} уже существует."


        key_skills = data.get('key_skills', [])
        for skill_data in key_skills:
            skill_name = skill_data.get('name')

            skill_obj, _ = Skill.objects.get_or_create(name=skill_name)
            vacancy.skills.add(skill_obj)
            
    return f"Вакансия {hh_vacancy_id} успешно обработана."


@shared_task
def search_vacancies(profession_id):

    profession = Profession.objects.get(id=profession_id)
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': profession.search_query,
        'per_page': 50, 
        'page': 0
    }
    
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        items = response.json().get('items', [])
        for item in items:

            process_single_vacancy.delay(item['id'], profession.id)
            
        return f"Запущена обработка {len(items)} вакансий для {profession.name}."
    return "Ошибка поиска вакансий."