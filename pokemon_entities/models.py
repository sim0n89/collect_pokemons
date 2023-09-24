from django.db import models


class Pokemon(models.Model):
    title = models.CharField("Название (рус.)", max_length=255)
    title_en = models.CharField("Название (англ.)", max_length=255, blank=True)
    title_jp = models.CharField("Название (яп.)", max_length=255, blank=True)
    image = models.ImageField("Картинка", blank=True, null=True, 
                              upload_to="pokemons")
    description = models.TextField("Описание", blank=True)

    previous_evolution = models.ForeignKey(
        "Pokemon",
        verbose_name="Предыдущая эволюция",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="next_evolutions",
    )

    class Meta:
        verbose_name = "Тип покемона"
        verbose_name_plural = "Типы покемонов"

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    lat = models.FloatField("Широта")
    lon = models.FloatField("Долгота")
    appeared_at = models.DateTimeField("Время появления", null=True,
                                       blank=True)
    disappeared_at = models.DateTimeField("Время исчезновения", null=True,
                                          blank=True)
    level = models.IntegerField("Уровень", blank=True, null=True)
    helth = models.IntegerField("Здоровье", blank=True, null=True)
    strength = models.IntegerField("Атака", blank=True, null=True)
    defence = models.IntegerField("Защита", blank=True, null=True)
    stamina = models.IntegerField("Выносливость", blank=True, null=True)
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name="Тип покемона",
        related_name="entities",
    )

    class Meta:
        verbose_name = "Покемон"
        verbose_name_plural = "Покемоны"

    def __str__(self):
        return f"{self.pokemon_type.title}: {self.lat} - {self.lon}"
