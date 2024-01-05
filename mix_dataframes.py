import pandas as pd
import numpy as np

# get the reviews
df_hotel_reviews = pd.read_csv('../csvs/Hotel_Reviews.csv')
df_peter_scrapped_reviews = pd.read_csv('../csvs/scrapped_reviews_peter.csv', sep=';')
df_my_scrapped_reviews_booking = pd.read_csv('../csvs/scrapped_reviews_booking.csv')
df_my_scrapped_reviews_hotelscom = pd.read_csv('../csvs/scrapped_reviews_hotelscom.csv')

# prepare hotel reviews
df_hotel_reviews = df_hotel_reviews[['Hotel_Name', 'Negative_Review', 'Positive_Review']]

# prepare peter scrapped reviews
df_peter_scrapped_reviews['Hotel_Name'] = 'InterContinental Amstel Amsterdam'
df_peter_scrapped_reviews['Negative_Review'] = df_peter_scrapped_reviews['review'].loc[df_peter_scrapped_reviews['rating'] < 25]
df_peter_scrapped_reviews['Positive_Review'] = df_peter_scrapped_reviews['review'].loc[df_peter_scrapped_reviews['rating'] >= 25]

df_peter_scrapped_reviews = df_peter_scrapped_reviews[['Hotel_Name', 'Negative_Review', 'Positive_Review']]

# prepare my scrapped reviews
# booking.com reviews were ready
# hotels.com need this preparation
df_my_scrapped_reviews_hotelscom['Hotel_Name'] = df_my_scrapped_reviews_hotelscom['Hotel_name']

df_my_scrapped_reviews_hotelscom['Negative_Review'] = df_my_scrapped_reviews_hotelscom['Review'].loc[df_my_scrapped_reviews_hotelscom['mark'] <= 6.0]
df_my_scrapped_reviews_hotelscom['Positive_Review'] = df_my_scrapped_reviews_hotelscom['Review'].loc[df_my_scrapped_reviews_hotelscom['mark'] > 6.0]

df_my_scrapped_reviews_hotelscom = df_my_scrapped_reviews_hotelscom[['Hotel_Name', 'Negative_Review', 'Positive_Review']]

# my own reviews
names = [
    'NH Collection Amsterdam Grand Hotel Krasnapolsky',
    'Ambassade Hotel',
    'The Hoxton, Amsterdam',
    'Hotel Jakarta Amsterdam',
    'Banks Mansion',
    'Hotel Estherea',
    'Mr. Jordaan Hotel',
    'NH CollectionAmsterdam Grand Hotel Krasnapolsky',
    'nhow Amsterdam RAI',
    "The Hendrick's Hotel"
]
bad_reviews = [
    'room service was so bad and the floor was dirty',
    'the location is not good beause it is very far from the city center',
    'breakfast was cold and little varied',
    'the room had bad views',
    'I do not like how the workers treat customers',
    'the cleaners did not come the whole trip',
    'you could hear the next room through the walls',
    'the smell in the hall was so bad and disgusting',
    'there was no parking near the hotel',
    'it was too expensive for what it offered'
]
good_reviews = [
    'there was a metro stop very close and it was very well connected',
    'room service was very fast and very friendly',
    'everything was clean and the room had very good light',
    'the views of the canals were beautiful',
    'the hotel offers any activities for tourists',
    'it was great value for money despite being high season',
    'the room was huge and so was the bed',
    'loved the bathtub and bathroom decor',
    'the breakfast was delicious and I loved that it was open late so I did not have to get up early',
    'I really liked how quickly they served you in the hotel restaurant'
]

my_reviews = {'Hotel_Name': names, 'Negative_Review': bad_reviews, 'Positive_Review': good_reviews}
df_my_own_reviews = pd.DataFrame(data=my_reviews)

# mixing the dataframes
dataframes = [df_hotel_reviews, df_peter_scrapped_reviews, df_my_scrapped_reviews_booking, df_my_scrapped_reviews_hotelscom, df_my_own_reviews]
df = pd.concat(dataframes)
#df.to_csv('../csvs/all_reviews.csv', sep=',', encoding='utf-8', index=False)