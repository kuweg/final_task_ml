# 30.513574259277 29.696893 60.192742 59.668353

import matplotlib.pyplot as plt
import numpy as np
import math
import requests
from io import BytesIO
from PIL import Image

from .variables import USER_AGENT
   
    
def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
  return (xtile, ytile)
    
def num2deg(xtile, ytile, zoom):
  n = 2.0 ** zoom
  lon_deg = xtile / n * 360.0 - 180.0
  lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
  lat_deg = math.degrees(lat_rad)
  return (lat_deg, lon_deg)
   
def getImageCluster(lat_deg, lon_deg, delta_lat,  delta_long, zoom):
    headers = USER_AGENT
    smurl = r"http://a.tile.openstreetmap.org/{0}/{1}/{2}.png"
    xmin, ymax =deg2num(lat_deg, lon_deg, zoom)
    xmax, ymin =deg2num(lat_deg + delta_lat, lon_deg + delta_long, zoom)
    print(f'{xmin=} {xmax=} {ymin=} {ymax=}')
    cluster = Image.new('RGB',((xmax-xmin+1)*256-1,(ymax-ymin+1)*256-1) ) 
    for xtile in range(xmin, xmax+1):
        for ytile in range(ymin,  ymax+1):
            try:
                imgurl = smurl.format(zoom, xtile, ytile)
                print("Opening: " + imgurl)
                imgstr = requests.get(imgurl, headers=headers)
                tile = Image.open(BytesIO(imgstr.content))
                cluster.paste(tile, box = ((xtile-xmin)*256 ,  (ytile-ymin)*255))
            except: 
                print("Couldn't download image")
                tile = None
   
    return cluster
    
    
    
# if __name__ == '__main__':
#     spb_coords = (30.513574259277, 29.696893, 60.192742, 59.668353)
#     a = (spb_coords[0] + spb_coords[1]) / 2
#     b = (spb_coords[2] + spb_coords[3]) / 2
#     print(a,b)
#     a = getImageCluster(b, a, 0.04,  0.01, 8)
#     fig = plt.figure()
#     fig.patch.set_facecolor('white')
#     plt.imshow(np.asarray(a))
#     plt.show()