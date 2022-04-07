from django.db import models

# Create your models here.
from skillboxcatapi.base_model import Base


class AnimalCategory(Base):
    title = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'Категория животных'
        verbose_name_plural = 'Категория животных'
        ordering = ['title']

    def __str__(self):
        return f'{self.title}'

    @property
    def animal_count(self):
        """
        Return number of animals in this category
        :return:
        """

        return Animal.objects.filter(category=self).count()


class Animal(Base):
    title = models.CharField(max_length=255)
    age = models.PositiveIntegerField(default=0)
    description = models.TextField()
    category = models.ForeignKey(AnimalCategory, on_delete=models.PROTECT)
    species = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images')

    class Meta:
        verbose_name = 'Животное'
        verbose_name_plural = 'Животные'
        ordering = ['title']

    def __str__(self):
        return f'{self.title}'