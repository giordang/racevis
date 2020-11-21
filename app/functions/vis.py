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

    ext = pd.DataFrame(columns=['hr', 'cad'])

    for i in range(len(data)):
        ext = ext.append({
            'hr': int(gpx.tracks[0].segments[0].points[i].extensions[0].getchildren()[0].text),
            'cad': int(gpx.tracks[0].segments[0].points[i].extensions[0].getchildren()[1].text)
        },
        ignore_index=True)

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

    splits_python = [{'Split': '1', 'Pace': split1_meanpace}, {'Split': '2', 'Pace': split2_meanpace}]
    splits_json = json.dumps(splits_python)

    data['splits'] = splits_json

    return(data)





def vis_fun(file):
    '''
    gpx_file = open('uploads/' + file, 'r') #open gpx file
    gpx = gpxpy.parse(gpx_file)
    #print(len(gpx.tracks[0].segments[0].points))

    data = gpx.tracks[0].segments[0].points

    start = data[0] #first data point
    finish = data[-1] #last data point
    #print(start)
    #print(finish)

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

    ext = pd.DataFrame(columns=['hr', 'cad'])

    for i in range(len(data)):
        ext = ext.append({
            'hr': int(gpx.tracks[0].segments[0].points[i].extensions[0].getchildren()[0].text),
            'cad': int(gpx.tracks[0].segments[0].points[i].extensions[0].getchildren()[1].text)
        },
        ignore_index=True)

    #print(len(nonext), len(ext))

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
    '''
    df = make_df(file)

    #df_time_index = df.set_index('time')
    #df_dist_index = df.set_index('total_dist')

    #average_pace = df['pace'].mean()

    #midpoint = df['total_dist'].iloc[-1] / 2
    #split1_meanpace = df[df['total_dist'] < midpoint]['pace'].mean()
    #split2_meanpace = df[df['total_dist'] > midpoint]['pace'].mean()

    #splits_python = [{'Split': '1', 'Pace': split1_meanpace}, {'Split': '2', 'Pace': split2_meanpace}]
    #splits_json = json.dumps(splits_python)

    data = {}

    data = split_vis(df, data)

    return(data)