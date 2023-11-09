import numpy as np
import pandas as pd


def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in km
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c

    return distance


def calculate_distance_to_facilities(data):
    existing_mrt_df = pd.read_csv(
        "Datasets/auxiliary-data/sg-mrt-existing-stations.csv"
    )
    shopping_malls_df = pd.read_csv("Datasets/auxiliary-data/sg-shopping-malls.csv")
    primary_schools_df = pd.read_csv("Datasets/auxiliary-data/sg-primary-schools.csv")

    # Calculate distances to existing MRT stations
    property_latitudes = data["latitude"].values
    property_longitudes = data["longitude"].values
    existing_mrt_latitudes = existing_mrt_df["latitude"].values
    existing_mrt_longitudes = existing_mrt_df["longitude"].values
    shopping_malls_latitudes = shopping_malls_df["latitude"].values
    shopping_malls_longitudes = shopping_malls_df["longitude"].values
    primary_schools_latitudes = primary_schools_df["latitude"].values
    primary_schools_longitudes = primary_schools_df["longitude"].values

    # Calculate distances
    distances_to_existing_mrt = haversine(
        property_latitudes[:, np.newaxis],
        property_longitudes[:, np.newaxis],
        existing_mrt_latitudes,
        existing_mrt_longitudes,
    )

    distances_to_shopping_malls = haversine(
        property_latitudes[:, np.newaxis],
        property_longitudes[:, np.newaxis],
        shopping_malls_latitudes,
        shopping_malls_longitudes,
    )

    distances_to_primary_schools = haversine(
        property_latitudes[:, np.newaxis],
        property_longitudes[:, np.newaxis],
        primary_schools_latitudes,
        primary_schools_longitudes,
    )

    # Find the minimum distances
    min_distances_to_existing_mrt = np.min(distances_to_existing_mrt, axis=1)
    min_distances_to_shopping_mall = np.min(distances_to_shopping_malls, axis=1)
    min_distances_to_primary_school = np.min(distances_to_primary_schools, axis=1)

    # Add the minimum distance as new features 'distance_to_nearest_existing_mrt', 'distance_to_nearest_shopping_mall', 'distance_to_nearest_primary_school'
    data["distance_to_nearest_existing_mrt"] = min_distances_to_existing_mrt
    data["distance_to_nearest_shopping_mall"] = min_distances_to_shopping_mall
    # data["distance_to_nearest_primary_school"] = min_distances_to_primary_school

    return data
