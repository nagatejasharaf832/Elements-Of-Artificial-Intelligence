#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: Allen Fox,nasharaf,lkota
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#


# !/usr/bin/env python3
from math import inf, tan
from math import radians, cos, sin, asin, sqrt
import sys
import math

"""
take input file as argument and return list of tuples
Eg:
Inp:-
'Bedford,_Indiana', '21', '52', 'IN_37'
'Cincinnati,_Indiana', '16', '45', 'IN_45'
out:-
[('Bedford,_Indiana', '21', '52', 'IN_37'),('Cincinnati,_Indiana', '16', '45', 'IN_45')]
"""
def parse_file(input_file):
    data = []
    f = open(input_file,"r+")
    
    for line in f:
        c = (line.split())
        data.append(c)
    return data



# Here comes the calculated delivery time for a node
def delivery_time(speed,dis,trip,time):
    d = 0
    if(int(speed)>=50):
        d = d+time+((tan(dis/1000))*(2*(time+trip)))
    else:
        d=d+time
    return d

# haversine distance calculation
def heuristic(city1,city2,city_data,cost,speed):
    distance=[]
    for i in city_data:
        if len(distance) == 4:
            lon1, lat1, lon2, lat2 = map(radians, [distance[1], distance[0], distance[3], distance[2]])
            lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

            # haversine formula 
            dlon = lon2 - lon1 
            dlat = lat2 - lat1 
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * asin(sqrt(a)) 
            r = 3956
            disss = c *r # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
            if(cost == "time" or cost == "delivery"):
                return disss/float(speed)
            if(cost=="segments"):
                return disss/90
            return disss
        if ((i[0]) == city1 or (i[0] == city2)):
            distance.append(float(i[1]))
            distance.append(float(i[2]))

# search for successors in bi-directional and return successors in an array
def findSuccessors(state,road_segments_data,city_gps_data,cost):
    succ=[]
    for i in road_segments_data:
        # bidrectional conditions
        if(i[0]==state[0]):
           route_taken =  state[5].copy()
           route_taken.append((i[1],i[4][:-1]+' for '+i[2]+' miles'))
           heu = heuristic(state[0],i[1],city_gps_data,cost,i[2]) if heuristic(state[0],i[1],city_gps_data,cost,i[2]) else 0
           succ.append((i[1],
                        state[1]+1,
                        state[2]+float(i[2]),
                        state[3]+(float(i[2])/float(i[3])),
                        state[4]+float(delivery_time(float(i[3]),float(i[2]),state[3],(float(i[2])/float(i[3])))),
                        route_taken,
                        heu))
        elif(i[1]==state[0]):
            route_taken =  state[5].copy()
            route_taken.append((i[0],i[4][:-1]+' for '+i[2]+' miles'))
            if(cost):
                heu = heuristic(state[0],i[0],city_gps_data,cost,i[2]) if heuristic(state[0],i[0],city_gps_data,cost,i[2]) else 0
            succ.append((i[0],
                        state[1]+1,
                        state[2]+float(i[2]),
                        state[3]+(float(i[2])/float(i[3])),
                        state[4]+float(delivery_time(float(i[3]),float(i[2]),state[3],(float(i[2])/float(i[3])))),
                        route_taken,
                        heu))
           
    return succ

# This function will pop out the least a*star value from fringe
def a_star_pop(fringe):
    mini = 0
    minii = inf
    for i in range(0,len(fringe)):
        if(fringe[i][0]<minii):
            (a,(b)) = fringe[i] 
            mini = i
            minii = a
    (c,(d)) = fringe[0]
    fringe[0] = (a,(b))
    fringe[mini] = (c,(d))
    return fringe

# Here is the main function to get the route from start city to end city
def get_route(start, end, cost):
    # parse files
    road_segments_data = parse_file("road-segments.txt")
    city_gps_data = parse_file("city-gps.txt")
    i = 1
    if(cost == "segments"):
        i = 1
    elif(cost == "distance"):
        i = 2
    elif(cost == "time"):
        i = 3
    elif(cost == "delivery"):
        i = 4
    fringe = [(0,(start,0,0,0,0,[],0))]
    #        [(a*value,(start,segments,miles,hours,delivery_hours,route_taken,heuristic_value,flag_value)]
    visited = []
    while(fringe):
        # decide which successor should call next
        state  = a_star_pop(fringe)
        # getting all the successors for start node
        successors = findSuccessors(state.pop(0)[1],road_segments_data,city_gps_data,cost)
        for succ in successors:
            if(succ[0]==end):
                return {"total-segments" : succ[1], 
                        "total-miles" : succ[2], 
                        "total-hours" : succ[3], 
                        "total-delivery-hours" : succ[4], 
                        "route-taken" : succ[5]}
            else:
                if succ[0] not in visited:
                    if(cost == "delivery"):
                        if(isinstance(succ[i],tuple)):
                            a_star_value = succ[6]+succ[i][0]
                        else:
                            a_star_value = succ[6]+succ[i]
                    else: 
                        a_star_value = succ[6]+succ[i]
                    visited.append(succ[0])
                    fringe.append((a_star_value,succ))


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)
    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print(step)
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])