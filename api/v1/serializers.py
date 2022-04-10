from rest_framework.serializers import ModelSerializer

from store.models import Animal, AnimalCategory


class AnimalCategorySerializer(ModelSerializer):
    class Meta:
        model = AnimalCategory
        fields = (
            'id',
            'title'
        )


class AnimalListSerializer(ModelSerializer):
    class Meta:
        model = Animal
        fields = (
            'id',
            'title',
            'species',
        )


class AnimalDetailSerializer(ModelSerializer):
    category = AnimalCategorySerializer()

    class Meta:
        model = Animal
        fields = (
            'id',
            'title',
            'image',
            'description',
            'age',
            'species',
            'category'
        )