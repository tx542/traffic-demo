import pandas as pd
import numpy as np
import geopandas as gpd
from geopandas import GeoDataFrame
from shapely.geometry import Point, LineString
# import geoplot as gplt

from sklearn.neighbors import KNeighborsRegressor as knn

import folium
from IPython.display import display

# Nominatim requests
import requests
import urllib.parse

import os
import os.path
from os import path
import time

# sets timezone
os.environ['TZ'] = "America/New_York"
time.tzset()

def get_coor(str_quote):
    # URL request to Nominatim (Open Street Map)
    url = 'https://nominatim.openstreetmap.org/search/' +\
    urllib.parse.quote(str_quote) +\
    '?format=json'

    response = requests.get(url).json()

    # return lat and long (coordinates)
    return [response[0]["lat"], response[0]["lon"], response[0]["display_name"]]


def det_boro(str_address):
    all_boros = ["Bronx", "Brooklyn", "Manhattan", "Queens", "Staten Island"]

    for elem in str_address.split(", "):
        if elem.strip() in all_boros:
            return elem.strip()


def show_map(Borough, Link_Name, all_links, Times, Modification, dataset):

    # verifies that link name is available
    if Link_Name not in all_links:
        print("Invalid link name")
        return None

    focus_of_map = {"Bronx": [40.8448, -73.8648],
                    "Brooklyn": [40.6782, -73.9442],
                    "Manhattan": [40.7831, -73.9712],
                    "Queens": [40.7282, -73.7949],
                    "Staten Island": [40.5795, -74.1502]
                   }

    # extract sub-df with matching link + borough name
    this_df = dataset[dataset["names"] == Link_Name]

    this_f_map = folium.Map(focus_of_map[Borough], zoom_start=12)

    l_idx = 0

    obs_row = this_df[this_df["time_s"] == Times]

    ave_speed = this_df['rou_speed'].apply(float).mean()

    this_speed = float(obs_row['rou_speed'])

    if this_speed > ave_speed:
        # faster than **average** speed
        this_color = 'darkgreen'
    else:
        this_color = 'darkred'

    folium.Choropleth(
        obs_row["geometry"],
        line_weight=8,
        line_color=this_color,
        key_on='names'
    ).add_to(this_f_map)
    l_idx += 1

    # take starting point for each camera-monitored road
    # e.g. [40.7894406, -73.786291]

    start_pt = list(list(obs_row["geometry"].tolist()[0].coords)[0])[::-1]

    # cols of self.recs:
    # "speed", "travel_time", "data_as_of", "link_points", "borough", "link_name"

    html_color = this_color.replace("dark", "")
    travel_color = html_color.capitalize()

    text_message_short = '''
    <center>
    <p style="color:{html_c};">
    <b>TRAVEL COLOR: {clr}</b>
    </p>
    </center>
    <hr>
    <center>
    <p><b>Date:</b> {date_rec} <b>|</b> <b>Time:</b> {t_rec}
    </p>
    </center>
    <hr>
    <p><b>Speed at This Time:</b> {speed:.2f} mph
    </p>
    <p><b>Travel Time:</b> {tr_t:.2f} minutes.
    </p>
    <p><b>Average Speed:</b> {ave_s:.2f} mph
    </p>
    <hr>
    <p><b>TrafficLink Name:</b> {lk_nm}
    </p>
    <p><b>Borough:</b> {bor}
    </p>
    '''.format(lk_nm = Link_Name,
               bor = obs_row["boro"].tolist()[0],
               date_rec = Times.split("T")[0],
               t_rec = Times.split("T")[1][:-4],
               tr_t = float(obs_row["tr_time"].tolist()[0]) / 60,
               speed = this_speed,
               ave_s = ave_speed,
               html_c = html_color,
               clr = travel_color.upper())

    temp_iframe = folium.IFrame(text_message_short)
    msg_popup = folium.Popup(temp_iframe,
                             min_width=300,
                             max_width=300,
                             min_height=500,
                             max_height=500)

    folium.Marker(
        location = start_pt,
        popup = msg_popup,
        icon = folium.Icon(color=html_color, icon="info-sign"),
        tooltip = "Click here to see more meta-info about this starting location!"
    ).add_to(this_f_map)

    # ADD LAT LONG POP-UPS
    # this_f_map.add_child(folium.LatLngPopup())
    # this_f_map.add_child(folium.ClickForMarker(popup="Waypoint (LatLng TBA)"))

    print("Proposed times is:", Times)
    print("Proposed modification is:", Modification)

    return this_f_map

    #this_f_map.save("{}_map.html".format(Link_Name))




def show_modify_map(all_links, make_pred, predictor_obj_1, predictor_obj_2, Borough, Link_Name, Times, Modification, the_obj):

    '''
    Traffic Light Color Scheme (hex code):
    Red: #BB1E10
    Green: #33A532
    Yellow: #F7B500
    '''

    # verifies that link name is available
    if Link_Name not in all_links:
        print("Invalid link name")
        return None

    # define temporary df to operate on
    temp_exp_df = the_obj.pol_df.copy()

    # kv for focus of map (depends on borough)
    focus_of_map = {"Bronx": [40.8448, -73.8648],
                    "Brooklyn": [40.6782, -73.9442],
                    "Manhattan": [40.7831, -73.9712],
                    "Queens": [40.7282, -73.7949],
                    "Staten Island": [40.5795, -74.1502]
                   }

    # if road blocked: drop the cat_code correponding to the name
    road_blocked = Link_Name # TB user input
    correspond_boro = temp_exp_df[temp_exp_df['names_code'] ==\
                                  the_obj.df_names_kv[road_blocked]]['boro'].unique().to_list()[0]

    # make a temporary df for analysis
    # temp_exp_df = temp_exp_df[temp_exp_df['names_code'] != the_obj.df_names_kv[road_blocked]]

    temp_exp_df = temp_exp_df[['names_code', 'boro_code', 'geometry', 'tr_dist']].drop_duplicates()

    # get rid of timezone discrepancy
    #Times = Times.tz_convert('America/New_York')

    # make the relevant predictions
    make_pred(Times, temp_exp_df, predictor_obj_1, predictor_obj_2)

    # extract sub-df with relevant borough name
    this_df = temp_exp_df[temp_exp_df['boro_code'] == the_obj.df_boro_kv[correspond_boro]]
    this_df["link_name"] = this_df["names_code"].apply(lambda x: the_obj.df_names_kv_rev[x])

    this_f_map = folium.Map(focus_of_map[correspond_boro], tiles="Stamen Toner", zoom_start=12)

    # firstly, add (display) all the linestrings for the corresponding borough

    l_idx = 0

    for l_str in this_df["geometry"]:

        ave_speed = this_df['pred_rou_speed'].apply(float).mean()

        this_speed = float(this_df["pred_rou_speed"].tolist()[l_idx])

        # the blocked road here
        if (this_df["names_code"].tolist()[l_idx] == the_obj.df_names_kv[road_blocked]):
            this_color = '#F7B500'

        elif this_speed > ave_speed:
            # faster than **average** speed
            this_color = '#33A532'

        else:
            this_color = '#BB1E10'

        folium.Choropleth(
            l_str,
            line_weight=8,
            line_color=this_color,
            key_on='names'
        ).add_to(this_f_map)

        l_idx += 1

    # then, add the meta-info, in the form of pop-up markers,
    # at the starting point of each recorded road

    row_idx = 0

    # for the starting point in every geometry (recorded road)
    for start_pt in this_df["geometry"].apply(lambda x: list(list(x.coords)[0])[::-1]):

        ave_speed = this_df['pred_rou_speed'].apply(float).mean()

        this_speed = float(this_df["pred_rou_speed"].tolist()[row_idx])

        # the blocked road here
        if (this_df["names_code"].tolist()[row_idx] == the_obj.df_names_kv[road_blocked]):
            this_color = '#F7B500'
            travel_color = "Yellow"

        elif this_speed > ave_speed:
            # faster than **average** speed
            this_color = '#33A532'
            travel_color = "Green"

        else:
            this_color = '#BB1E10'
            travel_color = "Red"

        html_color = this_color

        text_message_short = '''
        <center>
        <p style="color:{html_c};">
        <b>TRAVEL COLOR: {clr}</b>
        </p>
        </center>
        <hr>
        <center>
        <p><b>Date:</b> {date_rec} <b>|</b> <b>Time:</b> {t_rec}
        </p>
        </center>
        <hr>
        <p><b>Speed at This Time:</b> {speed:.2f} mph
        </p>
        <p><b>Travel Time:</b> {tr_t:.2f} minutes.
        </p>
        <p><b>Average Speed:</b> {ave_s:.2f} mph
        </p>
        <hr>
        <p><b>TrafficLink Name:</b> {lk_nm}
        </p>
        <p><b>Borough:</b> {bor}
        </p>
        '''.format(lk_nm = this_df["link_name"].tolist()[row_idx],
                   bor = correspond_boro,
                   date_rec = this_df["time_s"].tolist()[row_idx].split("T")[0],
                   t_rec = this_df["time_s"].tolist()[row_idx].split("T")[1],
                   tr_t = float(this_df["pred_tr_time"].tolist()[row_idx]) / 60,
                   speed = this_speed,
                   ave_s = ave_speed,
                   html_c = html_color,
                   clr = travel_color.upper())

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
        ).add_to(this_f_map)

        row_idx += 1

    print("Proposed times is:", Times.strftime("Date: %Y-%m-%d, Time: %H:%M:%S"))
    print("Proposed modification is:", Modification)

    display(this_f_map)
    # return this_f_map

    #this_f_map.save("{}_map.html".format(Link_Name))


def comp_model(all_links, make_pred, predictor_obj_1, predictor_obj_2,
Borough, Times, Modification, the_obj,
Link_Name, start_str, end_str, all_address):

    '''
    Traffic Light Color Scheme (hex code):
    Red: #BB1E10
    Green: #33A532
    Yellow: #F7B500
    '''

    # Modification:
    # options = ["None", "Construction", "New Road", "New Multi-Road"]

    # kv for focus of map (depends on borough)
    focus_of_map = {"Bronx": [40.8448, -73.8648],
                    "Brooklyn": [40.6782, -73.9442],
                    "Manhattan": [40.7831, -73.9712],
                    "Queens": [40.7282, -73.7949],
                    "Staten Island": [40.5795, -74.1502]
                   }

    # define temporary df to operate on
    temp_exp_df = the_obj.pol_df.copy()
    temp_exp_df = temp_exp_df[["names", 'names_code', 'boro', 'boro_code', 'geometry', 'tr_dist']].drop_duplicates()


    # ------>>>>>> Function Based on User's Choice of Modification <<<<<<------

    if Modification == "New Road":

        # try to get coordinates from user inputs
        try:
            start_pt = get_coor(start_str)
            end_pt = get_coor(end_str)
        except:
            print("Invalid starting/ending address!")
            return None

        # if can be found:
        # WE NEED:
        # - 'names_code' (based on proximity)
        # - 'boro_code' (based on address)
        # - 'tr_dist' (can be calculated based on start & end pts)
        # - 'time_float' (user input)

        # determine borough:

        st_borough = det_boro(start_pt[2])
        end_borough = det_boro(end_pt[2])

        # for now: start and end should be in the same borough

        if st_borough != end_borough:
            # print(st_borough, end_borough, st_borough == end_borough, sep = "\n")
            print("The starting and ending points must be in the same borough!")
            return None

        # name of corresponding borough
        correspond_boro = st_borough

        # determine travel distance
        # and construct Linestring object

        temp_pts = gpd.points_from_xy([start_pt[1], end_pt[1]],
                                      [start_pt[0], end_pt[0]],
                                      crs = "EPSG:4326")

        this_geometry = LineString(temp_pts)
        this_tr_dist = this_geometry.length

        # approximate - to which existing streets this new street
        # behaves most similarly to (KNN)

        # use 'geometry' ?
        this_appr_name_code = knn().fit(X = temp_exp_df[['boro_code', 'tr_dist']],
                                        y = temp_exp_df['names_code']).\
        predict(X = [[the_obj.df_boro_kv[correspond_boro], this_tr_dist]])


        # add entry of this new road into dataframe
        temp_exp_df = temp_exp_df.append({"names": "***Proposed New Road***",
                                          'names_code': this_appr_name_code,
                                          'boro': correspond_boro,
                                          'boro_code': the_obj.df_boro_kv[correspond_boro],
                                          'geometry': this_geometry,
                                          'tr_dist': this_tr_dist
                                         }
                                         , ignore_index = True)

    elif Modification == "New Multi-Road":

        add_ls = []

        for address_line in all_address.split("\n"):

            # get rid of extra white spaces/blank characters
            address_line = address_line.strip()

            # try to get coordinates from user inputs
            try:
                pt_coord = get_coor(address_line)
            except:
                print("Invalid point address!")
                return None

            add_ls.append(pt_coord)

        # if can be found:
        # WE NEED:
        # - 'names_code' (based on proximity)
        # - 'boro_code' (based on address)
        # - 'tr_dist' (can be calculated based on start & end pts)
        # - 'time_float' (user input)

        # determine borough:

        boro_ls = [det_boro(pt[2]) for pt in add_ls]

        # for now: all points should be in the same borough

        if not all(item == boro_ls[0] for item in boro_ls):
            print("All point addresses must be in the same borough!")
            print(boro_ls)
            return None

        # name of corresponding borough
        correspond_boro = boro_ls[0]

        # determine travel distance
        # and construct Linestring object

        temp_pts = gpd.points_from_xy([item[1] for item in add_ls],
        [item[0] for item in add_ls],
        crs = "EPSG:4326")

        this_geometry = LineString(temp_pts)
        this_tr_dist = this_geometry.length

        # approximate - to which existing streets this new street
        # behaves most similarly to (KNN)

        # use 'geometry' ?
        this_appr_name_code = knn().fit(X = temp_exp_df[['boro_code', 'tr_dist']],
                                        y = temp_exp_df['names_code']).\
        predict(X = [[the_obj.df_boro_kv[correspond_boro], this_tr_dist]])


        # add entry of this new road into dataframe
        temp_exp_df = temp_exp_df.append({"names": "***Proposed New Road***",
                                          'names_code': this_appr_name_code,
                                          'boro': correspond_boro,
                                          'boro_code': the_obj.df_boro_kv[correspond_boro],
                                          'geometry': this_geometry,
                                          'tr_dist': this_tr_dist
                                         }
                                         , ignore_index = True)


    elif Modification == "Construction":

        # verifies that link name is available
        if Link_Name not in all_links:
            print("Please input your selections...")
            return None

        # if road blocked: drop the cat_code correponding to the name
        road_blocked = Link_Name # TB user input

        correspond_boro = temp_exp_df[temp_exp_df['names_code'] ==\
        the_obj.df_names_kv[road_blocked]]['boro'].unique().to_list()[0]

        # make a temporary df for analysis
        # temp_exp_df = temp_exp_df[temp_exp_df['names_code'] != the_obj.df_names_kv[road_blocked]]

    else:
        # Modification == "None"

        # verifies that link name is available
        if Link_Name not in all_links:
            print("Please input your selections...")
            return None

        correspond_boro = temp_exp_df[temp_exp_df['names_code'] ==\
        the_obj.df_names_kv[Link_Name]]['boro'].unique().to_list()[0]

    # ------>>>>>> Operations Below to Display DF on Map <<<<<<------

    # make the relevant predictions
    make_pred(Times, temp_exp_df, predictor_obj_1, predictor_obj_2)

    # extract sub-df with relevant borough name
    this_df = temp_exp_df[temp_exp_df['boro_code'] == the_obj.df_boro_kv[correspond_boro]]

    this_f_map = folium.Map(focus_of_map[correspond_boro],
                            tiles = "Stamen Toner",
                            zoom_start = 12)

    # firstly, add (display) all the linestrings for the corresponding borough

    l_idx = 0

    for l_str in this_df["geometry"]:

        ave_speed = this_df['pred_rou_speed'].apply(float).mean()

        this_speed = float(this_df["pred_rou_speed"].tolist()[l_idx])

        # the modified road here
        if Modification == "Construction":
            if (this_df["names_code"].tolist()[l_idx] == the_obj.df_names_kv[road_blocked]):
                this_color = '#F7B500'
            # for other unimpacted roads
            elif this_speed > ave_speed:
                # faster than **average** speed
                this_color = '#33A532'
            else:
                this_color = '#BB1E10'

        elif Modification in ["New Road", "New Multi-Road"]:
            if (this_df["names_code"].tolist()[l_idx] == this_appr_name_code):
                this_color = '#F7B500'
            # for other unimpacted roads
            elif this_speed > ave_speed:
                # faster than **average** speed
                this_color = '#33A532'
            else:
                this_color = '#BB1E10'

        else:
            if this_speed > ave_speed:
                # faster than **average** speed
                this_color = '#33A532'
            else:
                this_color = '#BB1E10'

        folium.Choropleth(
            l_str,
            line_weight=8,
            line_color=this_color,
            key_on='names'
        ).add_to(this_f_map)

        l_idx += 1

    # then, add the meta-info, in the form of pop-up markers,
    # at the starting point of each recorded road

    row_idx = 0

    # for the starting point in every geometry (recorded road)
    for start_pt in this_df["geometry"].apply(lambda x: list(list(x.coords)[0])[::-1]):

        ave_speed = this_df['pred_rou_speed'].apply(float).mean()

        this_speed = float(this_df["pred_rou_speed"].tolist()[row_idx])

        constr_rd = False
        new_rd = False
        travel_color = ""
        # the modified road here
        if Modification == "Construction":
            if (this_df["names_code"].tolist()[row_idx] == the_obj.df_names_kv[road_blocked]):
                this_color = '#F7B500'
                constr_rd = True
                travel_color = "Yellow"

            elif this_speed > ave_speed:
                # faster than **average** speed
                this_color = '#33A532'
                travel_color = "Green"

            else:
                this_color = '#BB1E10'
                travel_color = "Red"

        elif Modification in ["New Road", "New Multi-Road"]:
            if (this_df["names_code"].tolist()[row_idx] == this_appr_name_code):
                this_color = '#F7B500'
                new_rd = True
                travel_color = "Yellow"

            elif this_speed > ave_speed:
                # faster than **average** speed
                this_color = '#33A532'
                travel_color = "Green"

            else:
                this_color = '#BB1E10'
                travel_color = "Red"

        else:
            if this_speed > ave_speed:
                # faster than **average** speed
                this_color = '#33A532'
                travel_color = "Green"

            else:
                this_color = '#BB1E10'
                travel_color = "Red"

        html_color = this_color

        if constr_rd:
            text_message_short = '''
            <center>
            <p style="color:{html_c};">
            <b>UNDER CONSTRUCTION</b>
            </p>
            </center>
            <hr>
            <center>
            <p><b>Date:</b> {date_rec} <b>|</b> <b>Time:</b> {t_rec}
            </p>
            </center>
            <hr>
            <p>You have chosen this road to be <b>under construction</b>,
            so it is not in operation.
            </p>
            <p><b>Historical Average Speed:</b> {ave_s:.2f} mph
            </p>
            <hr>
            <p><b>TrafficLink Name:</b> {lk_nm}
            </p>
            <p><b>Borough:</b> {bor}
            </p>
            '''.format(lk_nm = this_df["names"].tolist()[row_idx],
                       bor = correspond_boro,
                       ave_s = ave_speed,
                       date_rec = this_df["time_s"].tolist()[row_idx].split("T")[0],
                       t_rec = this_df["time_s"].tolist()[row_idx].split("T")[1],
                       html_c = html_color)

        elif new_rd:

            text_message_short = '''
            <center>
            <p style="color:{html_c};">
            <b>NEW ROAD</b>
            </p>
            </center>
            <hr>
            <center>
            <p><b>Date:</b> {date_rec} <b>|</b> <b>Time:</b> {t_rec}
            </p>
            </center>
            <hr>
            <p>This is a <b>new road</b> that you have proposed,
            thus yet to be constructed.
            </p>
            <hr>
            <p><b>Predicted Speed at This Time:</b> {speed:.2f} mph
            </p>
            <p><b>Predicted Travel Time:</b> {tr_t:.2f} minutes.
            </p>
            <hr>
            <p><b>TrafficLink Name:</b> {lk_nm}
            </p>
            <p><b>Borough:</b> {bor}
            </p>
            '''.format(lk_nm = this_df["names"].tolist()[row_idx],
                       bor = correspond_boro,
                       date_rec = this_df["time_s"].tolist()[row_idx].split("T")[0],
                       t_rec = this_df["time_s"].tolist()[row_idx].split("T")[1],
                       tr_t = float(this_df["pred_tr_time"].tolist()[row_idx]) / 60,
                       speed = this_speed,
                       html_c = html_color)

        else:
            text_message_short = '''
            <center>
            <p style="color:{html_c};">
            <b>TRAVEL COLOR: {clr}</b>
            </p>
            </center>
            <hr>
            <center>
            <p><b>Date:</b> {date_rec} <b>|</b> <b>Time:</b> {t_rec}
            </p>
            </center>
            <hr>
            <p><b>Speed at This Time:</b> {speed:.2f} mph
            </p>
            <p><b>Travel Time:</b> {tr_t:.2f} minutes.
            </p>
            <p><b>Average Speed:</b> {ave_s:.2f} mph
            </p>
            <hr>
            <p><b>TrafficLink Name:</b> {lk_nm}
            </p>
            <p><b>Borough:</b> {bor}
            </p>
            '''.format(lk_nm = this_df["names"].tolist()[row_idx],
                       bor = correspond_boro,
                       date_rec = this_df["time_s"].tolist()[row_idx].split("T")[0],
                       t_rec = this_df["time_s"].tolist()[row_idx].split("T")[1],
                       tr_t = float(this_df["pred_tr_time"].tolist()[row_idx]) / 60,
                       speed = this_speed,
                       ave_s = ave_speed,
                       html_c = html_color,
                       clr = travel_color.upper())

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
        ).add_to(this_f_map)

        row_idx += 1

    print("Proposed times is:", Times.strftime("Date: %Y-%m-%d, Time: %H:%M:%S"))
    print("Proposed modification is:", Modification)

    display(this_f_map)
    # return this_f_map

    #this_f_map.save("{}_map.html".format(Link_Name))
