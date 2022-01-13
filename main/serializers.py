from rest_framework import serializers
from .models import Movie, Genre, Rating


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
