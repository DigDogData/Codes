import scipy.stats as stats

"""
Data Grouping and Pivoting
"""
def group(df, feature1, feature2, label):
    # group data by types of feature1 & feature2 and compute mean label
    df2 = df[[feature1,feature2,label]]
    df2 = df2.groupby([feature1,feature2], as_index=False).mean()
    return df2

def pvot(df, feature1, feature2, label):
    # first group data
    df2 = group(df, feature1, feature2, label)
    # next create pivot table
    df2 = df2.pivot(index=feature1, columns=feature2)
    df2 = df2.fillna(0)     # replace NaN with 0
    return df2

"""
Pearson Correlation (returns correlation and significance)
"""
def corr(df, variable1, variable2):
    results = stats.pearsonr(df[variable1], df[variable2])
    return results

"""
ANOVA gives correlation of categorical variables. It is a statistical test of
whether means of two (or more) categorical groups are significantly different.
ANOVA assumes means of all groups are same, calculates how much actual means
deviate from this assumption, reports it as F-test score (higher score => more
different). Also reports significance of this score in terms of p-value.
Function below computes how two types/groups of a feature (e.g. make of a
car) impact label (e.g. car price), that is, if those are correlated
"""
def anova_pairwise(df, feature, label, type1, type2):
    # first group data by feature types/groups
    df2 = df[[feature,label]].groupby([feature])
    # compute one-way ANOVA for up to 5 feature groups (add code for >5)
    results = stats.f_oneway(df2.get_group(type1)[label],
                             df2.get_group(type2)[label])
    return results
    
# Function below computes how all types/groups of a feature impact label
# Currently written for <=5 feature types (add code for >5 types)
def anova_all(df, feature, label):
    df2 = df[[feature,label]].groupby([feature])
    names = df[feature].unique()    # names of all feature groups
    if len(names) == 2:
        results = stats.f_oneway(df2.get_group(names[0])[label],
                                 df2.get_group(names[1])[label])
    elif len(names) == 3:
        results = stats.f_oneway(df2.get_group(names[0])[label],
                                 df2.get_group(names[1])[label],
                                 df2.get_group(names[2])[label])
    elif len(names) == 4:
        results = stats.f_oneway(df2.get_group(names[0])[label],
                                 df2.get_group(names[1])[label],
                                 df2.get_group(names[2])[label],
                                 df2.get_group(names[3])[label])
    else:
        results = stats.f_oneway(df2.get_group(names[0])[label],
                                 df2.get_group(names[1])[label],
                                 df2.get_group(names[2])[label],
                                 df2.get_group(names[3])[label],
                                 df2.get_group(names[4])[label])
    return results
