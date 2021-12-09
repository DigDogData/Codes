#!/usr/bin/env python3

# pivot_table.py: Example code for pivot table analysis

import pandas as pd
import seaborn as sns

titanic = sns.load_dataset("titanic")
print(titanic.head())
print("------------------------")

# pivot table by hand: survival by sex
print(titanic.groupby("sex")[["survived"]].mean())
print("------------------------")
# survival by sex & class: group by sex+class -> select 'survival' ->
print(titanic.groupby(["sex", "class"])["survived"].aggregate("mean").unstack())
print("------------------------")

# pivot table using pivot_table method
print(titanic.pivot_table("survived", index="sex", columns="class"))
print("------------------------")

# multilevel pivot table
age = pd.cut(titanic["age"], [0, 18, 80])
print(titanic.pivot_table("survived", index=["sex", age], columns="class"))
print("------------------------")
fare = pd.qcut(titanic["fare"], 2)  # compute quantiles
print(titanic.pivot_table("survived", index=["sex", age], columns=[fare, "class"]))
print("------------------------")
print(
    titanic.pivot_table(
        index="sex", columns="class", aggfunc={"survived": sum, "fare": "mean"}
    )
)
print("------------------------")
# compute total
print(
    titanic.pivot_table(
        "survived", index="sex", columns="class", margins_name="Total", margins=True
    )
)
