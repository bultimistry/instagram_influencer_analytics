import pandas as pd
import numpy as np
import re

from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, accuracy_score


print("=" * 75)
print("SR NEXT - PHASE 2 AI/ML ANALYTICS & RANKING")
print("=" * 75)



# 1. LOAD PHASE 1 DATA


print("\n[1/8] Loading Phase 1 profile dataset...")

profiles = pd.read_csv("influencers_phase1_filtered.csv")
posts = pd.read_csv("final_influencer_posts.csv")

print(f"Profiles loaded : {len(profiles):,}")
print(f"Posts loaded    : {len(posts):,}")



# 2. CLEAN POST DATA


print("\n[2/8] Preparing real Instagram post data...")

posts["ownerUsername"] = (
    posts["ownerUsername"]
    .astype(str)
    .str.strip()
    .str.lower()
)

posts["ownerUsername"] = (
    posts["ownerUsername"]
    .str.replace("@", "", regex=False)
)

posts["likesCount"] = pd.to_numeric(
    posts["likesCount"], errors="coerce"
).fillna(0)

posts["commentsCount"] = pd.to_numeric(
    posts["commentsCount"], errors="coerce"
).fillna(0)

posts["caption"] = posts["caption"].fillna("").astype(str)

posts["timestamp"] = pd.to_datetime(
    posts["timestamp"], errors="coerce"
)

posts = posts.dropna(subset=["ownerUsername"])

print(f"Clean posts: {len(posts):,}")



# 3. NLP / CONTENT CLASSIFICATION


print("\n[3/8] Performing NLP content classification...")


def classify_content(text):
    text = text.lower()

    categories = {
        "fashion": [
            "fashion", "outfit", "style", "dress", "clothing",
            "look", "wear", "beauty", "makeup"
        ],
        "food": [
            "food", "recipe", "restaurant", "cooking", "eat",
            "delicious", "cake", "pizza", "lunch", "dinner"
        ],
        "travel": [
            "travel", "trip", "vacation", "tour", "hotel",
            "beach", "flight", "holiday", "destination"
        ],
        "fitness": [
            "fitness", "gym", "workout", "exercise", "health",
            "training", "muscle", "running"
        ],
        "technology": [
            "technology", "tech", "software", "computer",
            "ai", "python", "coding", "programming"
        ],
        "beauty": [
            "beauty", "makeup", "skincare", "skin", "cosmetic",
            "lipstick", "hair"
        ],
        "family": [
            "family", "baby", "kids", "child", "mother",
            "father", "parent"
        ]
    }

    scores = {}

    for category, keywords in categories.items():
        scores[category] = sum(
            1 for word in keywords if word in text
        )

    best_category = max(scores, key=scores.get)

    if scores[best_category] == 0:
        return "general"

    return best_category


posts["Content_Category"] = posts["caption"].apply(
    classify_content
)

posts["Caption_Length"] = posts["caption"].str.len()

posts["Hashtag_Count"] = posts["caption"].apply(
    lambda x: len(re.findall(r"#\w+", x))
)

print("NLP classification completed.")



# 4. FEATURE ENGINEERING


print("\n[4/8] Creating influencer features...")


post_features = (
    posts.groupby("ownerUsername")
    .agg(
        Posts_Analyzed=("ownerUsername", "count"),
        Avg_Likes=("likesCount", "mean"),
        Avg_Comments=("commentsCount", "mean"),
        Total_Likes=("likesCount", "sum"),
        Total_Comments=("commentsCount", "sum"),
        Avg_Caption_Length=("Caption_Length", "mean"),
        Avg_Hashtags=("Hashtag_Count", "mean"),
        NLP_Content=("Content_Category", lambda x: x.mode().iloc[0]
                     if not x.mode().empty else "general")
    )
    .reset_index()
)

# Interaction rate based on average likes + comments
post_features["Avg_Interactions"] = (
    post_features["Avg_Likes"] +
    post_features["Avg_Comments"]
)


# Merge with profiles
profiles["username"] = (
    profiles["Name / Username"]
    .astype(str)
    .str.strip()
    .str.lower()
)

profiles["username"] = (
    profiles["username"]
    .str.replace("@", "", regex=False)
)

profiles["Followers"] = pd.to_numeric(
    profiles["Followers"], errors="coerce"
).fillna(0)

profiles["Engagement Rate (%)"] = pd.to_numeric(
    profiles["Engagement Rate (%)"], errors="coerce"
).fillna(0)

profiles["Category"] = (
    profiles["Category"]
    .fillna("other")
    .astype(str)
)

df = profiles.merge(
    post_features,
    left_on="username",
    right_on="ownerUsername",
    how="left"
)

df["Posts_Analyzed"] = df["Posts_Analyzed"].fillna(0)
df["Avg_Likes"] = df["Avg_Likes"].fillna(0)
df["Avg_Comments"] = df["Avg_Comments"].fillna(0)
df["Avg_Caption_Length"] = df["Avg_Caption_Length"].fillna(0)
df["Avg_Hashtags"] = df["Avg_Hashtags"].fillna(0)

df["NLP_Content"] = df["NLP_Content"].fillna("unknown")


# Post frequency
df["Posts_Per_Month"] = pd.to_numeric(
    df["Posting Frequency"]
    .astype(str)
    .str.extract(r"([\d.]+)")[0],
    errors="coerce"
).fillna(0)


# Hashtag diversity approximation
df["Hashtag_Diversity"] = np.minimum(
    df["Avg_Hashtags"] / 10,
    1
)


print(f"Feature dataset created: {len(df):,} influencers")



# 5. ENGAGEMENT PREDICTION MODEL


print("\n[5/8] Training engagement prediction model...")


feature_columns = [
    "Followers",
    "Posts_Analyzed",
    "Avg_Likes",
    "Avg_Comments",
    "Avg_Caption_Length",
    "Avg_Hashtags",
    "Posts_Per_Month",
    "Hashtag_Diversity"
]

X = df[feature_columns].replace(
    [np.inf, -np.inf], np.nan
).fillna(0)

y = df["Engagement Rate (%)"].fillna(0)

# Only train on profiles with real observed engagement
real_engagement = (
    df["Posts_Analyzed"] > 0
)

X_real = X[real_engagement]
y_real = y[real_engagement]

if len(X_real) >= 20:

    X_train, X_test, y_train, y_test = train_test_split(
        X_real,
        y_real,
        test_size=0.20,
        random_state=42
    )

    engagement_model = RandomForestRegressor(
        n_estimators=150,
        random_state=42,
        max_depth=10
    )

    engagement_model.fit(X_train, y_train)

    predictions = engagement_model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)

    print(f"Training profiles : {len(X_train)}")
    print(f"Testing profiles  : {len(X_test)}")
    print(f"MAE               : {mae:.4f}")

    # Predict for every influencer
    df["Predicted_Engagement"] = engagement_model.predict(X)

else:

    print("Not enough real engagement profiles for ML training.")
    print("Using observed engagement values.")

    df["Predicted_Engagement"] = y


# Keep sensible values
df["Predicted_Engagement"] = (
    df["Predicted_Engagement"]
    .replace([np.inf, -np.inf], np.nan)
    .fillna(0)
    .clip(lower=0)
)



# 6. AUTOMATION ADOPTION ANALYSIS


print("\n[6/8] Creating automation adoption prediction...")


# not a claim that the influencer actually uses automation.

df["Automation_Likelihood"] = (
    (
        np.log1p(df["Followers"]) /
        np.log1p(df["Followers"].max())
    ) * 0.35
    +
    np.minimum(df["Posts_Per_Month"] / 30, 1) * 0.25
    +
    np.minimum(df["Posts_Analyzed"] / 10, 1) * 0.20
    +
    df["Hashtag_Diversity"] * 0.20
) * 100

df["Automation_Likelihood"] = (
    df["Automation_Likelihood"]
    .clip(0, 100)
    .round(2)
)

print("Automation likelihood generated from observable activity features.")
print("No fake automation labels were created.")



# 7. FINAL AI INFLUENCE RANKING


print("\n[7/8] Calculating final influencer ranking...")


# Normalize components to 0-100
def minmax(series):
    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        return pd.Series(0, index=series.index)

    return (
        (series - minimum) /
        (maximum - minimum)
    ) * 100


df["Follower_Score"] = minmax(
    np.log1p(df["Followers"])
)

df["Engagement_Score"] = minmax(
    df["Predicted_Engagement"]
)

df["Activity_Score"] = minmax(
    df["Posts_Per_Month"]
)

df["NLP_Content_Score"] = minmax(
    df["Avg_Hashtags"] +
    df["Avg_Caption_Length"] / 100
)


# Assignment-oriented composite score
df["Influence_Score"] = (
    df["Follower_Score"] * 0.30
    +
    df["Engagement_Score"] * 0.35
    +
    df["Activity_Score"] * 0.15
    +
    df["NLP_Content_Score"] * 0.10
    +
    df["Automation_Likelihood"] * 0.10
)

df["Influence_Score"] = df[
    "Influence_Score"
].round(2)


# Overall ranking
df = df.sort_values(
    "Influence_Score",
    ascending=False
).reset_index(drop=True)

df["Overall_Rank"] = (
    df.index + 1
)


# Category ranking
df["Category_Rank"] = (
    df.groupby("Category")["Influence_Score"]
    .rank(
        ascending=False,
        method="first"
    )
    .astype(int)
)



# 8. SAVE FINAL OUTPUTS


print("\n[8/8] Saving final Phase 2 outputs...")


output_columns = [
    "Overall_Rank",
    "Category_Rank",
    "Name / Username",
    "Instagram handle",
    "Followers",
    "Category",
    "Engagement Rate (%)",
    "Predicted_Engagement",
    "Posts_Analyzed",
    "Avg_Likes",
    "Avg_Comments",
    "Posts_Per_Month",
    "Avg_Hashtags",
    "Hashtag_Diversity",
    "NLP_Content",
    "Automation_Likelihood",
    "Influence_Score"
]

final_df = df[
    [c for c in output_columns if c in df.columns]
].copy()


final_df.to_csv(
    "ranked_influencers.csv",
    index=False
)

final_df.to_excel(
    "ranked_influencers.xlsx",
    index=False
)


# Top influencers by category
top_by_category = (
    final_df
    .sort_values(
        ["Category", "Category_Rank"]
    )
    .groupby("Category")
    .head(10)
)

top_by_category.to_csv(
    "top_10_influencers_by_category.csv",
    index=False
)


# Feature importance
if "engagement_model" in locals():

    importance = pd.DataFrame({
        "Feature": feature_columns,
        "Importance": engagement_model.feature_importances_
    }).sort_values(
        "Importance",
        ascending=False
    )

    importance.to_csv(
        "engagement_model_feature_importance.csv",
        index=False
    )


print("\n" + "=" * 75)
print("PHASE 2 COMPLETED SUCCESSFULLY")
print("=" * 75)

print(f"\nTotal influencers ranked : {len(final_df):,}")
print(f"Real post accounts       : {(df['Posts_Analyzed'] > 0).sum():,}")

print("\nTop 10 Influencers:")
print(
    final_df[
        [
            "Overall_Rank",
            "Name / Username",
            "Category",
            "Followers",
            "Influence_Score"
        ]
    ].head(10).to_string(index=False)
)

print("\nFiles created:")
print("  ranked_influencers.csv")
print("  ranked_influencers.xlsx")
print("  top_10_influencers_by_category.csv")
print("  engagement_model_feature_importance.csv")

print("\nNo synthetic Instagram engagement/contact data was generated.")
print("=" * 75)