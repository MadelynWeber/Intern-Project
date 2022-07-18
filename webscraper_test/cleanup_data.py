from re import sub
import pandas as pd

input = "./data/collected_data.csv"
output = "./data/collected_data_cleaned.csv"

df = pd.read_csv(input)

print(df.head())
print(df.columns)
print(df.shape)

# removing punctuation from text in dataset
df['Review Text'] = df['Review Text'].str.replace(r'[^\w\s]+', '')
# removing any potential duplicates in the dataset
df.drop_duplicates(subset=None, inplace=True)
# removing any potential rows containing no data
df.dropna(how = 'all')

print(df.head())
print(df.shape)

df.to_csv(output, index=False)

