import cv2
import numpy as np
from queue import PriorityQueue
import time


#---------------------------------------------Canvas Properties---------------------------------------------------------------------#
canvas_size = (500, 1200)  
canvas_height, canvas_width = canvas_size

canvas = np.ones((canvas_size[0], canvas_size[1], 3), dtype="uint8") * 255

#---------------------------------------------Drawing the hexagon using half planes--------------------------------------------------#
def draw_hexagon_using_half_planes(x,y):

    cx, cy = 650, 250
    side = 150
    r = side * np.cos(np.radians(30))  # radius of the hexagon
    y = abs(y - canvas_height)  # inverted to match the map given
    # Horizontal boundary points of the hexagon are calculated using the radius of the hexagon
    x_boundary_left , x_boundary_right  = cx - r, cx + r
    y_top = 325
    y_bottom = 175
    # diagoonal boundary line eqaution
    y_top_left = ((np.radians(30))*(x - x_boundary_left))+ y_top
    y_top_right = - ((np.radians(30))*(x - x_boundary_right))+ y_top
    y_bottom_right =  ((np.radians(30))*(x - x_boundary_right))+ y_bottom
    y_bottom_left = - ((np.radians(30))*(x - x_boundary_left))+ y_bottom

    # Check if the point is inside the hexagon
    if (x >= x_boundary_left and x <= x_boundary_right and y<= y_top_left and y>= y_bottom_left and y<= y_top_right and y>= y_bottom_right):
        return True
    else:
        return False
#---------------------------------------------Drawing the hexagon clearance using half planes--------------------------------------#   
def hex_clearance(x,y):
    cx, cy = 650, 250
    side = 150
    clearance = 5
    r = side * np.cos(np.radians(30)) + clearance  # radius of the hexagon
    y = abs(y - canvas_height)  # inverted to match the map given
    # Horizontal boundary points of the hexagon are calculated using the radius of the hexagon
    x_boundary_left , x_boundary_right  = cx - r, cx + r
    y_top = 325
    y_bottom = 175
    # diagoonal boundary line eqaution
    y_top_left = ((np.radians(30))*(x - x_boundary_left))+ y_top + clearance
    y_top_right = - ((np.radians(30))*(x - x_boundary_right))+ y_top + clearance
    y_bottom_right =  ((np.radians(30))*(x - x_boundary_right))+ y_bottom - clearance
    y_bottom_left = - ((np.radians(30))*(x - x_boundary_left))+ y_bottom - clearance

    # Check if the point is inside the hexagon
    if (x >= x_boundary_left and x <= x_boundary_right and y<= y_top_left and y>= y_bottom_left and y<= y_top_right and y>= y_bottom_right):
        return True
    else:
        return False
#---------------------------------------------Drawing the obstacles using half planes-----------------------------------------------#    
for x in range(canvas_width):
    for y in range(canvas_height):
        if hex_clearance(x, y):
            canvas[y, x] = (0, 0, 255)
        if draw_hexagon_using_half_planes(x, y):
            canvas[y, x] = (0, 0, 0)
            
#---------------------------------------------Drawing the rectangular obstacles using half planes-----------------------------------------------#
# Function to draw a rectangular obstacles using half planes
def renctangular_obstacles(x,y):
    y = abs(y - canvas_height) # inverted to match the map given
    obstacles_rectangles = [
        (x >= 100 and x <= 175 and y >= 100 and y <= 500), 
        (x >= 275 and x <= 350 and y >= 0 and y <= 400),
        (x >= 900 and x <= 1100 and y >= 50 and y <= 125),
        (x >= 900 and x <= 1100 and y >= 375 and y <= 450),
        (x >= 1020 and x <= 1100 and y >= 50 and y <= 450),        
    ]
    return any(obstacles_rectangles)
#---------------------------------------------Drawing the clearance using half planes-----------------------------------------------#
def rectangular_clearance(x, y):
    clearance = 5
    y = abs(y - canvas_height) # inverted to match the map given
    clearance = [
        (x >= 100 - clearance and x <= 175 + clearance and y >= 100 - clearance and y <= 500 + clearance),
        (x >= 275 - clearance and x <= 350 + clearance and y >= 0 - clearance and y <= 400 + clearance),
        (x >= 900 - clearance and x <= 1100 + clearance and y >= 50 - clearance and y <= 125 + clearance),
        (x >= 1020 - clearance and x <= 1100 + clearance and y >= 50 - clearance and y <= 450 + clearance),
        (x >= 900 - clearance and x <= 1100 + clearance and y >= 375 - clearance and y <= 450 + clearance),
        (x <= clearance or x >= canvas_width - clearance or y <= clearance or y >= canvas_height - clearance),
    ]
    return any(clearance)

for x in range(canvas_width):
    for y in range(canvas_height):
        if rectangular_clearance(x, y):
            canvas[y, x] = (0, 0, 255)
        if renctangular_obstacles(x, y):
            canvas[y, x] = (0, 0, 0)

#---------------------------------------------Finding whether the node is in free space or not---------------------------------------#
def is_free_space(x, y):
    return np.array_equal(canvas[y, x], [255, 255, 255])

