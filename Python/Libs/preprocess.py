import pandas as pd
import numpy as np

##########################################################
################### Handling NaN data ####################
##########################################################
# drop NaN rows (axis=0 for row, axis=1 for column)
# index resetting needed because whole rows are dropped
def drop_na(df, variables):
    for variable in variables:
        df.dropna(subset=[variable], axis=0, inplace=True)
    df.reset_index(drop=True, inplace=True)

# replace NaN with mean for numerical variables
def replace_with_mean(df, variables):
    for variable in variables:
        mean = df[variable].astype("float64").mean(axis=0)
        df[variable].replace(np.nan, mean, inplace = True)

# replace NaN with most frequent value for categorical variables
# .idxmax() method finds most frequent value in .value_counts() method 
def replace_with_most(df, variables):
    for variable in variables:
        var = df[variable].value_counts().idxmax()
        df[variable].replace(np.nan, var, inplace=True)

##########################################################
################## Data Normalization ####################
##########################################################
# simple feature scaling (=x/x_max)
def simple_feature_scaling(df, variables):
    for variable in variables:
        df[variable] /= df[variable].max()
    return df

# min-max scaling ((=x-x_min)/(x_max-x_min))
def min_max(df, variables):
    for variable in variables:
        df[variable] = (df[variable] - df[variable].min()) / (df[variable].max() - df[variable].min())
    return df

# z-score scaling ((=x-mean)/std)
def z_score(df, variables):
    for variable in variables:
        df[variable] = (df[variable] - df[variable].mean()) / df[variable].std()
    return df

####################################################
########### Category to dummy conversion ###########
####################################################
def to_dummy(df, variables):
    for variable in variables:
        dummy_variable = pd.get_dummies(df[variable], prefix=variable, prefix_sep="-")
        df = pd.concat([df, dummy_variable], axis=1)    # axis=1 for columns
        df.drop(variable, axis=1, inplace=True)         # drop original column
    return df

####################################################
################## Data Binning ####################
####################################################
# uses numpy's linspace(start_val, end_val, bin numbers) function
# panda's cut() function assigns bin names to values
def bin_data(df, variable, names, binsize):
    bins = np.linspace(min(df[variable]), max(df[variable]), binsize)
    df[f"{variable}-binned"] = pd.cut(df[variable], bins, labels = names, include_lowest = True)
    return df

