#!/usr/bin/python

#
# Implements 8-connectivity connected component labeling
# 
# Algorithm obtained from "Optimizing Two-Pass Connected-Component Labeling 
# by Kesheng Wu, Ekow Otoo, and Kenji Suzuki
#

from PIL import Image, ImageDraw

import sys
import math, random
from itertools import product
from ufarray import *
import cv2
import numpy as np

def run(img):
    data = img.load()
    width, height = img.size
    
    # Union find data structure
    uf = UFarray()
 
    #
    # First pass
    #
 
    # Dictionary of point:label pairs
    labels = {}
 
    for y, x in product(range(height), range(width)):
 
        #
        # Pixel names were chosen as shown:
        #
        #   -------------
        #   | a | b | c |
        #   -------------
        #   | d | e |   |
        #   -------------
        #   |   |   |   |
        #   -------------
        #
        # The current pixel is e
        # a, b, c, and d are its neighbors of interest
        #
        # 255 is white, 0 is black
        # White pixels part of the background, so they are ignored
        # If a pixel lies outside the bounds of the image, it default to white
        #
 
        # If the current pixel is white, it's obviously not a component...
        if data[x, y] == 255:
            pass
 
        # If pixel b is in the image and black:
        #    a, d, and c are its neighbors, so they are all part of the same component
        #    Therefore, there is no reason to check their labels
        #    so simply assign b's label to e
        elif y > 0 and data[x, y-1] == 0:
            labels[x, y] = labels[(x, y-1)]
 
        # If pixel c is in the image and black:
        #    b is its neighbor, but a and d are not
        #    Therefore, we must check a and d's labels
        elif x+1 < width and y > 0 and data[x+1, y-1] == 0:
 
            c = labels[(x+1, y-1)]
            labels[x, y] = c
 
            # If pixel a is in the image and black:
            #    Then a and c are connected through e
            #    Therefore, we must union their sets
            if x > 0 and data[x-1, y-1] == 0:
                a = labels[(x-1, y-1)]
                uf.union(c, a)
 
            # If pixel d is in the image and black:
            #    Then d and c are connected through e
            #    Therefore we must union their sets
            elif x > 0 and data[x-1, y] == 0:
                d = labels[(x-1, y)]
                uf.union(c, d)
 
        # If pixel a is in the image and black:
        #    We already know b and c are white
        #    d is a's neighbor, so they already have the same label
        #    So simply assign a's label to e
        elif x > 0 and y > 0 and data[x-1, y-1] == 0:
            labels[x, y] = labels[(x-1, y-1)]
 
        # If pixel d is in the image and black
        #    We already know a, b, and c are white
        #    so simpy assign d's label to e
        elif x > 0 and data[x-1, y] == 0:
            labels[x, y] = labels[(x-1, y)]
 
        # All the neighboring pixels are white,
        # Therefore the current pixel is a new component
        else: 
            labels[x, y] = uf.makeLabel()
 
    #
    # Second pass
    #
 
    uf.flatten()
 
    colors = {}

    # Image to display the components in a nice, colorful way
    output_img = Image.new("RGB", (100, 100))
    
    Zero=np.zeros(shape=(100, 100),dtype=np.uint8)
    One=np.zeros(shape=(100, 100),dtype=np.uint8)
    Two=np.zeros(shape=(100, 100),dtype=np.uint8)
    Three=np.zeros(shape=(100, 100),dtype=np.uint8)
    Four=np.zeros(shape=(100, 100),dtype=np.uint8)
    Five=np.zeros(shape=(100, 100),dtype=np.uint8)
    Six=np.zeros(shape=(100, 100),dtype=np.uint8)
    Seven=np.zeros(shape=(100, 100),dtype=np.uint8)
    outdata = output_img.load()
    #outdata1 = np.zeros_like(output_img)
    for (x, y) in labels:
        #print str(x) + " " + str(y)
        # Name of the component the current point belongs to
        component = uf.find(labels[(x, y)])
       # print component
        #temp=labels[(x, y)] 
        # Update the labels with correct information
        labels[(x, y)] = component
        path='imagesNew/13/'
        #print str(x) +","+ str(y)+ " " +str(labels[(x, y)])
        if labels[(x, y)]==0:
            Zero[y][x]=int(255)
            Z=Zero[y][x]
            print Z
            if Z==5:
              print Zero[y][x]
            Zeroth = Image.fromarray(Zero)
            Zeroth.save(path+'Zero'+'.png','png')
            
            #print str(Zero[x][y])
        if labels[(x, y)]==1:
            One[y][x]=int(255)
            First = Image.fromarray(One)
            First.save(path+'First'+'.png','png')
            #print str(One[x][y])
        if labels[(x, y)]==2:
            Two[y][x]=int(255)
            Second=Image.fromarray(Two)
            Second.save(path+'Second'+'.png','png')
            #print str(Three[x][y])
        if labels[(x, y)]==3:
           Three[y][x]=int(255)
           Third=Image.fromarray(Three)
           Third.save(path+'Third'+'.png','png')
            #print str(Three[x][y])
        if labels[(x, y)]==4:
           Four[y][x]=int(255)
           Fourth=Image.fromarray(Four)
           Fourth.save(path+'Fourth'+'.png','png')
        if labels[(x, y)]==5:
           Five[y][x]=int(255)
           Fifth=Image.fromarray(Five)
           Fifth.save(path+'Fifth'+'.png','png')
        if labels[(x, y)]==6:
           Six[y][x]=int(255)
           Sixth=Image.fromarray(Six)
           Sixth.save(path+'Sixth'+'.png','png')
        if labels[(x, y)]==7:
           Seven[y][x]=int(255)
           Seventh=Image.fromarray(Seven)
           Seventh.save(path+'Seven'+'.png','png')
            #print str(Three[x][y])
        
        # Associate a random color with this component 
        if component not in colors: 
            colors[component] = (random.randint(0,255), random.randint(0,255),random.randint(0,255))
            #print colors[component]


        
        outdata[x, y] = colors[component]
        #i=10
        #for (x,y) in outdata:
            #outdata1[x, y] = colors[component]
            #cv2.imwrite("C:/Python27/cclabel/images/emp"+str(i)+'.png', outdata1)
    
    
    return (labels, output_img)

 
def main():
    # Open the image
    img = Image.open(sys.argv[1])
    
    
    #pix = np.array(img)
    #print type(pix)

    #print img.shape
    # Threshold the image, this implementation is designed to process b+w
    # images only
    img = img.point(lambda p: p > 190 and 255)
    img = img.convert('1')

    # labels is a dictionary of the connected component data in the form:
    #     (x_coordinate, y_coordinate) : component_id
    #
    # if you plan on processing the component data, this is probably what you
    # will want to use
    #
    # output_image is just a frivolous way to visualize the components.
    (labels, output_img) = run(img)

    #output_img.show()
    output_img.save('emp1'+'.png','png')
   # crop=output_img.crop(labels[x, y])
    #output_img2 = Image.new("RGB", (50, 50))
    #output_img2.paste(crop)
    #output_img2.save('C:/Python27/cclabel/images/test10'+'.png','png')
if __name__ == "__main__": main()
