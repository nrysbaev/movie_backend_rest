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


@api_view(['GET'])
def movie_list_view(request):
    movies = Movie.objects.all()
    data = MovieSerializer(movies, many=True).data
    return Response(data=data)


@api_view(['GET'])
def movie_detail_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'movie not found'})
    data = MovieDetailSerializer(movie, many=False).data
    return Response(data=data)
