import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../csvs/clean.csv")

sum_df = df.groupby(['Hotel_Name']).agg({'Negative_Review': 'count', 'Positive_Review': 'count'}).reset_index()
print(sum_df)

sum_df.plot(x="Hotel_Name", y=["Negative_Review", "Positive_Review"], kind="bar")
plt.savefig('../images/plot.png')
plt.show()