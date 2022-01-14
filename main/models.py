from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField()
    duration = models.IntegerField()
    genres = models.ManyToManyField(Genre, blank=True)

    def count_genres(self):
        return self.genres.filter(is_active=True).count()

    def rating(self):
        c = 0
        for i in self.ratings.all():
            c += i.value
        try:
            return c / self.ratings.all().count()
        except ZeroDivisionError:
            return 0

    def __str__(self):
        return self.name


STARS = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)


class Rating(models.Model):
    text = models.CharField(max_length=100)
    value = models.IntegerField(choices=STARS)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,
                              related_name='ratings')

    def __str__(self):
        return self.text
