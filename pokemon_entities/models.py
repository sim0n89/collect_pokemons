from django.db import models  # noqa F401

# your models here
class Pokemon(models.Model):
	title = models.CharField(max_length=255, null=False)
	title_en = models.CharField( max_length=255, blank=True)
	title_jp = models.CharField( max_length=255, blank=True)
	image = models.ImageField(blank=True,null=True, upload_to='pokemons')
	description = models.TextField(blank=True)

	previous_evolution = models.ForeignKey(
        "Pokemon",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="next_evolutions",
    )

	def __str__(self):
		return self.title
	
class PokemonEntity(models.Model):
	lat = models.FloatField()
	lon = models.FloatField()
	pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
	appeared_at = models.DateTimeField(null=True, blank=True)
	disappeared_at = models.DateTimeField(null=True, blank=True)
	level = models.IntegerField(default=1)
	helth = models.IntegerField(default=100)
	strength = models.IntegerField(default=1)
	defence = models.IntegerField(default=1)
	stamina = models.IntegerField(default=1)
	
	def __str__(self):
		return f"{self.pokemon.title}: {self.lat} - {self.lon}"
	