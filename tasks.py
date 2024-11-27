import geopandas as gpd
import pandas as pd
from invoke import task


@task
def process(c):
    print("Merging US States shapefile with CSV data...")
    states = gpd.read_file('data/cb_2018_us_state_20m/cb_2018_us_state_20m.shp')

    gpd.GeoDataFrame(
        states
        .merge(pd.read_csv('data/cost_of_living.csv'), how="left", left_on="NAME", right_on="State")
        .merge(pd.read_csv('data/education.csv'), how="left", left_on="NAME", right_on="State",
               suffixes=("", "_education"))
        .merge(pd.read_csv('data/election.csv'), how="left", left_on="NAME", right_on="State",
               suffixes=("", "_election"))
        .merge(pd.read_csv('data/fiber.csv'), how="left", left_on="NAME", right_on="State", suffixes=("", "_fiber"))
        .merge(pd.read_csv('data/homicides.csv'), how="left", left_on="NAME", right_on="State",
               suffixes=("", "_homicides"))
        .merge(pd.read_csv('data/marijuana.csv'), how="left", left_on="NAME", right_on="State",
               suffixes=("", "_marijuana"))
        .merge(pd.read_csv('data/abortion.csv'), how="left", left_on="NAME", right_on="State",
               suffixes=("", "_abortion"))
        .drop(columns=[
            "State", "State_education", "State_election", "State_fiber", "State_homicides", "State_marijuana",
            "State_abortion"
        ])
    ).to_crs(epsg=4326).to_file("static/states_data.geojson", driver="GeoJSON")

    print("Done!")
