"""
SR NEXT - AI-Powered Instagram Influencer Analytics
Phase 1: Real Data Preparation

SOURCE FILES
------------
1. final_influencer_dataset_normalized.csv
   23,726 unique influencer profiles

2. final_influencer_posts.csv
   Real post-level data for 325 accounts

IMPORTANT
---------
This script NEVER generates fake/random:
- followers
- engagement
- emails
- posting frequency
- hashtags
- automation usage
- categories

Unavailable information is kept as NA/Unknown.
"""

from pathlib import Path
from collections import Counter
import re

import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

PROFILE_FILE = BASE_DIR / "final_influencer_dataset_normalized.csv"
POST_FILE = BASE_DIR / "final_influencer_posts.csv"

OUTPUT_CSV = BASE_DIR / "influencers_phase1_filtered.csv"
OUTPUT_XLSX = BASE_DIR / "influencers_phase1_filtered.xlsx"


# ============================================================
# CONSTANTS
# ============================================================

REQUIRED_PROFILE_COLUMNS = [
    "username",
    "followers",
    "category",
    "profile_posts_total",
    "dataset_posts_available",
    "verified",
]

REQUIRED_POST_COLUMNS = [
    "ownerUsername",
    "timestamp",
    "likesCount",
    "commentsCount",
    "caption",
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_username(value):
    """Normalize an Instagram username."""

    if pd.isna(value):
        return pd.NA

    value = str(value).strip()

    if not value:
        return pd.NA

    value = value.replace(
        "https://www.instagram.com/",
        ""
    )

    value = value.replace(
        "https://instagram.com/",
        ""
    )

    value = value.replace(
        "http://www.instagram.com/",
        ""
    )

    value = value.replace(
        "http://instagram.com/",
        ""
    )

    value = value.strip("/")
    value = value.lstrip("@")

    return value.lower()


def clean_category(value):
    """Preserve the real category."""

    if pd.isna(value):
        return "Unknown"

    value = str(value).strip()

    if not value:
        return "Unknown"

    return value


def safe_numeric(series):
    """Convert a pandas series to numeric."""

    return pd.to_numeric(
        series,
        errors="coerce"
    )


def extract_hashtags(caption):
    """Extract real hashtags from a caption."""

    if pd.isna(caption):
        return []

    caption = str(caption)

    hashtags = re.findall(
        r"#([A-Za-z0-9_\u0080-\uffff]+)",
        caption
    )

    return [
        tag.lower()
        for tag in hashtags
        if tag.strip()
    ]


def calculate_hashtag_diversity(hashtags):
    """
    Simple hashtag diversity metric.

    unique hashtags / total hashtags
    """

    if not hashtags:
        return 0.0

    return round(
        len(set(hashtags)) / len(hashtags),
        4
    )


def calculate_post_frequency(timestamps):
    """
    Estimate posts/month from the observed post window.

    This is calculated only from real timestamps.
    """

    timestamps = pd.to_datetime(
        timestamps,
        errors="coerce",
        utc=True
    ).dropna()

    if len(timestamps) < 2:
        return pd.NA

    earliest = timestamps.min()
    latest = timestamps.max()

    days = (
        latest - earliest
    ).total_seconds() / 86400

    if days <= 0:
        return pd.NA

    months = days / 30.4375

    if months <= 0:
        return pd.NA

    return round(
        len(timestamps) / months,
        2
    )


def calculate_last_10_metrics(group):
    """
    Calculate metrics using the most recent 10 real posts.
    """

    group = group.copy()

    group["timestamp"] = pd.to_datetime(
        group["timestamp"],
        errors="coerce",
        utc=True
    )

    group["likesCount"] = safe_numeric(
        group["likesCount"]
    )

    group["commentsCount"] = safe_numeric(
        group["commentsCount"]
    )

    # Most recent posts first.
    group = group.sort_values(
        "timestamp",
        ascending=False,
        na_position="last"
    )

    # SR NEXT specifically asks for last 10 posts.
    last_10 = group.head(10).copy()

    post_count = len(last_10)

    if post_count == 0:
        return {
            "post_count_used": 0,
            "likes": pd.NA,
            "comments": pd.NA,
            "engagement_rate": pd.NA,
            "posting_frequency": pd.NA,
            "hashtags": pd.NA,
            "hashtag_count": 0,
            "unique_hashtag_count": 0,
            "hashtag_diversity": 0.0,
            "caption_count": 0,
            "avg_caption_length": pd.NA,
        }

    likes = last_10["likesCount"].sum(
        min_count=1
    )

    comments = last_10["commentsCount"].sum(
        min_count=1
    )

    # Collect real hashtags from captions
    all_hashtags = []

    for caption in last_10["caption"].dropna():
        all_hashtags.extend(
            extract_hashtags(caption)
        )

    unique_hashtags = sorted(
        set(all_hashtags)
    )

    # Caption length
    caption_lengths = []

    for caption in last_10["caption"].dropna():
        caption_lengths.append(
            len(str(caption))
        )

    avg_caption_length = (
        round(
            sum(caption_lengths)
            / len(caption_lengths),
            2
        )
        if caption_lengths
        else pd.NA
    )

    return {
        "post_count_used": post_count,
        "likes": likes,
        "comments": comments,
        "posting_frequency": calculate_post_frequency(
            last_10["timestamp"]
        ),
        "hashtags": (
            ", ".join(
                f"#{tag}"
                for tag in unique_hashtags
            )
            if unique_hashtags
            else pd.NA
        ),
        "hashtag_count": len(all_hashtags),
        "unique_hashtag_count": len(
            unique_hashtags
        ),
        "hashtag_diversity": calculate_hashtag_diversity(
            all_hashtags
        ),
        "caption_count": len(caption_lengths),
        "avg_caption_length": avg_caption_length,
        "_captions": last_10[
            "caption"
        ].dropna().tolist(),
    }


# ============================================================
# START
# ============================================================

print("=" * 75)
print("SR NEXT - PHASE 1 REAL DATA PIPELINE")
print("=" * 75)


# ============================================================
# CHECK FILES
# ============================================================

if not PROFILE_FILE.exists():
    raise FileNotFoundError(
        f"Missing profile file:\n{PROFILE_FILE}"
    )

if not POST_FILE.exists():
    raise FileNotFoundError(
        f"Missing post file:\n{POST_FILE}"
    )


# ============================================================
# LOAD PROFILES
# ============================================================

print("\n[1/7] Loading profile dataset...")

profiles = pd.read_csv(
    PROFILE_FILE
)

print(
    f"Loaded profiles: {len(profiles):,}"
)

missing_profile_columns = [
    column
    for column in REQUIRED_PROFILE_COLUMNS
    if column not in profiles.columns
]

if missing_profile_columns:
    raise ValueError(
        "Missing profile columns:\n"
        + "\n".join(
            missing_profile_columns
        )
    )


# ============================================================
# PROFILE CLEANING
# ============================================================

print("\n[2/7] Cleaning and validating profiles...")

profiles["username"] = profiles[
    "username"
].apply(clean_username)

profiles["followers"] = safe_numeric(
    profiles["followers"]
)

profiles["category"] = profiles[
    "category"
].apply(clean_category)

profiles["profile_posts_total"] = safe_numeric(
    profiles["profile_posts_total"]
)

profiles["dataset_posts_available"] = safe_numeric(
    profiles["dataset_posts_available"]
)

# Remove profiles without usernames.
profiles = profiles.dropna(
    subset=["username"]
)

# Remove profiles without real follower count.
profiles = profiles.dropna(
    subset=["followers"]
)

# SR NEXT requirement: below 1M followers.
profiles = profiles[
    (profiles["followers"] >= 0)
    &
    (profiles["followers"] < 1_000_000)
].copy()

# Remove duplicate Instagram profiles.
profiles = profiles.drop_duplicates(
    subset=["username"],
    keep="first"
).reset_index(
    drop=True
)

print(
    f"Valid unique profiles: {len(profiles):,}"
)

print(
    f"Profiles under 1M followers: "
    f"{(
        profiles['followers'] < 1_000_000
    ).sum():,}"
)


# ============================================================
# LOAD POSTS
# ============================================================

print("\n[3/7] Loading real post dataset...")

posts = pd.read_csv(
    POST_FILE
)

print(
    f"Loaded posts: {len(posts):,}"
)

missing_post_columns = [
    column
    for column in REQUIRED_POST_COLUMNS
    if column not in posts.columns
]

if missing_post_columns:
    raise ValueError(
        "Missing post columns:\n"
        + "\n".join(
            missing_post_columns
        )
    )


# ============================================================
# CLEAN POSTS
# ============================================================

posts["ownerUsername"] = posts[
    "ownerUsername"
].apply(clean_username)

posts["timestamp"] = pd.to_datetime(
    posts["timestamp"],
    errors="coerce",
    utc=True
)

posts["likesCount"] = safe_numeric(
    posts["likesCount"]
)

posts["commentsCount"] = safe_numeric(
    posts["commentsCount"]
)

posts["caption"] = posts[
    "caption"
].fillna("")

posts = posts.dropna(
    subset=["ownerUsername"]
)

# Remove duplicate posts.
if "id" in posts.columns:
    posts = posts.drop_duplicates(
        subset=["id"],
        keep="first"
    )

print(
    f"Clean posts: {len(posts):,}"
)

print(
    f"Unique accounts with posts: "
    f"{posts['ownerUsername'].nunique():,}"
)


# ============================================================
# CALCULATE REAL LAST-10 METRICS
# ============================================================

print(
    "\n[4/7] Calculating real last-10-post metrics..."
)

metric_rows = []

for username, group in posts.groupby(
    "ownerUsername"
):

    metrics = calculate_last_10_metrics(
        group
    )

    metrics["username"] = username

    metric_rows.append(
        metrics
    )

post_metrics = pd.DataFrame(
    metric_rows
)

print(
    f"Accounts with calculated post metrics: "
    f"{len(post_metrics):,}"
)


# ============================================================
# MERGE
# ============================================================

print(
    "\n[5/7] Merging profiles and post metrics..."
)

df = profiles.merge(
    post_metrics,
    on="username",
    how="left"
)


# ============================================================
# REAL ENGAGEMENT RATE
# ============================================================

def calculate_engagement_rate(row):

    followers = row["followers"]
    likes = row["likes"]
    comments = row["comments"]
    post_count = row["post_count_used"]

    if pd.isna(followers):
        return pd.NA

    if followers <= 0:
        return pd.NA

    if pd.isna(likes):
        return pd.NA

    if pd.isna(comments):
        return pd.NA

    if pd.isna(post_count):
        return pd.NA

    if post_count <= 0:
        return pd.NA

    # Average likes/comments per post
    avg_likes = likes / post_count
    avg_comments = comments / post_count

    # SR NEXT formula:
    # (Likes + Comments) / Followers
    engagement = (
        (avg_likes + avg_comments)
        / followers
        * 100
    )

    return round(
        engagement,
        4
    )


df["Engagement Rate (%)"] = df.apply(
    calculate_engagement_rate,
    axis=1
)


# ============================================================
# BUILD PHASE 1 REQUIRED COLUMNS
# ============================================================

print(
    "\n[6/7] Building SR NEXT Phase 1 dataset..."
)

df["Name / Username"] = df[
    "username"
]

df["Instagram handle"] = (
    "@"
    + df["username"].astype(str)
)

df["Followers"] = df[
    "followers"
]

df["Category"] = df[
    "category"
]

df["Last 10 Posts Likes"] = df[
    "likes"
]

df["Last 10 Posts Comments"] = df[
    "comments"
]


def format_post_frequency(value):

    if pd.isna(value):
        return pd.NA

    return f"{value} posts/month"


df["Posting Frequency"] = df[
    "posting_frequency"
].apply(
    format_post_frequency
)

df["Hashtags / Content Themes"] = df[
    "hashtags"
]

# We do not have Instagram bio/contact data
# in the supplied profile/post datasets.
df["Contact Details"] = pd.NA

# We do not have verified evidence of automation
# usage in the supplied datasets.
df["Automation Usage"] = "Unknown"

df["Notes"] = df.apply(
    lambda row: (
        "Real last-10-post metrics available."
        if pd.notna(
            row["post_count_used"]
        )
        else
        "No post data available for this profile; "
        "post-derived metrics left blank."
    ),
    axis=1
)


# ============================================================
# FINAL OUTPUT
# ============================================================

output_columns = [
    "Name / Username",
    "Instagram handle",
    "Followers",
    "Category",
    "Last 10 Posts Likes",
    "Last 10 Posts Comments",
    "Engagement Rate (%)",
    "Contact Details",
    "Posting Frequency",
    "Hashtags / Content Themes",
    "Automation Usage",
    "Notes",
]

final_df = df[
    output_columns
].copy()


# ============================================================
# FINAL VALIDATION
# ============================================================

print(
    "\n[7/7] Final validation..."
)

total_profiles = len(final_df)

unique_profiles = (
    final_df[
        "Instagram handle"
    ].nunique()
)

under_1m = (
    final_df["Followers"] < 1_000_000
).all()

duplicate_handles = (
    final_df[
        "Instagram handle"
    ].duplicated()
    .sum()
)

engagement_available = (
    final_df[
        "Engagement Rate (%)"
    ].notna().sum()
)

post_frequency_available = (
    final_df[
        "Posting Frequency"
    ].notna().sum()
)

hashtag_available = (
    final_df[
        "Hashtags / Content Themes"
    ].notna().sum()
)


print()
print("-" * 75)
print("PHASE 1 VALIDATION")
print("-" * 75)

print(
    f"Total profiles             : {total_profiles:,}"
)

print(
    f"Unique Instagram profiles  : {unique_profiles:,}"
)

print(
    f"Followers below 1M         : {under_1m}"
)

print(
    f"Duplicate handles          : {duplicate_handles:,}"
)

print(
    f"Real engagement available  : "
    f"{engagement_available:,}"
)

print(
    f"Posting frequency available: "
    f"{post_frequency_available:,}"
)

print(
    f"Real hashtags available    : "
    f"{hashtag_available:,}"
)

print(
    f"Unknown automation status  : "
    f"{(
        final_df['Automation Usage']
        == 'Unknown'
    ).sum():,}"
)


# ============================================================
# CATEGORY SUMMARY
# ============================================================

print()
print("-" * 75)
print("CATEGORY DISTRIBUTION")
print("-" * 75)

print(
    final_df[
        "Category"
    ].value_counts(
        dropna=False
    ).to_string()
)


# ============================================================
# SAVE
# ============================================================

final_df.to_csv(
    OUTPUT_CSV,
    index=False
)

final_df.to_excel(
    OUTPUT_XLSX,
    index=False
)

print()
print("-" * 75)
print("OUTPUT")
print("-" * 75)

print(
    f"CSV  : {OUTPUT_CSV}"
)

print(
    f"Excel: {OUTPUT_XLSX}"
)

print()
print(
    "Phase 1 processing completed."
)

print(
    "No synthetic/random data was generated."
)

print("=" * 75)