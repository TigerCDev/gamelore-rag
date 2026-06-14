from django.db import models

class Studio(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=50)
    founded_year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class Platform(models.Model):
    name = models.CharField(max_length=50)


class Game(models.Model):
    title = models.CharField(max_length=255)
    release_year = models.IntegerField()
    studio = models.ForeignKey(Studio, on_delete=models.SET_NULL, null=True)
    synopsis = models.TextField()
    engine = models.CharField(max_length=50)
    platform = models.ManyToManyField(Platform)
    created_at = models.DateTimeField(auto_now_add=True)


class Person(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=50)
    games = models.ManyToManyField(Game)


class Award(models.Model):
    name = models.CharField(max_length=50)
    year = models.IntegerField()
    ceremony = models.CharField(max_length=50)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
