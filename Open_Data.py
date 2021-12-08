import os
import os.path
from os import path
import time

import pandas as pd
import numpy as np
import geopandas as gpd
from geopandas import GeoDataFrame
from shapely.geometry import Point, LineString
# import geoplot as gplt

from sodapy import Socrata
import json
import matplotlib.pyplot as plt
import folium
from IPython.display import display

DATASET_ID = {
"CarCrashes": "h9gi-nx95",
"LiveTraffic": "i4gi-tjb9"
}

FIG_WIDTH = 16
FIG_HEIGHT = 9


class NYC_OPEN_DATA():
    '''
    The superclass to process datasets obtained from NYC Open Data.
    Child classes vary depending on the actual dataset.
    '''
    def __init__(self, ds_name, max_size):

        self.data_set_name = ds_name
        self.size_limit = max_size

        self.all_infos = {"user": "9ez7-sax2", "pass": "Uj6-ZGK?EXp*BZb^L6y%", "app_token": "fYoPDh2EAmIxCQzaeUvjuKYW6"}

        # Client Authentification using Socrata:
        self.client = Socrata("data.cityofnewyork.us",
        self.all_infos["app_token"],
        username = self.all_infos["user"],
        password = self.all_infos["pass"])

        self.client.timeout = self.size_limit * 15 # set time out as a minute

        self.results = []
        self.results_df = pd.DataFrame()

    def needs_update(self):
        if path.exists((self.data_set_name + "_results.txt")):
            f_elapsed_t = time.time() - os.path.getmtime((self.data_set_name + "_results.txt"))

            if f_elapsed_t > 3600:
                # if the last update (of data) took place
                # more than an hour ago
                return True
            else:
                return False
        else:
            return True

    def read_data(self):
        # checks whether data needs to be updated

        self.results = self.client.get(DATASET_ID[self.data_set_name], limit = self.size_limit)

        for item in self.results:
            if "-73.8389340.75562" in item["link_points"]:
                item["link_points"] = item["link_points"].replace("-73.8389340.75562", "-73.83893 40.75562")

            if "-73.83621140.81201" in item["link_points"]:
                item["link_points"] = item["link_points"].replace("-73.83621140.81201", "-73.836211 40.81201")

        # Convert to pandas DataFrame
        self.results_df = pd.DataFrame.from_records(self.results)

class Crashes(NYC_OPEN_DATA):
    '''
    Motor Vehicle Collisions - Crashes
    https://dev.socrata.com/foundry/data.cityofnewyork.us/h9gi-nx95
    '''
    def __init__(self, ds_name, max_size):
        NYC_OPEN_DATA.__init__(self, ds_name, max_size)
        self.read_data()
        self.loc_pairs = pd.DataFrame()
        self.gdf = GeoDataFrame()

    def static_map(self):

        self.loc_pairs.loc[:, ('latitude_float')] = self.results_df['latitude'].apply(lambda x: float(x))
        self.loc_pairs.loc[:, ('longitude_float')] = self.results_df['longitude'].apply(lambda x: float(x))

        self.loc_pairs = self.loc_pairs.dropna() # drops NaN obs
        self.loc_pairs = self.loc_pairs[(self.loc_pairs != 0).all(1)] # drops zero (placeholding) values

        geometry = gpd.points_from_xy(self.loc_pairs['longitude_float'], self.loc_pairs['latitude_float'])
        self.gdf = GeoDataFrame(self.loc_pairs, geometry = geometry)

        # this is a simple map that goes with geopandas
        nyc = gpd.read_file(gpd.datasets.get_path('nybb')) # nyc map (included)
        self.gdf.plot(ax = nyc.to_crs("EPSG:4326").boundary.plot(figsize = (FIG_WIDTH, FIG_HEIGHT), color = "grey"), marker = 'o', color = 'red', markersize = 5)
        plt.show()

class RTraffic(NYC_OPEN_DATA):
    '''
    DOT Traffic Speeds NBE
    https://dev.socrata.com/foundry/data.cityofnewyork.us/i4gi-tjb9
    '''
    def __init__(self, ds_name, max_size):
        NYC_OPEN_DATA.__init__(self, ds_name, max_size)
        self.read_data()
        self.recs = pd.DataFrame()
        self.f_map = folium.Map([40.7, -73.9], zoom_start=10)
        self.pol_df = pd.DataFrame()


    def get_polylines(self):

        self.recs = self.results_df[["speed", "travel_time", "data_as_of", "link_points", "borough", "link_name"]]
        # self.recs["encoded_poly_line"] = self.recs["encoded_poly_line"].apply(lambda x: x.decode("utf-8"))

        # self.recs["decoded_polyline"] = [polyline.decode(item.encode('utf-8').decode('utf-8')) for item in self.recs["encoded_poly_line"]]

        all_pairs = []

        idx = 0

        all_records = GeoDataFrame()

        for row_str in self.recs["link_points"].tolist():

            row_ls = row_str.split(" ")

            pairs_fn = [(float(item.split(",")[0].strip()), float(item.split(",")[1].strip())) \
            for item in row_ls \
            if ((len(item) > 1) \
            and (len(item.split(",")) > 1 ) \
            and (len((item.split(",")[0].strip())) > 7) \
            and (len((item.split(",")[1].strip())) > 7) \
            and ("," in item) \
            and (38 <= float(item.split(",")[0].strip()) <= 42) \
            and (71 <= np.absolute(float(item.split(",")[1].strip())) <= 75) \
            and (item.count(".") <= 2))]
            # exclude blank and incomplete pairs (or pairs with incorrect/partial values)

            longitudes = [item[1] for item in pairs_fn]
            latitudes = [item[0] for item in pairs_fn]

            cam_name = [self.recs["link_name"][idx]] * len(longitudes)

            rt_speed = [self.recs["speed"][idx]] * len(longitudes)

            timestamp = self.recs["data_as_of"][idx]

            place = self.recs["borough"][idx]

            my_temp_df = pd.DataFrame({"longitude": longitudes, "latitude": latitudes,
                                       "names": cam_name,
                                       "rou_speed": rt_speed,
                                       "time_s": timestamp,
                                       "boro": place,
                                       "tr_time": self.recs["travel_time"][idx]
                                      })

            my_temp_df = GeoDataFrame(my_temp_df, geometry = gpd.points_from_xy(longitudes, latitudes, crs="EPSG:4326"))

            if idx == 0:
                all_records = my_temp_df
            else:
                all_records = all_records.append(my_temp_df)

            idx += 1

        #all_records['geometry'].plot()
        # Aggregate these points with the GroupBy
        agg_df = all_records.groupby(['names', 'rou_speed', 'time_s', "boro", "tr_time"])['geometry'].apply(lambda x: LineString(x.tolist()))

        agg_df = GeoDataFrame(agg_df, geometry='geometry').reset_index()
        # print(agg_df.head(200))

        # construct gpd points
        # contiguous_usa = gpd.read_file(gplt.datasets.get_path('contiguous_usa'))
        # nyc = gpd.read_file(gpd.datasets.get_path('nybb')) # nyc map (included)
        # agg_df.plot(ax = nyc.to_crs("EPSG:4326").boundary.plot(figsize = (FIG_WIDTH, FIG_HEIGHT), color = "grey"), marker = 'o', markersize = 5, column = 'names', legend = True, legend_kwds={'loc': 'upper left', 'fontsize': 6})
        # , legend = True, legend_kwds={'loc': 'upper left', 'fontsize': 6}
        # plt.show()

        agg_df.crs = {'init' :'epsg:4326'}

         # for item in all_pairs:
        #     print(item, type(item), '\n\n')
        #     print("******")


        #geo_df = GeoDataFrame({'geometry': self.recs["decoded_polyline"]})
        #geo_df['geometry']= geo_df['geometry'].apply(lambda x: [gpd.points_from_xy(i[1], i[0]) for i in x])
        #print(geo_df)

        # this is a simple map that goes with geopandas
        #nyc = gpd.read_file(gpd.datasets.get_path('nybb')) # nyc map (included)
        #geo_df.plot(ax = nyc.to_crs("EPSG:4326").plot(figsize = (FIG_WIDTH, FIG_HEIGHT), color = "grey"), marker = 'o', color = 'red', markersize = 10)
        #plt.show()

        self.pol_df = agg_df

        return agg_df


    def display_folium(self):

        geo_df = self.get_polylines() # get geo DF to operate upon

        # print(geo_df["geometry"])

        # add the linestrings to be plotted on the folium map
        l_idx = 0
        for l_str in geo_df["geometry"]:

            if float(geo_df['rou_speed'].tolist()[l_idx]) > 25:
                # faster than 25 miles
                this_color = 'darkgreen'
            else:
                this_color = 'darkred'

            folium.Choropleth(
                l_str,
                line_weight=8,
                line_color=this_color,
                key_on='names'
            ).add_to(self.f_map)
            l_idx += 1

        # take starting point for each camera-monitored road
        # e.g. [40.7894406, -73.786291]
        # and keep track of the index!

        # cols of self.recs:
        # "speed", "travel_time", "data_as_of", "link_points", "borough", "link_name"

        row_idx = 0

        for start_pt in self.recs["link_points"].apply(lambda x: [float(item) for item in x.split()[0].split(",")]):


            if float(self.recs["speed"].tolist()[row_idx]) > 25:
                # faster than 25 miles
                travel_color = 'Green (Ave Speed > 25 mph)'
                html_color = 'green'
            else:
                travel_color = 'Red (Ave Speed <= 25 mph)'
                html_color = 'red'

            text_message_long = '''
            This is the starting point of the
            "{lk_nm}"
            camera-monitored road.

            This road belongs to the {bor} borough.
            ---
            As of {date_rec}, it will take on average
            {tr_t} (unit TBD) to travel through this road, with an
            average speed of {s} mph.
            '''.format(lk_nm = self.recs["link_name"].tolist()[row_idx],
                      bor = self.recs["borough"].tolist()[row_idx],
                      date_rec = self.recs["data_as_of"].tolist()[row_idx],
                      tr_t = self.recs["travel_time"].tolist()[row_idx],
                      s = self.recs["speed"].tolist()[row_idx])

            text_message_short = '''
            <p style="color:{html_c};">
            <b>Travel Speed:</b> {clr}
            </p>
            <hr>
            <p><b>Name:</b> {lk_nm}
            </p>
            <p><b>Borough:</b> {bor}
            </p>
            <p><b>Date:</b> {date_rec}
            </p>
            <b>Timestamp:</b> {t_rec}
            <hr>
            <p>
            <b>Travel Time:</b> {tr_t:.2f} minutes.
            </p>
            <p>
            <b>Average Speed:</b> {s} mph
            </p>

            '''.format(lk_nm = self.recs["link_name"].tolist()[row_idx],
                       bor = self.recs["borough"].tolist()[row_idx],
                       date_rec = self.recs["data_as_of"].tolist()[row_idx].split("T")[0],
                       t_rec = self.recs["data_as_of"].tolist()[row_idx].split("T")[1][:-4],
                       tr_t = float(self.recs["travel_time"].tolist()[row_idx]) / 60,
                       s = self.recs["speed"].tolist()[row_idx],
                       html_c = html_color,
                       clr = travel_color)

            # decide which message to use here:
            temp_iframe = folium.IFrame(text_message_short)
            msg_popup = folium.Popup(temp_iframe,
                                     min_width=300,
                                     max_width=300,
                                     min_height=500,
                                     max_height=500)

            folium.Marker(
                location = start_pt,
                popup = msg_popup,
                icon = folium.Icon(color="blue", icon="info-sign"),
                tooltip = "Click here to see more meta-info about this starting location!"
            ).add_to(self.f_map)

            row_idx += 1


        self.f_map.add_child(folium.LatLngPopup())
        #self.f_map.add_child(folium.ClickForMarker(popup="Waypoint (LatLng TBA)"))

        display(self.f_map)

        return None
