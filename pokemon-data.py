import requests
 
def get_pokemon_info(gen):

    """
        Hello Welcome to the code! My goal of this project is to explore getting data
        from API, and practicing DRY (Don't Repeat Yourself) code principle.
    
        Args:
            gen: Pokemon listed based on their generation (Pokedex reference).
    
        Returns:
            pokedex_data: The generation description data for each pokemon returned by the PokeAPI when the request succeeds.
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
pokedex_info = get_pokemon_info(gen)

if pokedex_info:
    rows = []

    for pokemon in pokedex_info["pokemon_species"]:
        pokemon_response = requests.get(pokemon["url"])

        if pokemon_response.status_code == 200:
            pokemon_data = pokemon_response.json()
            description = next(
                (
                    entry["flavor_text"].replace("\n", " ").replace("\f", " ")
                    for entry in pokemon_data["flavor_text_entries"]
                    if entry["language"]["name"] == "en"
                ),
                "No description available.",
            )
            rows.append((pokemon_data["id"], pokemon_data["name"].title(), description))
        else:
            print(f"Failed to retrieve the data. {pokemon_response.status_code}")

    for pokemon_id, name, description in rows:
        print(
            f"Pokemon: {name}\n"
            f"No. {pokemon_id}\n"
            f"Description: {description}\n"
        )
