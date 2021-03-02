#! /usr/bin/env python

"""
Author       : shiv

Description  : Technical Test for Radar
"""
import sys
import pandas as pd
import math

usage = "Run the script: \"python radar_server_engineering n\" where n is an integer indicating the nth location"

if len(sys.argv)!=2:
    print(usage)
    sys.exit(0)

#Global Variables
list_of_stops=[]
soho_locations=[]
soho_hashmap={}

def place_table():
    print("")
    print("In the place_table function")

    # Paths to the csv files
    soho_file="/home/shiv/Stuff10/soho.csv"
    stops_file="/home/shiv/Stuff10/stops.csv"

    # Read in the csv file
    soho=pd.read_csv(soho_file)
    stops=pd.read_csv(stops_file)

    # Print out the csv files as a check
    #print(soho);
    #print(stops)

    # Create list for stops and soho locations from the data
    for index, row in stops.iterrows():
        list_of_stops.append((row['latitude'], row['longitude']))

    for index, row in soho.iterrows():
        soho_locations.append((row['name'],row['latitude'],row['longitude'],row['popularity']))

def place_retrieval(list_of_stops, soho_locations):
    print("")
    print("In the place_retrieval function")
    #print(soho_locations)

    # Create hashmap of list of stops (keys) and place "close enough" (values)
    for i in list_of_stops:
        soho_hashmap[i]=[]
        for j in soho_locations:
            degree_diff=math.sqrt((i[0]-j[1])**2 + (i[1]-j[2])**2)
            distance=degree_diff*111139
            #print('digree_diff is: ' + str(distance))

            # Choosing distance less than 12m as the radious,
            # (since the error is up to 10m and allowing for the 2m buffer)
            if(distance < 12):
                soho_hashmap[i].append(j)


def place_ranking(n):
    print("")
    print("In the place_ranking function")
    print("")
    print("The input coordinates are: ")
    print(soho_hashmap.keys()[n])
    print("")
    print("The closest coordinates are: ")
    print(soho_hashmap[soho_hashmap.keys()[n]])

    distance_dict={}
    for i in (soho_hashmap[soho_hashmap.keys()[n]]):
        degrees=math.sqrt((i[1]-soho_hashmap.keys()[n][0])**2+(i[2]-soho_hashmap.keys()[n][1])**2)
        distance_dict[i[0]]=degrees*111139

    print("")
    print("The most likely places for the user, in order of distance, with the distance (in metres), printed, are: ")
    sorted_distance_dict=sorted(distance_dict.items(), key=lambda x: x[1])
    for key in sorted_distance_dict:
        print(key)

def main():
    print("In the main function")
    place_table()
    place_retrieval(list_of_stops, soho_locations)
    place_ranking(int(sys.argv[1]))


if __name__ == "__main__":
    main()
