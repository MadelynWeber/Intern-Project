import pandas as pd

def main():
    df = pd.read_csv ('review_data.csv')
    df.drop_duplicates(inplace = True)

if __name__ == "__main__":
    main()