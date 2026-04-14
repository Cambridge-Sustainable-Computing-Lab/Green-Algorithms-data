import pandas as pd
import argparse

def map_continents(df_without_continents: pd.DataFrame, df_with_continents: pd.DataFrame, 
                   country_col: str, continent_col: str, edge_cases: dict = None) -> pd.DataFrame:
    """
    Map the continents to the electricity map data.

    Parameters
    ----------
    df_without_continents : pd.DataFrame
        The electricity map data without continent information.
    df_with_continents : pd.DataFrame
        The continent-country mapping data.
    country_col : str
        The column name for the country information.
    continent_col : str
        The column name for the continent information.
    edge_cases : dict, optional
        A dictionary of edge cases for country-continent mapping.
    Returns
    -------
    pd.DataFrame
        The electricity map data with the continents mapped.
    """

    df = df_with_continents[[country_col, continent_col]]
    continents_country_map = dict(zip(df[country_col], df[continent_col]))
    if edge_cases:
        continents_country_map.update(edge_cases)

    split_iso = df_without_continents['Zone id'].str.split('-').str[0] # Pick only country code from 'Zone id' (e.g., 'DE' from 'DE-AT')
    df_without_continents['Continent'] = split_iso.map(continents_country_map)

    return df_without_continents

if __name__ == "__main__":
    # Mapping ISO-alpha2 country codes to continents using the UN  M49 standard, with some edge cases for specific codes.
    # https://unstats.un.org/unsd/methodology/m49/

    argparser = argparse.ArgumentParser(description="Map continents to the electricity map data.")
    
    argparser.add_argument("--electricitymapcsv", help='Path to the electricity map CSV file.', default='CI-electricitymap-yearly_2024.csv')
    argparser.add_argument("--continentmappingcsv", help='Path to the continent mapping CSV file.', required=False, default='UNSD_M49.csv')
    argparser.add_argument("--savepath", help='Path to save the output CSV file.', required=False, default='CI-electricitymap-with-continents.csv')

    args = argparser.parse_args()

    try:
        df_elec_maps = pd.read_csv(args.electricitymapcsv)
        df_continents_map = pd.read_csv(args.continentmappingcsv, delimiter=';')
        edge_cases = {
            "XK": "Europe",
            "TW": "Asia",
            "GLOBAL": "World"
        }
        df_with_continents = map_continents(df_elec_maps, df_continents_map, 'ISO-alpha2 Code', 'Region Name', edge_cases)
        df_with_continents.to_csv(args.savepath, index=False)
        print(f"Continents mapped successfully and saved to '{args.savepath}'.")

    except Exception as e:
        print(f"Error occurred during continent mapping: {e}")

