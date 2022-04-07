from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(AnimalCategory)
class AnimalCategoryModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'animal_count')


@admin.register(Animal)
class AnimalCategoryModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'age',  'species', 'category')