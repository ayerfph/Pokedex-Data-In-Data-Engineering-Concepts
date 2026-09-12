import requests
import json


def get_pokemon_info(gen):
    """
    Get Pokémon information based on their generation.

    Args:
        gen: Pokémon generation number.

    Returns:
        pokedex_data: Generation data returned by the PokeAPI.
        None: If the request fails.
    """

    base_url = "https://pokeapi.co/api/v2/generation/"
    url = f"{base_url}/{gen}"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve the data. {response.status_code}")
        return None


def get_pokemon_data(pokemon):
    """
    Get information about a single Pokémon.

    Args:
        pokemon: Pokémon information from the generation data.

    Returns:
        Dictionary containing the Pokémon's information.
    """

    # Use the Pokémon name to access the regular Pokémon endpoint
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon['name']}"

    pokemon_response = requests.get(url)

    if pokemon_response.status_code == 200:

        pokemon_data = pokemon_response.json()

        types = ", ".join(
            pokemon_type["type"]["name"]
            for pokemon_type in pokemon_data["types"]
        )

        abilities = ", ".join(
            ability["ability"]["name"]
            for ability in pokemon_data["abilities"]
        )

        return {
            "ID": pokemon_data["id"],
            "Name": pokemon_data["name"].title(),
            "Type": types,
            "Abilities": abilities
        }

    else:
        print(
            f"Failed to retrieve {pokemon['name']}. "
            f"{pokemon_response.status_code}"
        )

        return None


def save_to_json(data, filename):
    """
    Save the collected Pokémon data to a JSON file.

    Args:
        data: List of Pokémon dictionaries.
        filename: Name of the JSON file.
    """

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# -----------------------------------
# Main Program
# -----------------------------------

gen = "1"

pokedex_info = get_pokemon_info(gen)

if pokedex_info:

    rows = []

    for pokemon in pokedex_info["pokemon_species"]:

        pokemon_data = get_pokemon_data(pokemon)

        if pokemon_data:
            rows.append(pokemon_data)

    save_to_json(
        rows,
        "pokemon_info_generation_1.json"
    )

    print("Pokemon information successfully saved!")