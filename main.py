import pandas as pd
import math
import random

def read_parser(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

        city_data_start = False
        city_info = []

        for line in lines:
            if "NODE_COORD_SECTION" in line:
                city_data_start = True
                continue
            if "EOF" in line:
                break
            if city_data_start:
                parts = line.strip().split()
                city_info.append((int(parts[0]),float(parts[1]),float(parts[2])))

    df = pd.DataFrame(city_info, columns = ["ID", "X", "Y"])
    return df

file_path = "berlin11_modified.tsp"
rp_df = read_parser(file_path)
print(rp_df)

def cities_distance(city1,city2):
    x1, y1 = city1["X"], city1["Y"]
    x2, y2 = city2["X"], city2["Y"]

    result = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return round(result)
city1 = rp_df.iloc[0]
city2 = rp_df.iloc[1]
#print(cities_distance(city1,city2))

cities_list = []
num_cities = rp_df.shape[0]
for i in range(1,num_cities + 1):
    cities_list.append(i)

#random.shuffle(cities_list)

def fitness(cities_list):
    total_distance = 0
    cities_len = len(cities_list)
    for idx in range(0,cities_len):
        city1_idx = cities_list[idx] - 1
        city2_idx = cities_list[(idx + 1) % cities_len] - 1

        city1 = rp_df.iloc[city1_idx]
        city2 = rp_df.iloc[city2_idx]
        dist = cities_distance(city1,city2)
        total_distance = total_distance + dist

    return(total_distance)


def info():
    print(cities_list)
    print(f"The total distance is {fitness(cities_list)}")


info()

def greedy_algorithm(starting_city):
    num_cities = rp_df.shape[0]
    visited = []
    current_city = starting_city 
    tour = [current_city + 1]
    total_distance = 0





        
