import gpxpy
import json
import matplotlib.pyplot as plt
import geopy.distance
import numpy as np
import pandas as pd


def make_df(f):
    gpx_file = open('uploads/' + f, 'r') #open gpx file
    gpx = gpxpy.parse(gpx_file)

    data = gpx.tracks[0].segments[0].points

    start = data[0] #first data point
    finish = data[-1] #last data point

    nonext = pd.DataFrame(columns=['lon', 'lat', 'alt', 'time']) #initialize empty df

    for point in data: #reformat time variable
        point.time = str(point.time).split('+')[0]

    for point in data: #put non-extension data into df
        nonext = nonext.append({'lon': point.longitude, 
                    'lat' : point.latitude, 
                    'alt' : point.elevation, 
                    'time' : point.time,
                   }, 
                   ignore_index=True)


    with open('uploads/' + f, 'r') as f2:
        file_text = f2.read().replace('\n', '')

    #format of gpx file depends on presence of atemp, hr, and cad
    if ('gpxtpx:atemp' in file_text and 'gpxtpx:hr' in file_text and 'gpxtpx:cad' in file_text):
        ext = pd.DataFrame(columns=['atemp', 'hr', 'cad'])

        for i in range(len(data)):
            ext = ext.append({
                'atemp': int(gpx.tracks[0].segments[0].points[i].extensions[0].getchildren()[0].text),
                'hr': int(gpx.tracks[0].segments[0].points[i].extensions[0].getchildren()[1].text),
                'cad': int(gpx.tracks[0].segments[0].points[i].extensions[0].getchildren()[2].text)
            },
            ignore_index=True)
    elif('gpxtpx:hr' in file_text and 'gpxtpx:cad' in file_text):
        ext = pd.DataFrame(columns=['hr', 'cad'])

        for i in range(len(data)):
            ext = ext.append({
                'hr': int(gpx.tracks[0].segments[0].points[i].extensions[0].getchildren()[0].text),
                'cad': int(gpx.tracks[0].segments[0].points[i].extensions[0].getchildren()[1].text)
            },
            ignore_index=True)
    else:
        ext = pd.DataFrame()

    if (ext.empty):
        df = nonext
    else:
        df = nonext.join(ext)

    df['time'] = df['time'].astype('datetime64')
    df['total_gain'] = 0
    df['total_dist'] = 0
    df['pace'] = 0

    for i in range(1, len(df)): #compute rolling altitude gain
        currentAlt = df.loc[i, 'alt']
        lastAlt = df.loc[i-1, 'alt']
        altDiff = currentAlt - lastAlt
    
        if (altDiff > 0):
            df.loc[i, 'total_gain'] = df.loc[i-1, 'total_gain'] + altDiff
        else:
            df.loc[i, 'total_gain'] = df.loc[i-1, 'total_gain'] 

    for i in range(1, len(df)): #compute rolling total distance
        currentPos = (df.loc[i, 'lat'], df.loc[i, 'lon'])
        lastPos = (df.loc[i-1, 'lat'], df.loc[i-1, 'lon'])
        distTrav = geopy.distance.distance(currentPos, lastPos).mi
        df.loc[i, 'total_dist'] = df.loc[i-1, 'total_dist'] + distTrav

    for i in range(1, len(df)): #compute rolling current pace
        currentPos = (df.loc[i, 'lat'], df.loc[i, 'lon'])
        lastPos = (df.loc[i-1, 'lat'], df.loc[i-1, 'lon'])
        distTrav = geopy.distance.distance(currentPos, lastPos).mi
        
        currentTime = df.loc[i, 'time']
        lastTime = df.loc[i-1, 'time']
        timeDiff = pd.Timedelta(currentTime - lastTime).seconds
    
        if (distTrav == 0):
            df.loc[i, 'pace'] = 0
        else:
            df.loc[i, 'pace'] = (timeDiff / 60) / distTrav   
        
    return(df)


def split_vis(df, data):
    midpoint = df['total_dist'].iloc[-1] / 2

    split1_meanpace = df[df['total_dist'] < midpoint]['pace'].mean()
    split2_meanpace = df[df['total_dist'] > midpoint]['pace'].mean()
    splits_pace_python = [{'Split': '1', 'Pace': split1_meanpace}, {'Split': '2', 'Pace': split2_meanpace}]
    splits_pace_json = json.dumps(splits_pace_python)
    data['splits_pace'] = splits_pace_json

    split1_meanhr = df[df['total_dist'] < midpoint]['hr'].mean()
    split2_meanhr = df[df['total_dist'] > midpoint]['hr'].mean()
    splits_hr_python = [{'Split': '1', 'HR': split1_meanhr}, {'Split': '2', 'HR': split2_meanhr}]
    splits_hr_json = json.dumps(splits_hr_python)
    data['splits_hr'] = splits_hr_json

    return(data)


def map_vis(df, data):
    lat_max = df['lat'].max()
    lon_max = df['lon'].max()

    lat_min = df['lat'].min()
    lon_min = df['lon'].min()

    lat_avg = (lat_max + lat_min) / 2
    lon_avg = (lon_max + lon_min) / 2

    map_center_python = [{'Lat': lat_avg, 'Lon': lon_avg}]
    map_center_json = json.dumps(map_center_python)

    data['map_center'] = map_center_json

    coord_df = df[['lon', 'lat']].copy()
    #coords_python = [{'coords' : coord_df.values.tolist()}]
    #coords_json = json.dumps(coords_python)
    #data['coord'] = coords_python

    coords = coord_df.values.tolist()
    data['coord'] = coords

    return(data)


def alt_hr_pace_vis(df, data):
    #df_dist_index = df.set_index('total_dist')
    #alt_hr_pace_json = df_dist_index[['alt', 'hr', 'pace']].to_json(orient='records')
    alt_hr_pace_json = df[['total_dist', 'alt', 'hr', 'pace']].to_json(orient='records')
    data['alt_hr_pace'] = alt_hr_pace_json

    return data


def vis_fun(file):
    df = make_df(file)
    #df_time_index = df.set_index('time')
    #df_dist_index = df.set_index('total_dist')

    data = {}

    data = split_vis(df, data)
    data = map_vis(df, data)
    data = alt_hr_pace_vis(df, data)

    #print(data)

    return(data)