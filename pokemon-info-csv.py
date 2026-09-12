import requests
import pandas as pd


def get_pokemon_info(gen):
    """
    Get Pokémon species information based on their generation.

    Args:
        gen: Pokémon generation number.

    Returns:
        pokedex_data: Generation data returned by the PokeAPI
                      when the request succeeds.
        None: If the request fails.
    """

    base_url = "https://pokeapi.co/api/v2/generation/"
    url = f"{base_url}/{gen}"

    response = requests.get(url)

    if response.status_code == 200:
        pokedex_data = response.json()
        return pokedex_data
    else:
        print(f"Failed to retrieve the data. {response.status_code}")
        return None


def get_pokemon_description(pokemon):
    """
    Get the English description of a Pokémon.

    Args:
        pokemon: Pokémon information from the generation data.

    Returns:
        Dictionary containing the Pokémon ID, name, and description.
    """

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

        return {
            "ID": pokemon_data["id"],
            "Name": pokemon_data["name"].title(),
            "Description": description
        }

    else:
        print(
            f"Failed to retrieve {pokemon['name']}. "
            f"{pokemon_response.status_code}"
        )
        return None


def save_to_csv(data, filename):
    """
    Convert the collected data into a Pandas DataFrame
    and save it as a CSV file.

    Args:
        data: List of Pokémon data.
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

pokedex_info = get_pokemon_info(gen)

if pokedex_info:
    rows = []

    for pokemon in pokedex_info["pokemon_species"]:

        pokemon_data = get_pokemon_description(pokemon)

        if pokemon_data:
            rows.append(pokemon_data)

    # Save the data to CSV
    df = save_to_csv(
        rows,
        "pokemon_descriptions_generation_1.csv"
    )

    print("Data successfully saved!")

    # Display the data
    print(df)