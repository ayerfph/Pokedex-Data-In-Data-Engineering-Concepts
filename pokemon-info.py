import requests
 
def get_pokemon_generation(gen):
    """
    Hello Welcome to the code! My goal of this project is to explore getting data
    from API, and practicing DRY (Don't Repeat Yourself) code principle.

    Args:
        gen: Pokemon listed based on their generation (Pokedex reference).

    Returns:
        pokedex_data: The generation data returned by the PokeAPI when the request succeeds.
        If the request fails, it will show the error status code.

    Notes: The output of this code was to get the data of all pokemon in gen 1.
    """
    base_url = "https://pokeapi.co/api/v2/generation/"
    url = f"{base_url}/{gen}"
    response = requests.get(url)

    if response.status_code == 200:
        pokedex_data = response.json()
        #print(pokedex_data)
        return pokedex_data
    else:
        print(f"Failed to retrieve the data. {response.status_code}")

gen = "1"
pokedex_info = get_pokemon_generation(gen)

if pokedex_info:
    print("Pokémon from generation 1:") # Title ref

    # Getting the data 
    for pokemon in pokedex_info["pokemon_species"]:
        pokemon_response = requests.get(
            f"https://pokeapi.co/api/v2/pokemon/{pokemon['name']}"
        )
        
        pokemon_data = pokemon_response.json()
        types = ", ".join(
            pokemon_type["type"]["name"]
            for pokemon_type in pokemon_data["types"]
        )
        abilities = ", ".join(
            ability["ability"]["name"]
            for ability in pokemon_data["abilities"]
        )

        print(
            f"Name: {pokemon_data['name'].title()}\n"
            f"ID: {pokemon_data['id']}\n"
            f"Type: {types}\n"
            f"Abilities: {abilities}\n"
        )
        
