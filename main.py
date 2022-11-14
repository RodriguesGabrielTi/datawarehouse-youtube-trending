import pandas as pd

df = pd.read_csv('ratings_Books.csv', names=["reviewer_id", "asin", "overall", "unix_review_time"], nrows=1000)
df_json = pd.read_json('Books_5.json', lines=True, nrows=1000000)
print(df_json)
