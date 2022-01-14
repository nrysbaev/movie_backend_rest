from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MovieSerializer, MovieDetailSerializer
from .models import Movie


@api_view(['GET'])
def index(request):
    context = {
        'number': 100,
        'float': 1.11,
        'text': 'Hello World',
        'list': [1, 2, 3],
        'dict': {'name': 'Aziz'}
    }
    return Response(data=context, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def movie_list_view(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        data = MovieSerializer(movies, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        name = request.data['name']
        description = request.data.get('description', '')
        duration = request.data['duration']
        is_active = request.data['is_active']
        genres = request.data['genres']
        movie = Movie.objects.create(
            name=name, description=description, duration=duration,
            is_active=is_active
        )
        movie.genres.set(genres)
        return Response(data=MovieSerializer(movie).data,
                        status=status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE'])
def movie_detail_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'movie not found'})
    if request.method == 'GET':
        data = MovieDetailSerializer(movie, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(data={'message': 'Movie successfully removed!'})
