import folium
import json
from django.utils import timezone
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from .models import PokemonEntity, Pokemon


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
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


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    time_now = timezone.now()
    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lte = time_now,
        disappeared_at__gte = time_now 
    )

    for pokemon_entity in pokemon_entities:
        pokemon_image = pokemon_entity.pokemon.image
        if pokemon_image:
            image_url = request.build_absolute_uri(pokemon_image.url)
        else:
            image_url = DEFAULT_IMAGE_URL

        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            image_url,
        )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemon_image = pokemon.image
        if pokemon_image:
            image_url = request.build_absolute_uri(pokemon_image.url)
        else:
            image_url = DEFAULT_IMAGE_URL
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': image_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    time_now = timezone.now()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    if pokemon.image:
        image_url = request.build_absolute_uri(pokemon.image.url)
    else:
        image_url = DEFAULT_IMAGE_URL

    pokemon_entities = PokemonEntity.objects.filter(
        pokemon=pokemon,
        appeared_at__lte=time_now,
        disappeared_at__gte=time_now,
    )

    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            image_url
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': {
            'pokemon_id': pokemon.id,
            'img_url': image_url,
            'title_ru': pokemon.title,
            'description': pokemon.description,
        }
    })
