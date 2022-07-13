"Reads in contractor review data from web scraping code and classifies reviews on a 1-5 star scale"
from io import StringIO
import pandas as pd

def main():
    df = pd.read_csv ('review_data.csv')
    # following lines of code drops duplicate reviews and any rows with empty values
    df.drop_duplicates(inplace = True)
    df.dropna(inplace = True)
    # line below removes reviews without any letters or numbers (eg. reviews with only punctuation, emojis)
    cleaned_df = df[df['ReviewText'].str.contains('[A-Za-z0-9]')]
    # temp.to_csv("temp.csv", index=False)
    cleaned_df.to_csv('cleaned_reviews.csv', index=False)
    df = pd.read_csv ('cleaned_reviews.csv')
    print(df)
    # col = ['Rating', 'Review Text']
    # df = df[col]
    # df = df[pd.notnull(df['Consumer complaint narrative'])]
    # df.columns = ['Product', 'Consumer_complaint_narrative']
    # df['category_id'] = df['Product'].factorize()[0]
    # category_id_df = df[['Product', 'category_id']].drop_duplicates().sort_values('category_id')
    # category_to_id = dict(category_id_df.values)
    # id_to_category = dict(category_id_df[['category_id', 'Product']].values)
    # df.head()
    

if __name__ == "__main__":
    main()