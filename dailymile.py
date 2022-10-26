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
#import numpy as np

data_dir    = './'
fname_in    = '11572144'


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

    if single_plot:
        fig1    = plt.figure( figsize=(8,6) )
        ax1     = fig1.add_subplot( 1,1,1 )
        ax1.plot( lon, lat, marker='.', linestyle='none' )
        plt.show()


#}}}

print( get_title(fname_in, silent=False) )
print( get_waypoints(fname_in, single_plot=True) )
print('xxxxxxxx' )

with open (fname_in, 'r') as f:
    # open html file and read its conten
    contents = f.read()

    # create BeautifulSoup object, pass HTML data to the constructor, specify parser
    soup    = BeautifulSoup(contents, 'lxml')

    # print html code of tags h2 and head
    #print(soup.h2)
    #print(soup.head)

    # of the multiple li elements, first is printed
    #print(soup.li)

print('*********************')
with open (fname_in, 'r') as fh:
    soup2   = BeautifulSoup(fh, 'lxml')
print(soup2.h2)
rawJ    = soup2.find_all('script')
print('len(rawJ): ',len(rawJ))
#print(rawJ[6])
J = str(rawJ[6])

# split() method splits string from specified separator and returns list object 
# with string elements separated by separator
J1 = J.split('var waypoints = ')
J2 = J1[1].split(';')
J3 = J2[0]
# delete beginning '[' and ending ']'
J3 = J3[1:-1]

# loop through string of waypoints and convert it into array
lat = []
lon = []
print('len(J3):', len(J3))
for ii in range(len(J3)):
    if J3[ii] == '[':
        # read until next occurence of ',' and convert into float
        lat_val = float( J3[(ii+1):].partition(',')[0] )
        #print( ii, J3[ii], lat_val )
        lat.append( lat_val ) 
    elif (J3[ii] == ',') and (J3[ii-1] != ']'):
        lon.append( float( J3[(ii+1):].partition(']')[0] ) )

#print(lat)
#print(lon)

#J4 = J3.split(',')

#print(J3)
#print(J3[0])

fig1    = plt.figure( figsize=(8,6) )
ax1     = fig1.add_subplot( 1,1,1 )
ax1.plot( lon, lat, marker='.', linestyle='none' )
plt.show()

