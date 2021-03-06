from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MovieSerializer, MovieDetailSerializer, MovieCreateSerializer, GenresSerializer
from .models import Movie
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from main.models import Genre
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.models import Token


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
    print(request.user)
    if request.method == 'GET':
        movies = Movie.objects.all()
        data = MovieSerializer(movies, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializer = MovieCreateSerializer(data=request.data)
        print('request.data:', request.data)
        print('serializer.initial_data:', serializer.initial_data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={'errors': serializer.errors})
        print('serializer.validated_data:', serializer.validated_data)
        print('errors:', serializer.errors)
        name = serializer.validated_data['name']
        description = serializer.validated_data.get('description', '')
        duration = serializer.validated_data['duration']
        is_active = serializer.validated_data['is_active']
        genres = serializer.validated_data['genres']
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


class GenreCreateListAPIView(ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    pagination_class = PageNumberPagination

    # def list(self, request, *args, **kwargs):
    # def create(self, request, *args, **kwargs):


class GenreDetailUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    lookup_field = 'pk'


class LoginAPIView(GenericAPIView):
    def post(self, request):
        user = authenticate(**request.data)
        if user:
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            return Response(data={'token': token.key})
        return Response(data={'User not found'}, status=404)
