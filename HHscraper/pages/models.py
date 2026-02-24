from django.db import models

class Profession(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название профессии")
    search_query = models.CharField(max_length=100, verbose_name="Поисковой запрос для HH")

    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название навыка")

    def __str__(self):
        return self.name

class Vacancy(models.Model):
    hh_id = models.CharField(max_length=50, unique=True, verbose_name="ID на HH.ru")
    title = models.CharField(max_length=200, verbose_name="Название вакансии")
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.ManyToManyField(Skill, related_name='vacancies')
    
    def __str__(self):
        return self.title