# -*- coding: utf-8 -*-
"""Data Scrapping.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1qzCYsQ7y3J4EQo-xMJODgyP1OIJeJEi6
"""

import pandas as pd

"""scrapping Data"""

!pip install google-play-scraper

from google_play_scraper import app, reviews_all

app_bca = 'com.bca'
app_info = app(app_bca)

# country indonesia
reviews = reviews_all(
    app_bca,
    lang='id',
    country='id'
)

# Membuat DataFrame dari hasil review
dataframe = pd.DataFrame(reviews)

# lihat isi dari kolom
dataframe.info()

dataframe.head()

dataframe.shape

dataframe['reviewCreatedVersion'].unique()

# memfilter data berdasarkan tahun
data = dataframe[dataframe['at'].dt.year == 2024]

data.head()

data.shape

# Save data to excel
data.to_excel('data2.xlsx', index=False)

# Download file to laptop
from google.colab import files
files.download('data2.xlsx')