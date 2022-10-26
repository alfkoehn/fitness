# coding=utf-8

__author__      = 'Alf Köhn-Seemann'
__email__       = 'alf.koehn@posteo.net'
__copyright__   = 'Alf Köhn-Seemann'


"""
xhtml is a stricter, more XML-based version of HTML


"""

#from html.parser import HTMLParser
#class parser(HTMLParser):
#    pass
#p = parser()
#p.feed('10371720')


from bs4 import BeautifulSoup
import json
import matplotlib.pyplot as plt
#import numpy as np

data_dir    = './'
fname_in    = '11572144'


def get_title( fname_in, silent=True ):

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


def get_all_metatags( fname_in ):
    
    with open(fname_in, 'r') as f:
        # open html file and read its conten
        contents    = f.read()
    
        # create BeautifulSoup object, pass HTML data to the constructor, specify parser
        soup    = BeautifulSoup(contents, 'lxml')

    metatags    = soup.find_all('meta', attrs={'name':'generator'})

    for tag in metatags:
        print( tag )


print( get_title(fname_in, silent=False) )
print( get_all_metatags(fname_in) )
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

