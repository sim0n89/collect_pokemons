import folium
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .models import PokemonEntity, Pokemon


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision"
    "/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832"
    "&fill=transparent"
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def check_image(request, image):
    if image:
        image_url = request.build_absolute_uri(image.url)
    else:
        image_url = DEFAULT_IMAGE_URL
    return image_url


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    time_now = timezone.now()
    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lte=time_now, disappeared_at__gte=time_now
    )

    for pokemon_entity in pokemon_entities:
        pokemon_image = pokemon_entity.pokemon.image
        image_url = check_image(request, pokemon_image)
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            image_url,
        )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemon_image = pokemon.image
        image_url = check_image(request, pokemon_image)
        pokemons_on_page.append(
            {
                "pokemon_id": pokemon.id,
                "img_url": image_url,
                "title_ru": pokemon.title,
            }
        )

    return render(
        request,
        "mainpage.html",
        context={
            "map": folium_map._repr_html_(),
            "pokemons": pokemons_on_page,
        },
    )


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    time_now = timezone.now()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    image_url = check_image(request, pokemon.image)
    pokemon_entities = PokemonEntity.objects.filter(
        pokemon=pokemon,
        appeared_at__lte=time_now,
        disappeared_at__gte=time_now,
    )

    for pokemon_entity in pokemon_entities:
        add_pokemon(folium_map,
                    pokemon_entity.lat,
                    pokemon_entity.lon,
                    image_url
                    )

    previous_evolution = {}
    previous_pokemon = pokemon.previous_evolution
    if previous_pokemon:
        previous_evolution = {
            "title_ru": previous_pokemon.title,
            "pokemon_id": previous_pokemon.id,
            "img_url": request.build_absolute_uri(previous_pokemon.image.url),
            "description": previous_pokemon.description,
            "title_en": previous_pokemon.title_en,
            "title_jp": previous_pokemon.title_jp,
        }

    next_evolution = {}
    next_pokemon = pokemon.next_evolutions.all().first()
    if next_pokemon:
        next_evolution = {
            "title_ru": next_pokemon.title,
            "pokemon_id": next_pokemon.id,
            "img_url": request.build_absolute_uri(next_pokemon.image.url),
        }

    return render(
        request,
        "pokemon.html",
        context={
            "map": folium_map._repr_html_(),
            "pokemon": {
                "pokemon_id": pokemon.id,
                "img_url": image_url,
                "title_ru": pokemon.title,
                "description": pokemon.description,
                "title_en": pokemon.title_en,
                "title_jp": pokemon.title_jp,
                "previous_evolution": previous_evolution,
                "next_evolution": next_evolution,
            },
        },
    )
