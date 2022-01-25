from rest_framework import serializers
from .models import Movie, Genre, Rating
from rest_framework.exceptions import ValidationError


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class RatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'text', 'value']


class MovieSerializer(serializers.ModelSerializer):
    # genres = GenresSerializer(many=True)
    # ratings = RatingsSerializer(many=True)
    ratings = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        # fields = '__all__'
        # fields = 'id name'.split()
        fields = ['id', 'name', 'genres', 'ratings', 'count_genres', 'rating']

    def get_ratings(self, movie):
        # rate = movie.ratings.filter(value__gt=3)
        rate = Rating.objects.filter(movie=movie, value__gt=3)
        data = RatingsSerializer(rate, many=True).data
        return data

    def get_genres(self, movie):
        # filtered_genres = movie.genres.filter(is_active=True)
        # data = GenresSerializer(filtered_genres, many=True).data
        return GenresSerializer(movie.genres.filter(is_active=True), many=True).data


class MovieDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'name', 'description', 'duration', 'count_genres']


class GenreCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    is_active = serializers.BooleanField()


class MovieCreateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=3, max_length=10)
    description = serializers.CharField(required=False)
    duration = serializers.IntegerField(default=0)
    is_active = serializers.BooleanField()
    genres = serializers.ListField(child=serializers.IntegerField())
    created_genres = serializers.ListField(child=GenreCreateSerializer())

    def validate_name(self, value):
        movies = Movie.objects.filter(name=value)
        if movies:
            raise ValidationError('Movie already exists!')
        return value

    # При кастомной валидации всех полей (attrs) в конце надо возвращать также все поля (attrs)
    # def validate(self, attrs):
    #     name = attrs['name']
    #     movies = Movie.objects.filter(name=name)
    #     if movies:
    #         raise ValidationError('Movie already exists!')
    #     return attrs

    # def validate_name(self, name):
    #     for i in name:
    #         if 1040 <= ord(i) <= 1103:
    #             raise ValidationError('Please use english only')
    #     return name
