"Reads in contractor review data from web scraping code and classifies reviews on a 1-5 star scale"
from io import StringIO
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
from sklearn.feature_selection import chi2
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# ------------------------------------------------CLEAN REVIEWS FOR ANALYSIS ---------------------------------------------------
def cleanReviews():
    df = pd.read_csv ('review_data.csv')
    # following lines of code drops duplicate reviews and any rows with empty values
    df.drop_duplicates(inplace = True)
    df.dropna(inplace = True)
    # line below removes reviews without any letters or numbers (eg. reviews with only punctuation, emojis)
    cleaned_df = df[df['ReviewText'].str.contains('[A-Za-z0-9]')]
    cleaned_df.to_csv('cleaned_reviews.csv', index=False)

def main():
    #  cleanReviews()

    # ------------------------------------------------ TEST REVIEWS ON ANALYSIS MODELS ---------------------------------------------------
    with open("temp.txt", "w", encoding="ISO-8859-1") as f:
        df = pd.read_csv('cleaned_reviews.csv')
        tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 3))
        features = tfidf.fit_transform(df.ReviewText).toarray()
        f.write(str(features) + '\n')
        labels = df.Rating
        Ratings = [1, 2, 3, 4, 5, ]
        N = 5
        for category_id in Ratings:
            features_chi2 = chi2(features, labels == category_id)
            f.write(str(features_chi2))
            indices = np.argsort(features_chi2[0])
            feature_names = np.array(tfidf.get_feature_names_out())[indices]
            unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
            bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
            trigrams = [v for v in feature_names if len(v.split(' ')) == 3]
            print("# '{}':".format(category_id))
            print("  . Most correlated unigrams:\n. {}".format('\n. '.join(unigrams[-N:])))
            print("  . Most correlated bigrams:\n. {}".format('\n. '.join(bigrams[-N:])))
            print("  . Most correlated trigrams:\n. {}".format('\n. '.join(trigrams[-N:])))
    # ------------------------------------------------ NAIVE BAYES CLASSIFIER  ---------------------------------------------------

    X_train, X_test, y_train, y_test = train_test_split(df['ReviewText'], df['Rating'], random_state = 0)
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(X_train)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    clf = MultinomialNB().fit(X_train_tfidf, y_train)

    # ------------------------------------------COMPARE DIFFERING MACHINE LEARNING MODELS  ------------------------------------------------
    models = [
        RandomForestClassifier(n_estimators=200, max_depth=3, random_state=0),
        LinearSVC(),
        MultinomialNB(),
        LogisticRegression(random_state=0),
    ]
    CV = 5
    cv_df = pd.DataFrame(index=range(CV * len(models)))
    entries = []
    for model in models:
        model_name = model.__class__.__name__
        accuracies = cross_val_score(model, features, labels, scoring='accuracy', cv=CV)
        for fold_idx, accuracy in enumerate(accuracies):
            entries.append((model_name, fold_idx, accuracy))
    cv_df = pd.DataFrame(entries, columns=['model_name', 'fold_idx', 'accuracy'])
    
    sns.boxplot(x='model_name', y='accuracy', data=cv_df)
    sns.stripplot(x='model_name', y='accuracy', data=cv_df, 
                size=8, jitter=True, edgecolor="gray", linewidth=2)
    plt.show()
    print(cv_df.groupby('model_name').accuracy.mean())

    # ------------------------------------------ MODEL EVALUATION  ------------------------------------------------
    model = LinearSVC()
    X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(features, labels, df.index, test_size=0.33, random_state=0)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    from sklearn.metrics import confusion_matrix
    conf_mat = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots(figsize=(10,10))
    sns.heatmap(conf_mat, annot=True, fmt='d',
                xticklabels=Ratings, yticklabels=Ratings)
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.show()


if __name__ == "__main__":
    main()