from email.headerregistry import Address
import pandas as pd
import requests
import urllib.parse
import json
from os.path import isfile 
import os
import collections

def address2lonlat(address):
    url = 'https://nominatim.openstreetmap.org/search/' + \
        urllib.parse.quote(address) + '?format=json'
    response = requests.get(url).json()
    return response[0]["lon"], response[0]["lat"]


def get_loc(dt):
    saved_coords_loc="Code/Data/saved_coords_data.json"
    if isfile(saved_coords_loc):
        a_file = open(saved_coords_loc, "r")
        saved_coords = json.load(a_file)
    else:
        saved_coords = collections.defaultdict(dict)

    lon_list, lat_list = [], []
    for index, row in dt.iterrows():
        address = ', '.join([row['county'], row['state']])
        if address in saved_coords:
            lon, lat = saved_coords[address]['lon'],saved_coords[address]['lat']
        else:
            try: 
                lon, lat = address2lonlat(address)
                print('Get geo location of row {} success: {}, lon: {}, lat: {}'.format(
            index, address, lon, lat))
            except: 
                lon, lat = None,None
                print('FAILED: Get geo location of row {} success: {}, lon: {}, lat: {}'.format(
            index, address, lon, lat))
            saved_coords[address]={'lon':lon,'lat':lat}

            a_file = open(saved_coords_loc, "w")
            json.dump(saved_coords, a_file)
            a_file.close()



        lon_list.append(lon)
        lat_list.append(lat)

        
    return lon_list, lat_list


dt = pd.read_csv(
    'Code/Data/United_States_COVID-19_Community_Levels_by_County.csv')
# dt = dt[~dt['state'].isin(['Alaska', 'Puerto Rico'])]
dt = dt[dt.date_updated ==  ]

lon, lat = get_loc(dt)
dt['lon'] = lon
dt['lat'] = lat

# Index(['county', 'county_fips', 'state', 'county_population',
    #    'health_service_area_number', 'health_service_area',
    #    'health_service_area_population', 'covid_inpatient_bed_utilization',
    #    'covid_hospital_admissions_per_100k', 'covid_cases_per_100k',
    #    'covid-19_community_level', 'date_updated', 'lon', 'lat'],
    #   dtype='object')
dt = dt[['county','state','county_population','covid_hospital_admissions_per_100k','covid_cases_per_100k','lon','lat']]
dt.to_csv('Code/Data/cleaned_data.csv')
