#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2014年1月15日
@author: peng
@contact: myme5261314@gmail.com
This file defines some transform function that will be invoked in this project.
'''
import math

def latToTileY(lat, zoom):
    l = lat / 180 * math.pi;
    pf = math.log(math.tan(l) + (1 / math.cos(l)));
    return math.pow(2.0, zoom - 1) * (math.pi - pf) / math.pi;

def lonToTileX(lon, zoom):
    return math.pow(2.0, zoom - 3) * (lon + 180.0) / 45.0;

def tileYToLat(y, zoom):
    return math.atan(math.sinh(math.pi - (math.pi * y / math.pow(2.0, zoom - 1)))) * 180 / math.pi;

def tileXToLon(x, zoom):
    return x * 45.0 / math.pow(2.0, zoom - 3) - 180.0;


def tileXYZToQuadKey(x, y, z):
    '''This is a function that transform the Tile with (x,y) coordinate at (z) zoom level
    to its corresponding QuadKey index.
    
    Args:
        x (int): the horizontal axes position. Range from 0-2^z-1.
        y (int): the vertical axes position. Range from 0-2^z-1.
        z (int): the zoom level. Range from 1-19 for the Bing Map Tile System.
    
    Returns:
        str: the corresponding QuadKey index which has the length of z.
    '''
    
    quadKey = ''
    for i in range(z, 0, -1):
        digit = 0
        mask = 1 << (i - 1)
        if(x & mask) != 0:
            digit += 1
        if(y & mask) != 0:
            digit += 2
        quadKey += str(digit)
    return quadKey