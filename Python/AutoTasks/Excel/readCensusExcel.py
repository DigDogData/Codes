#!/usr/bin/env python3

# readCensusExcel.py - Tabulates population and number of census tracts for each county

import openpyxl
import pprint
import census2010  # import only after creating it below


class ReadCensusData:

    # initializer
    def __init__(self, file_name, sheet):
        self.file_name = file_name
        self.sheet = sheet

    # method to save census data
    def save_census(self):

        # collect each county's population and tracts
        county_data = {}
        print("Reading rows...")
        for row in range(2, self.sheet.max_row + 1):
            # each row has data for one census tract
            state = self.sheet["B" + str(row)].value  # 'state' cell data
            county = self.sheet["C" + str(row)].value  # 'county' cell data
            pop = self.sheet["D" + str(row)].value  # 'pop' cell data

            # make sure keys for state and county exist before writing values to them
            # (setdefault() method sets value to a key if none exists, passes otherwise)
            county_data.setdefault(state, {})
            county_data[state].setdefault(county, {"tracts": 0, "pop": 0})

            # increment tract by 1 and popsize by population in this tract
            county_data[state][county]["tracts"] += 1
            county_data[state][county]["pop"] += int(pop)

        # write data to a file
        print("Writing results...")
        result_file = open(self.file_name, "w")
        result_file.write("allData = " + pprint.pformat(county_data))
        result_file.close()
        print("Done.")

        return None

    # method to show census data
    def show_census(self, state, county):
        county_pop = census2010.allData[state][county]["pop"]
        # print("The 2010 population of {%s} was {%s}", county, str(county_pop))
        print("The 2010 population of %s was %s" % (county, str(county_pop)))
        return None


if __name__ == "__main__":
    print("Opening workbook...")
    wb = openpyxl.load_workbook("Data/censuspopdata.xlsx")
    sheet = wb["Population by Census Tract"]  # read sheet by name
    file_name = "census2010.py"  # file to save/show processed census data
    ReadCensusData(file_name, sheet).save_census()
    # ReadCensusData(file_name, sheet).show_census("AK", "Anchorage")
    ReadCensusData(file_name, sheet).show_census("AL", "Baldwin")
