#!/usr/local/bin/python3
#
# Your names and user ids:
# Nagatheja Sharaf - nasharaf@iu.edu
# Prasad Hegde     - phegde@iu.edu
# Akhil            - nyeniset@iu.edu


from PIL import Image
from numpy import *
from scipy.ndimage import filters
import sys
import imageio
import copy

# calculate "Edge strength map" of an image                                                                                                                                      
def edge_strength(input_image):
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)
    filters.sobel(grayscale,0,filtered_y)
    return sqrt(filtered_y**2)

# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
#
def draw_boundary(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range( int(max(y-int(thickness/2), 0)), int(min(y+int(thickness/2), image.size[1]-1 )) ):
            image.putpixel((x, t), color)
    return image

def draw_asterisk(image, pt, color, thickness):
    for (x, y) in [ (pt[0]+dx, pt[1]+dy) for dx in range(-3, 4) for dy in range(-2, 3) if dx == 0 or dy == 0 or abs(dx) == abs(dy) ]:
        if 0 <= x < image.size[0] and 0 <= y < image.size[1]:
            image.putpixel((x, y), color)
    return image


# Save an image that superimposes three lines (simple, hmm, feedback) in three different colors 
# (yellow, blue, red) to the filename
def write_output_image(filename, image, simple, hmm, feedback, feedback_pt):
    new_image = draw_boundary(image, simple, (255, 255, 0), 2)
    new_image = draw_boundary(new_image, hmm, (0, 0, 255), 2)
    new_image = draw_boundary(new_image, feedback, (255, 0, 0), 2)
    new_image = draw_asterisk(new_image, feedback_pt, (255, 0, 0), 2)
    imageio.imwrite(filename, new_image)



# main program
#
if __name__ == "__main__":

    if len(sys.argv) != 6:
        raise Exception("Program needs 5 parameters: input_file airice_row_coord airice_col_coord icerock_row_coord icerock_col_coord")

    input_filename = sys.argv[1]
    gt_airice = [ int(i) for i in sys.argv[2:4] ]
    gt_icerock = [ int(i) for i in sys.argv[4:6] ]

    # load in image 
    input_image = Image.open(input_filename).convert('RGB')
    image_array = array(input_image.convert('L'))

    # compute edge strength mask -- in case it's helpful. Feel free to use this.
    edge_strength = edge_strength(input_image)
    imageio.imwrite('edges.png', uint8(255 * edge_strength / (amax(edge_strength))))
        
    # return list of indices of 
    # max edge strength in each column
    def simple(table):
        T=copy.deepcopy(table)
        return [list(c).index(max(list(c))) for c in T] 

    # make a layer of [rows][columns] for given target
    # we use this to remove air-ice boundary
    def removLayer(table,target,margin):  
        T=copy.deepcopy(table)
        for c in range(len(T)):
            T[c]=[0 if x<target[c]+margin else T[c][x] for x in range(len(T[c])) ]
        return T

    def humanPointHeuristic(point,i,totalCols):
        return abs(point-i)/totalCols

    def hmm(newTable):
        boundary=[]
        m=newTable[0].index(max(newTable[0])) # initial boundary -> S0
        boundary.append(m)
        for c in range(1,len(newTable)):
            r=0
            while r<len(newTable[c]): # decide S(i+1) based on S(i) and ti->t(i+1)
                newTable[c][r]=newTable[c][r] - (newTable[c][r]*abs(m-r)/len(newTable[c]))
                r+=1
            m=newTable[c].index(max(newTable[c]))
            boundary.append(m)

        return boundary

    # transpose the table so that it's easy to travesrse column
    table=transpose(edge_strength)
    
    newTable=copy.deepcopy(table)
    newTable=newTable.tolist()
    for c in range(len(table)): # update - edge strength-> range(0,1)
        newTable[c]=[ 0 if max(newTable[c])==0 else newTable[c][r]/max(newTable[c]) for r in range(len(newTable[c]))]
    # calc air-ice and ice-rock boundary --> SIMPLE
    airice_simple=simple(newTable)
    icerock_simple=simple(removLayer(table,airice_simple,10))

    # calc air-ice and ice-rock boundary --> HMM
    airice_hmm=hmm(newTable)
    icerock_hmm=hmm(removLayer(newTable,airice_hmm,10))

    feedbaclTable1=copy.deepcopy(newTable)
    for c in range(len(feedbaclTable1)):
        feedbaclTable1[c]=[ feedbaclTable1[c][r]-humanPointHeuristic(gt_airice[1],r,len(feedbaclTable1[c])) for r in range(len(feedbaclTable1[c]))]
    
    airice_feedback= hmm(feedbaclTable1)

    feedbaclTable2=copy.deepcopy(newTable)
    for c in range(len(feedbaclTable2)):
        feedbaclTable2[c]=[ feedbaclTable2[c][r]-humanPointHeuristic(gt_icerock[1],r,len(feedbaclTable2[c])) for r in range(len(feedbaclTable2[c]))]

    icerock_feedback= hmm(removLayer(feedbaclTable2,airice_feedback,10))

    # Now write out the results as images and a text file
    write_output_image("air_ice_output.png", input_image, airice_simple, airice_hmm, airice_feedback, gt_airice)
    write_output_image("ice_rock_output.png", input_image, icerock_simple, icerock_hmm, icerock_feedback, gt_icerock)
    with open("layers_output.txt", "w") as fp:
        for i in (airice_simple, airice_hmm, airice_feedback, icerock_simple, icerock_hmm, icerock_feedback):
            fp.write(str(i) + "\n")
