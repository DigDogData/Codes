#!/usr/bin/env python3

# pd_merge.py: Example merge code to rank US states/territories by 2010 population density

import pandas as pd

# read US population data
pop = pd.read_csv("Data/state-population.csv")
areas = pd.read_csv("Data/state-areas.csv")
abbrevs = pd.read_csv("Data/state-abbrevs.csv")

# print(pop.head())
# print(areas.head())
# print(abbrevs.head())

# merge population and state data using common keys
merged = pd.merge(
    pop, abbrevs, how="outer", left_on="state/region", right_on="abbreviation"
)
merged = merged.drop("abbreviation", axis=1)  # drop duplicate info column

print(merged.head())

# missing data (NaN)
print(merged.isnull().any())  # which, if any, column has missing data?
print(merged[merged["population"].isnull()].head())  # Puerto Rico pop < 2000 is NaN
# also Puerto Rico and USA do not have state abbreviation key
print(merged.loc[merged["state"].isnull(), "state/region"].unique())
# add state abbreviation key to missing data
merged.loc[merged["state/region"] == "PR", "state"] = "Puerto Rico"
merged.loc[merged["state/region"] == "USA", "state"] = "United States"
print(merged.isnull().any())

# merge area data to population (to estimate pop density)
final = pd.merge(merged, areas, on="state", how="left")
print(final.head())

# check for NaN
print(final.isnull().any())
# NaN area for United States as a whole
print(final["state"][final["area (sq. mi)"].isnull()].unique())
# drop null area (pop density for entire USA not important)
final.dropna(inplace=True)
print(final.isnull().any())

# select total pop data for year 2010
data2010 = final.query("year == 2010 & ages == 'total'")
print(data2010.head())
