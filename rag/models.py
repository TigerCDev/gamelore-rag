from django.db import models
from pgvector.django import VectorField
from games.models import Game



class DocumentChunk(models.Model):
    content = models.TextField()
    embedding = VectorField(dimensions=1536)
    source_url = models.CharField(max_length=250)
    source_type = models.CharField(max_length=50)
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

