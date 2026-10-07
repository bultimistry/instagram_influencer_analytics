import pandas as pd

df = pd.read_csv("influencers_phase1_filtered.csv")
print(df[['Name / Username', 'Followers', 'Last 10 Posts Likes', 'Last 10 Posts Comments', 'Engagement Rate (%)']].head())