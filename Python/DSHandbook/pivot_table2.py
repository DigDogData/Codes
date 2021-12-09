#!/usr/bin/env python3

# pivot_table2.py: Example code for pivot table analysis using US birth data

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

births = pd.read_csv("Data/births.csv")
print(births.head())

print("----------------------------")
births["decade"] = 10 * (births["year"] // 10)
print(births.pivot_table("births", index="decade", columns="gender", aggfunc="sum"))
sns.set()  # set seaborn style
births.pivot_table("births", index="year", columns="gender", aggfunc="sum").plot()
plt.ylabel("total births per year")
plt.show()
