import pandas as pd
import re

df = pd.read_csv('../csvs/all_reviews.csv')

df['Negative_Review'] = df['Negative_Review'].apply(lambda x : re.sub(r'[^a-zA-Z0-9 ]+','', str(x)))
df['Positive_Review'] = df['Positive_Review'].apply(lambda x : re.sub(r'[^a-zA-Z0-9 ]+','', str(x)))

df['Negative_Review'] = df['Negative_Review'].apply(lambda x : re.sub(r'No Negative','', str(x)))
df['Positive_Review'] = df['Positive_Review'].apply(lambda x : re.sub(r'No Positive','', str(x)))

# remove this one because it have dutch reviews
df = df[df.Hotel_Name != 'Outside Inn']

df['Negative_Review'] = df['Negative_Review'].apply(lambda x : re.sub(r'nan','', str(x)))
df['Positive_Review'] = df['Positive_Review'].apply(lambda x : re.sub(r'nan','', str(x)))

df.to_csv('../csvs/clean.csv', sep=',', encoding='utf-8', index=False)
