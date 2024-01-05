import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import matplotlib.pyplot as plt

df = pd.read_csv("../csvs/clean.csv", index_col=0)

print(df.head())

text = []

for i in range(df.shape[0]):
    text.append(str(df['Positive_Review'][i]))
    text.append(str(df['Negative_Review'][i]))

text = ''.join(text)

wordcloud = WordCloud(background_color='white').generate(text)

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
wordcloud.to_file("../images/wordcloud.png")