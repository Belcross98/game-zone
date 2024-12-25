from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.template.defaultfilters import slugify
from django.db.models import Avg

# Create your models here.


class Game(models.Model):

    name = models.CharField(max_length=255)
    genres = models.CharField(max_length=255,blank=True)
    categories = models.CharField(max_length=255,blank=True)
    publishers = models.CharField(max_length=255,blank=True)
    developers = models.CharField(max_length=255,blank=True)
    description = models.TextField(max_length=255,blank=True)
    release_date = models.DateField()
    img_url = models.CharField(max_length=255,blank=True)
    slug = models.SlugField(null=False, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        self.slug = slugify(self.name)
        super(Game, self).save(*args, **kwargs)

    def avg_rating(self):
        return self.ratings.aggregate(Avg('rating'))['rating__avg'] or 0


class Rating(models.Model):

    game = models.ForeignKey(Game, related_name='ratings',
                             null=True, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return f'Rating: {self.rating}, Game: {self.game}'
