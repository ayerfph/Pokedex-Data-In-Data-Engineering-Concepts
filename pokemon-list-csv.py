import requests
import pandas as pd


def get_pokemon_generation(gen):
    """
    Get Pokémon data based on their generation from the PokeAPI.

    Args:
        gen: Pokémon generation number.

    Returns:
        pokedex_data: Generation data returned by the PokeAPI
                      when the request succeeds.
        None: If the request fails.
    """
    base_url = "https://pokeapi.co/api/v2/generation"
    url = f"{base_url}/{gen}"

    response = requests.get(url)

    if response.status_code == 200:
        pokedex_data = response.json()
        return pokedex_data
    else:
        print(f"Failed to retrieve the data. Status code: {response.status_code}")
        return None


def get_pokemon_data(pokemon_name):
    """
    Get and process information about a single Pokémon.

    Args:
        pokemon_name: Name of the Pokémon.

    Returns:
        Dictionary containing the Pokémon's name, ID, types, and abilities.
    """
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"

    response = requests.get(url)

    if response.status_code == 200:
        pokemon_data = response.json()

        types = ", ".join(
            pokemon_type["type"]["name"]
            for pokemon_type in pokemon_data["types"]
        )

        abilities = ", ".join(
            ability["ability"]["name"]
            for ability in pokemon_data["abilities"]
        )

        return {
            "Name": pokemon_data["name"].title(),
            "ID": pokemon_data["id"],
            "Type": types,
            "Abilities": abilities
        }

    else:
        print(
            f"Failed to retrieve {pokemon_name}. "
            f"Status code: {response.status_code}"
        )
        return None


def save_to_csv(data, filename):
    """
    Convert Pokémon data into a Pandas DataFrame
    and save it as a CSV file.

    Args:
        data: List of Pokémon dictionaries.
        filename: Name of the CSV file.

    Returns:
        Pandas DataFrame containing the Pokémon data.
    """
    df = pd.DataFrame(data)

    df.to_csv(filename, index=False)

    return df


# -----------------------------------
# Main Program
# -----------------------------------

gen = "1"

pokedex_info = get_pokemon_generation(gen)

if pokedex_info:
    print(f"Pokémon from generation {gen}:")

    pokemon_list = []

    # Get information for every Pokémon
    for pokemon in pokedex_info["pokemon_species"]:

        pokemon_data = get_pokemon_data(pokemon["name"])

        if pokemon_data:
            pokemon_list.append(pokemon_data)

    # Convert the data to CSV
    df = save_to_csv(
        pokemon_list,
        "pokemon_generation_1.csv"
    )

    print("\nData successfully saved to pokemon_generation_1.csv")

    print("\nPreview:")
    print(df)