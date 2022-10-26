# coding=utf-8

__author__      = 'Alf Köhn-Seemann'
__email__       = 'alf.koehn@posteo.net'
__copyright__   = 'Alf Köhn-Seemann'


"""
xhtml is a stricter, more XML-based version of HTML


"""


from bs4 import BeautifulSoup
import json
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np


def get_title( fname_in, silent=True ):
#{{{
    with open(fname_in, 'r') as f:
        # open html file and read its conten
        contents    = f.read()
    
        # create BeautifulSoup object, pass HTML data to the constructor, specify parser
        soup    = BeautifulSoup(contents, 'lxml')

    # 'meta' tag name must be first argument to find()
    # keyword arguments for specific attributes
    description = soup.find('meta', attrs={'name':'description'})

    if not silent:
        print( "description from file '{0}': {1}".format(fname_in, description['content']) )
        #print(description['content'] if description else 'no description given' )

    return description['content']
#}}}


def get_waypoints( fname_in, silent=True, single_plot=False ):
#{{{

    errValue    = -1
    
    with open (fname_in, 'r') as fh:
        soup    = BeautifulSoup(fh, 'lxml')

    # get all JavaScript elements
    script_all  = soup.find_all('script')
    # works also: script_all  = soup.find_all('script', type='text/javascript')

    if not silent:
        print( 'len(script_all): ', len(script_all) )

    # the relevant data is stored at ID 6 which should correspond to the 7th
    # javascript element in the array of all javascript elements
    relevant_script = str(script_all[6])

    # split() method splits string from specified separator and returns list 
    # object with string elements separated by separator
    str_tmp1    = relevant_script.split('var waypoints = ')
    # some files do not contain waypoints for some reason, thus above split
    # command will find nothing to split, hence results is same as original
    # string, but in a 1-element list
    if str_tmp1[0] == relevant_script:
        print( 'WARNING: no waypoints found in file {0}'.format(fname_in) )
        return errValue
    str_tmp2    = str_tmp1[1].split(';')
    str_tmp3    = str_tmp2[0]
    # delete beginning '[' and ending ']'
    waypts_str  = str_tmp3[1:-1]

    # loop through string of waypoints and convert it into array
    lat = []
    lon = []
    for ii in range(len(waypts_str)):
        if waypts_str[ii] == '[':
            # read until next occurence of ',' and convert into float
            lat_val = float( waypts_str[(ii+1):].partition(',')[0] )
            lat.append( lat_val ) 
        elif (waypts_str[ii] == ',') and (waypts_str[ii-1] != ']'):
            lon.append( float( waypts_str[(ii+1):].partition(']')[0] ) )

    if not silent:
        print( "number of waypoints extracted from file '{0}': N_lon = {1}, N_lat = {2}".format(
            fname_in, len(lon), len(lat) ))

    # convert everything to a pandas dataframe
    df  = pd.DataFrame( lat, columns=['latitude'] )
    df['longitude'] = lon

    if single_plot:
        fig1    = plt.figure( figsize=(8,6) )
        ax1     = fig1.add_subplot( 1,1,1 )
        ax1.plot( df['longitude'], df['latitude'], marker='.' )
        plt.show()

    return df

#}}}


def plot_all_track( data_dir='./', 
                    lat_min=np.nan, lat_max=np.nan, 
                    lon_min=np.nan, lon_max=np.nan,
                    silent=True ):
#{{{

    # empty dataframe to be filled waypoints from all tracks
    df  = pd.DataFrame( columns=['latitude', 'longitude'] )

    # loop through all files in set directoy
    for filename in os.listdir(data_dir):
        fname   = os.path.join( data_dir, filename )
        print( filename, fname, os.path.isfile(fname) )
        # take case that we only the dailymile files (which have no ending)
        if os.path.isfile(fname) and ('.' not in filename):
            print( get_title(fname) )
            df_tmp  = get_waypoints(fname)
            if isinstance(df_tmp, pd.DataFrame):
                df  = pd.concat( [df, df_tmp], axis=0, ignore_index=False )

    if np.isnan(lat_min):
        lat_min = df['latitude'].min()
    if np.isnan(lat_max):
        lat_max = df['latitude'].max()
    if np.isnan(lon_min):
        lon_min = df['longitude'].min()
    if np.isnan(lon_max):
        lon_max = df['longitude'].max()

    fig1    = plt.figure( figsize=(8,8) )
    ax1     = fig1.add_subplot( 1,1,1 )

    ax1.scatter( df['longitude'], df['latitude'], s=0.1 )

    ax1.set_xlim( [lon_min, lon_max] )
    ax1.set_ylim( [lat_min, lat_max] )

    plt.show()
#}}}


def main():
    data_dir    = './'
    fname_in    = '11572144'
    #print( get_title(fname_in, silent=False) )
    #print( get_waypoints(fname_in, single_plot=True, silent=False) )


if __name__ == '__main__':
    main()



