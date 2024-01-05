import pandas as pd
from pandas.core.frame import DataFrame
from sqlalchemy import create_engine

df = pd.read_csv('../csvs/clean.csv')

df_labeled_neg = DataFrame()
df_labeled_pos = DataFrame()

df_labeled_neg[['hotel', 'review']] = df[['Hotel_Name', 'Negative_Review']]
df_labeled_pos[['hotel', 'review']] = df[['Hotel_Name', 'Positive_Review']]
df_labeled_neg['label'] = 0
df_labeled_pos['label'] = 1

dataframes = [df_labeled_pos, df_labeled_neg]
df = pd.concat(dataframes)

engine = create_engine('mysql+mysqlconnector://root:root@localhost/hotel_reviews', pool_recycle=3600, pool_size=5)

df.to_sql(name='reviews',con=engine,if_exists='fail',index=False,chunksize=1000) 