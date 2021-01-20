#!/usr/bin/python

# This module contains functions relevent to getting metrics from ASC files.

#from Scripts.Calibration.include.ascFile import *

import head as hd
from pathlib import Path


def calculate(populationFile):
    WEIGHTEDPFPR = Path("C:\\Users\\pua66\\PycharmProjects\\PSU-CIDD-Rwanda\\out\\weighted_pfpr.csv")#("out/weighted_pfpr.csv")

    NUMERATOR = 0
    DENOMINATOR = 1
    [ ascheader, district ] = hd.load_asc("C:\\Users\\pua66\\PycharmProjects\\PSU-CIDD-Rwanda\\GIS\\rwa_district.asc")#("../../GIS/rwa_district.asc")
    [ ascheader, pfpr ] = hd.load_asc("C:\\Users\\pua66\\PycharmProjects\\PSU-CIDD-Rwanda\\GIS\\rwa_pfpr2to10.asc")#("../../GIS/rwa_pfpr2to10.asc")
    [ ascheader, population ] = hd.load_asc(populationFile)

    data = {}
    totalPopulation = 0

    for row in range(ascheader['nrows']):
        for col in range(ascheader['ncols']):
            # Continue if there is no data
            if district[row][col] == ascheader['nodata']:
                continue

            # Create the district if it does not exist
            key = district[row][col]
            if not key in data.keys():
                data[key] = [0, 0]

            # Update the running values
            data[key][NUMERATOR] += pfpr[row][col] * population[row][col]
            data[key][DENOMINATOR] += population[row][col]
            totalPopulation += population[row][col]

    numerator = 0
    denominator = 0

    with open(WEIGHTEDPFPR, 'w') as out:
        for key in data.keys():
            numerator += data[key][NUMERATOR]
            denominator += data[key][DENOMINATOR]
            result = round((data[key][NUMERATOR] / data[key][DENOMINATOR]) * 100, 2)
            message = "District: {0}, PfPR: {1}%".format(int(key), result)
            
            out.write("{},{}\n".format(int(key), result))
            print(message)

    result = round(numerator * 100 / denominator, 2)
    print("\nFull Map, PfPR: {0}%".format(result))
    print("Population: {:,}\n".format(totalPopulation))


def simulatePopulation(fileName, rate, years, start):
    [ ascheader, data ] = hd.load_asc(fileName)

    # Apply the population adjustment
    initial = 0
    for row in range(ascheader['nrows']):
        for col in range(ascheader['ncols']):
            if data[row][col] == ascheader['nodata']: continue
            data[row][col] *= 0.25
            initial += data[row][col]
    print ("{}: {}".format(start, int(round(initial / 0.25))))

    # Apply the population growth
    for year in range(years):
        population = 0
        for row in range(ascheader['nrows']):
            for col in range(ascheader['ncols']):
                # Pass if there is no data
                if data[row][col] == ascheader['nodata']: continue

                # Update the population in this cell
                data[row][col] = data[row][col] * (1 + rate)

                # Update the running total
                population += data[row][col]

        print ("{}: {}".format(start + year + 1, int(round(population / 0.25))))


if __name__ == '__main__':
    calculate("C:\\Users\\pua66\\PycharmProjects\\PSU-CIDD-Rwanda\\GIS\\rwa_population.asc")#("../../GIS/rwa_population.asc")
