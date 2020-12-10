import gpxpy
import json
import math
import matplotlib.pyplot as plt
import geopy.distance
import numpy as np
import pandas as pd


def make_df(f):
    gpx_file = open('uploads/' + f, 'r') #open gpx file
    gpx = gpxpy.parse(gpx_file)

    data = gpx.tracks[0].segments[0].points

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

    split1_meanpace = round(df[df['total_dist'] < midpoint]['pace'].mean(),2)
    split2_meanpace = round(df[df['total_dist'] > midpoint]['pace'].mean(),2)
    splits_pace_python = [{'Split': '1st Half', 'Pace': split1_meanpace}, {'Split': '2nd Half', 'Pace': split2_meanpace}]
    splits_pace_json = json.dumps(splits_pace_python)
    data['splits_pace'] = splits_pace_json

    split1_meanhr = round(df[df['total_dist'] < midpoint]['hr'].mean(),2)
    split2_meanhr = round(df[df['total_dist'] > midpoint]['hr'].mean(),2)
    splits_hr_python = [{'Split': '1st Half', 'HR': split1_meanhr}, {'Split': '2nd Half', 'HR': split2_meanhr}]
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

    coords = coord_df.values.tolist()
    data['coord'] = coords
    data['start'] = coords[0]
    data['finish'] = coords[-1]

    return(data)


def alt_hr_pace_vis(df, data):
    alt_hr_pace_json = df[['total_dist', 'alt', 'hr', 'pace']].to_json(orient='records')
    data['alt_hr_pace'] = alt_hr_pace_json

    return data


def summary_stats(df, data):
    avg_pace = round(df['pace'].mean(),2)
    data['avg_pace'] = avg_pace

    avg_hr = round(df['hr'].mean(),2)
    data['avg_hr'] = avg_hr

    total_distance = round(df['total_dist'].max(),2)
    data['total_distance'] = total_distance

    total_time_string = str(df['time'].max() - df['time'].min()).split('days')[1].strip()
    data['total_time'] = total_time_string

    total_gain = round(df['total_gain'].max(),2)
    data['total_gain'] = total_gain

    return(data)


def pace_dist(df, data):
    min_pace = df['pace'].min()
    max_pace = df['pace'].max()

    min_pace_round = round(min_pace*2)/2
    max_pace_round = round(max_pace*2)/2

    if min_pace_round < 0.5:
        min_pace_round = 0.0
    else:
        min_pace_round = min_pace_round - 0.5

    pace_df = pd.DataFrame(columns=['pace', 'count'])

    total_len = len(df)

    for i in np.arange(min_pace_round, max_pace_round + 0.51, 0.5):
        bucket_length = len(df[(df['pace'] >= i) & (df['pace'] < i + 0.5)])
        if (bucket_length/total_len >= 0.05):
            new_row = {'pace': str(i) +'-' + str(i+0.5), 'count':bucket_length}
            pace_df = pace_df.append(new_row, ignore_index=True)

    pace_count_sum = pace_df['count'].sum()
    pace_df['percentage'] = (pace_df['count'] / pace_count_sum) * 100
    pace_df['percentage'] = pace_df['percentage'].astype('float').round(2)
    pace_data_json = pace_df[['pace', 'percentage']].to_json(orient='records')

    data['pace_dist'] = pace_data_json

    return(data)


def hr_dist(df, data):
    max_hr = df['hr'].max()

    max_hr_round = int(math.ceil(max_hr / 10.0)) * 10

    hr_df = pd.DataFrame(columns=['hr', 'count'])

    total_len = len(df)

    for i in range(0, max_hr_round, 10):
        bucket_length = len(df[(df['hr'] >= i) & (df['hr'] < i + 10)])
        if (bucket_length/total_len >= 0.05):
            new_row = {'hr': str(i) +'-' + str(i+10), 'count':bucket_length}
            hr_df = hr_df.append(new_row, ignore_index=True)

    hr_count_sum = hr_df['count'].sum()
    hr_df['percentage'] = (hr_df['count'] / hr_count_sum) * 100
    hr_df['percentage'] = hr_df['percentage'].astype('float').round(2)
    hr_data_json = hr_df[['hr', 'percentage']].to_json(orient='records')

    data['hr_dist'] = hr_data_json

    return(data)


def getAltChange(alt_list):
    change = 0
    list_len = len(alt_list)
    
    for i in range(list_len):
        if (i < list_len - 1):
            change = change + alt_list[i + 1] - alt_list[i]  
    return(change)


def split_table(df, data):
    max_dist = df['total_dist'].max()

    splits_df = pd.DataFrame(columns=['split (mi)', 'pace (min/mi)', 'hr (bpm)', 'gain (m)'])

    for i in np.arange(0, max_dist):
        split = df[(df['total_dist'] >= i) & (df['total_dist'] < i + 1) ]
        mile = i + 1
        split_pace = split['pace'].mean()
        split_hr = split['hr'].mean()
        split_alt = getAltChange(split['alt'].to_list())
        
        if(mile > max_dist):
            mile = max_dist - i
        
        new_row = {'split (mi)': mile, 'pace (min/mi)': split_pace, 'hr (bpm)': split_hr, 'gain (m)': split_alt}
        splits_df = splits_df.append(new_row, ignore_index = True)
        
    splits_df = splits_df.round(2)

    splits_data_json = splits_df.to_json(orient='records')
    data['split_table'] = splits_data_json

    return(data)


def vis_fun(file):
    df = make_df(file)

    data = {}
    
    title = file.replace('.gpx','').replace('_',' ')
    data['title'] = title

    data = split_vis(df, data)
    data = map_vis(df, data)
    data = alt_hr_pace_vis(df, data)
    data = summary_stats(df, data)
    data = pace_dist(df, data)
    data = hr_dist(df, data)
    data = split_table(df, data)

    return(data)