from django.db import models  # noqa F401

# your models here
class Pokemon(models.Model):
	title = models.CharField(max_length=255, null=False)
	image = models.ImageField(blank=True, upload_to='pokemons')

	def __str__(self):
		return self.title
	
class PokemonEntity(models.Model):
	lat = models.FloatField()
	lon = models.FloatField()

	def __str__(self):
		return f"{self.lat} - {self.lon}"
	