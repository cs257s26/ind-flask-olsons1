import csv
from pathlib import Path
import argparse

#File paths for load_csv
project_dir = Path(__file__).resolve().parent
data_dir = project_dir / "CSV-DATA" / "csv" #modified for the individual flask deliverable

def load_csv(csvName: str) -> list[str]:
    """
    Takes in a string name of a csv file located in the ProductionCode folder and then loads it using the csv module.
    """
    localData = []
    path = (data_dir / csvName).resolve()

    try:
        with open(path, newline="") as datafile:
            csv_file = csv.reader(datafile)
            for row in csv_file:
                localData.append(row)
    except FileNotFoundError as e:
        return None

    return localData

def get_specified_column(column_heading: str, data: list) -> list[str]:
    """
    Returns a specific column in the csv sheet (represented as a python list called "data"), provided a column heading 
    """

    if not data:
        return ([]) 

    header = data[0]

    """if the name is not in the headers, it does not exist so empty list"""
    if column_heading not in header:
        return ([])
    
    """if in header, then for loop and return everything in that column"""
    index = header.index(column_heading)
    column_values = []    

    for row in data[1:]:
        value = row[index]
        column_values.append(value)
    return (column_values)

def find_bird_name(bird: str, data: list) -> int:
    """
    finds the name of a bird given that the name of the bird is EXACTLY what is under the "Common Name (Scientific Name)" column in the spreadsheet.
    """

    bird_data = []
    bird_data = get_specified_column("Common Name (Scientific Name)" , data)
    for birdName in range(0, len(bird_data)):
        if (str(bird) == bird_data[birdName]):
            return(birdName)

def find_sightings_at_location(bird: str, stop: int, year: int) -> int:
    """
    returns an integer amount of the number of times a specific bird was sighted at one of the stops (numbered 1 through 17) in a given year
    """

    # get dataset of year
    data = load_csv(str(year) + ".csv")
    
    if data is None:
        return None
    
    # find index of bird row, if it exists
    bird_index = find_bird_name(bird, data)
    if bird_index is None:
        return 0

    # get the stop column and then index it with the bird's index in that specific row to return the count
    stop_column = get_specified_column(str(stop), data)

    # guard against out-of-range index
    if bird_index >= len(stop_column):
        return 0

    bird_count = stop_column[bird_index]    
    if bird_count == "p" or bird_count == "":
        return 0
        
    return int(bird_count)

def find_sightings_all_locations(bird: str, year: int) -> int:
    """
    returns an integer amount of the number 3of times a specific bird was sighted at all 17 stops in a given year
    """

    total_sightings = 0
    for stop in range (1, 18):
        sightingsIncrement = find_sightings_at_location(bird, stop, year)
        if sightingsIncrement is None:
            return None

        total_sightings += sightingsIncrement
    return total_sightings

def find_most_popular_stop(year: int) -> int:
    """
    returns an stop number (integer from 1-17) that had the most birds sighted at it within a given year
    """

    most_popular_stop_number = None
    most_popular_stop_sightings = 0

    data = load_csv(year + ".csv")

    if data is None:
        return None
    
    # loop through all stop locations and find total bird sightings for each
    for stop in range(1, 18):
        total_sightings = 0
        stop_column = get_specified_column(str(stop), data)

        for cell in stop_column:
            if cell in ("", "p"):
                continue
            try:
                total_sightings += int(cell)
            except ValueError:
                continue

        # set most popular stop number to new stop if its sightings are greater than the...
        # most popular that has been seen so far
        if total_sightings > most_popular_stop_sightings:
            most_popular_stop_number = stop
    
    return most_popular_stop_number

def main():
    parser = argparse.ArgumentParser(
        description = "Analyze the dataset from command line"
    )
    

    parser.add_argument(
        "--bird",
        default = "American Crow (Corvus brachyrhynchos) ",
        help = "Stop location"
    )

    parser.add_argument(
        "--stop",
        default = 1,
        help = "Stop location"
    )

    parser.add_argument(
        "--year",
        default = 2000,
        help = "Year dataset"
    )

    args = parser.parse_args()
    
    print(find_sightings_at_location(args.bird, args.stop, args.year))

if __name__ == "__main__":
    main()