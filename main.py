import pandas as pd

def read_parser():
    with open("berlin11_modified.tsp", "r") as file:
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

    df = pd.DataFrame(city_info)

    print(df)


read_parser()


        
