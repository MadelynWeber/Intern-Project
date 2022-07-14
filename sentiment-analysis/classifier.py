"Reads in contractor review data from web scraping code and classifies reviews on a 1-5 star scale"
from io import StringIO
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2
import numpy as np


def main():
    # ------------------------------------------------CLEAN REVIEWS FOR ANALYSIS ---------------------------------------------------
    df = pd.read_csv ('review_data.csv')
    # following lines of code drops duplicate reviews and any rows with empty values
    df.drop_duplicates(inplace = True)
    df.dropna(inplace = True)
    # line below removes reviews without any letters or numbers (eg. reviews with only punctuation, emojis)
    cleaned_df = df[df['ReviewText'].str.contains('[A-Za-z0-9]')]
    # temp.to_csv("temp.csv", index=False)
    cleaned_df.to_csv('cleaned_reviews.csv', index=False)

    # ------------------------------------------------ TEST REVIEWS ON ANALYSIS MODELS ---------------------------------------------------
    df = pd.read_csv ('cleaned_reviews.csv')
    df.head()
    tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 3))
    features = tfidf.fit_transform(df.ReviewText).toarray()
    labels = df.Rating
    Ratings = [1, 2, 3, 4, 5]
    features.shape
    N = 2
    for category_id in Ratings:
        features_chi2 = chi2(features, labels == category_id)
        indices = np.argsort(features_chi2[0])
        feature_names = np.array(tfidf.get_feature_names_out())[indices]
        unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
        bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
        trigrams = [v for v in feature_names if len(v.split(' ')) == 3]
        print("# '{}':".format(category_id))
        print("  . Most correlated unigrams:\n. {}".format('\n. '.join(unigrams[-N:])))
        print("  . Most correlated bigrams:\n. {}".format('\n. '.join(bigrams[-N:])))
        print("  . Most correlated trigrams:\n. {}".format('\n. '.join(trigrams[-N:])))
    

if __name__ == "__main__":
    main()