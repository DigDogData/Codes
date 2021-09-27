#!/usr/bin/env python3

# readCensusExcel.py - Tabulates population and number of census tracts for each county

import openpyxl
import pprint


class ReadCensusData:

    # initializer
    def __init__(self):
        pass

    # method
    def read_census(self, sheet):

        # collect each county's population and tracts
        county_data = {}
        print("Reading rows...")
        for row in range(2, sheet.max_row + 1):
            # each row has data for one census tract
            state = sheet["B" + str(row)].value
            county = sheet["C" + str(row)].value
            pop = sheet["D" + str(row)].value

            # make sure keys for state and county exist before writing values to them
            # (setdefault() method sets value to a key if none exists, passes otherwise)
            county_data.setdefault(state, {})
            county_data[state].setdefault(county, {"tracts": 0, "pop": 0})

            # increment tract by 1 and popsize by population in this tract
            county_data[state][county]["tracts"] += 1
            county_data[state][county]["pop"] += int(pop)

        # write data to a file
        print("Writing results...")
        result_file = open("censusData2010.py", "w")
        result_file.write("allData = " + pprint.pformat(county_data))
        result_file.close()
        print("Done.")


if __name__ == "__main__":
    print("Opening workbook...")
    wb = openpyxl.load_workbook("censuspopdata.xlsx")
    sheet = wb["Population by Census Tract"]  # read sheet by name
    ReadCensusData.read_census(sheet)
