import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

print("Loading dataset for Phase 2 ML Ranking...")

#  Load the generated Phase 1 dataset
df = pd.read_csv("influencers_phase1_filtered.csv")

#  Data Cleaning: Clean numeric fields & remove inf/NaN values
numeric_cols = ['Followers', 'Last 10 Posts Likes', 'Last 10 Posts Comments', 'Engagement Rate (%)']

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Clean or recalculate Engagement Rate (%) if inf or NaN occurs
df['Followers'] = df['Followers'].replace(0, np.nan).fillna(5000)
df['Last 10 Posts Likes'] = df['Last 10 Posts Likes'].fillna(0)
df['Last 10 Posts Comments'] = df['Last 10 Posts Comments'].fillna(0)

#  ((Likes + Comments) / (Followers * 10)) * 100
df['Engagement Rate (%)'] = np.round(
    ((df['Last 10 Posts Likes'] + df['Last 10 Posts Comments']) / (df['Followers'] * 10)) * 100, 2
)

# Replace any lingering infinity values with finite maximums or zeros
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df['Engagement Rate (%)'] = df['Engagement Rate (%)'].fillna(0)

# Clip extreme outliers to keep float64 values within safe limits
df['Engagement Rate (%)'] = np.clip(df['Engagement Rate (%)'], 0, 100)

print(f"Data cleaned successfully. Total profiles ready: {len(df)}")

# 3. Feature Engineering & Preprocessing
# Parse posting frequency integer
df['Posts_Per_Month'] = df['Posting Frequency'].str.extract(r'(\d+)').astype(float).fillna(12)

# Encode Categorical Variables
le_cat = LabelEncoder()
df['Category_Encoded'] = le_cat.fit_transform(df['Category'].astype(str))

le_auto = LabelEncoder()
df['Automation_Encoded'] = le_auto.fit_transform(df['Automation Usage'].astype(str))

# Define Features (X) and Target (y)
X = df[['Followers', 'Category_Encoded', 'Posts_Per_Month', 'Automation_Encoded']]
y = df['Engagement Rate (%)']

# Double-check finite values before model fit
X = X.fillna(0)
y = y.fillna(0)

# 4. Train Random Forest Ranking Model
print("Training Random Forest Regressor Model...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Predict engagement scores and AI ranking
df['Predicted_Engagement_Score'] = np.round(model.predict(X), 2)

# Compute Composite Influence Score for Final Ranking
df['Influence_Score'] = np.round(
    (df['Followers'] * 0.4) + (df['Predicted_Engagement_Score'] * 10000 * 0.6), 2
)

#  Rank Influencers Overall and Per Category
df_ranked = df.sort_values(by='Influence_Score', ascending=False).reset_index(drop=True)
df_ranked['Overall_Rank'] = df_ranked.index + 1

#  Final ML Ranked Outputs
df_ranked.to_csv("ranked_influencers.csv", index=False)
df_ranked.to_excel("ranked_influencers.xlsx", index=False)

print("\nSUCCESS: Phase 2 ML Ranking execution complete!")
print("Saved outputs as 'ranked_influencers.csv' and 'ranked_influencers.xlsx'.")