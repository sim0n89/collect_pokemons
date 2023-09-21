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
	pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
	appeared_at = models.DateTimeField(null=True, blank=True)
	disappeared_at = models.DateTimeField(null=True, blank=True)
	def __str__(self):
		return f"{self.pokemon.title}: {self.lat} - {self.lon}"
	