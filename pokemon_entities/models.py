from django.db import models

class Pokemon(models.Model):
	title = models.CharField('Название (рус.)',max_length=255)
	title_en = models.CharField('Название (англ.)', max_length=255, blank=True)
	title_jp = models.CharField('Название (яп.)', max_length=255, blank=True)
	image = models.ImageField('Картинка',blank=True,null=True, upload_to='pokemons')
	description = models.TextField('Описание',blank=True)

	previous_evolution = models.ForeignKey(
        "Pokemon",
				verbose_name='Предыдущая эволюция',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="next_evolutions",
    )

	def __str__(self):
		return self.title
	
	class Meta:
		verbose_name = 'Тип покемона'
		verbose_name_plural = 'Типы покемонов'
	
class PokemonEntity(models.Model):
	lat = models.FloatField('Широта')
	lon = models.FloatField('Долгота')
	pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
	appeared_at = models.DateTimeField('Время появления', null=True, blank=True)
	disappeared_at = models.DateTimeField('Время исчезновения', null=True, blank=True)
	level = models.IntegerField('Уровень',default=1)
	helth = models.IntegerField('Здоровье', default=100)
	strength = models.IntegerField('Атака', default=1)
	defence = models.IntegerField('Защита', default=1)
	stamina = models.IntegerField('Выносливость',default=1)
	
	def __str__(self):
		return f"{self.pokemon.title}: {self.lat} - {self.lon}"
	
	class Meta:
		verbose_name = 'Покемон'
		verbose_name_plural = 'Покемоны'