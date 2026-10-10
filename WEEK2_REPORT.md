# Week 2 Report: Data Cleaning and Preprocessing

**Project:** AI-Powered Instagram Influencer Analytics & Automation Insights  
**Organization:** SR Next  
**Phase:** Data Cleaning and Preprocessing

## 1. Objective

The objective of Week 2 was to clean, normalize, and validate the influencer profile and post datasets so they could be used for analysis, influencer ranking, and machine learning experiments.

## 2. Input Datasets

The preprocessing workflow used two main datasets:

| File | Rows | Columns |
|---|---:|---:|
| `final_influencer_dataset_normalized.csv` | 23,726 | 15 |
| `final_influencer_posts.csv` | 2,802 | 42 |

These counts reflect the latest inspection of the working files.

## 3. Profile Dataset

The normalized profile dataset contains the following fields:

- `username`
- `followers`
- `category`
- `profile_posts_total`
- `dataset_posts_available`
- `verified`
- `recent_posts`
- `avg_likes`
- `avg_comments`
- `total_likes`
- `total_comments`
- `engagement_rate`
- `post_frequency`
- `latest_post`
- `oldest_post`

These fields provide information about influencer identity, audience size, category, available post coverage, engagement, and posting activity.

## 4. Post Dataset

The post dataset includes fields such as:

- `ownerUsername`
- `ownerFullName`
- `id`
- `shortCode`
- `timestamp`
- `likesCount`
- `commentsCount`
- `caption`
- `hashtags/0` through `hashtags/29`
- `type`
- `productType`
- `isCommentsDisabled`
- `isPinned`
- `url`
- `displayUrl`
- `videoUrl`

The dataset stores post-level information. Hashtags are represented in separate columns in this export, and some post metadata fields may be empty for certain records.

## 5. Cleaning and Preprocessing

The project workflow includes the following data preparation activities:

1. **Profile normalization:** Standardized profile records into a consistent table structure.
2. **Eligibility filtering:** Prepared the target pool of profiles with fewer than 1,000,000 followers.
3. **Duplicate handling:** Used account usernames as the primary identifier when checking profile duplication.
4. **Numeric validation:** Prepared follower counts and engagement-related values for numerical analysis.
5. **Category handling:** Organized influencer category information for category-wise analysis.
6. **Post matching:** Used account usernames to associate post records with influencer profiles.
7. **Post coverage tracking:** Kept total profile records separate from accounts with available post observations.
8. **Date and engagement fields:** Retained timestamps, likes, and comments for further analysis.
9. **Export preparation:** Stored normalized profile and post records in CSV format for downstream processing.

Missing fields were not intentionally fabricated. The existence of a row does not mean every field in that row is populated; the final missing-value counts should be reported after validation.

## 6. Final Dataset Summary

The latest inspected files contain:

- **23,726 influencer profile records**
- **2,802 post records**
- **15 profile columns**
- **42 post columns**

The post records represent multiple posts from a smaller set of accounts. Therefore, profile coverage and post coverage are reported separately.

## 7. Validation and Quality Checks

The datasets were validated using a Python script with Pandas.

### 7.1 Profile Dataset Validation

The profile dataset contains 23,726 records and 15 columns.

| Validation check | Result |
|---|---:|
| Total profile rows | 23,726 |
| Unique usernames | 23,726 |
| Duplicate usernames | 0 |
| Missing usernames | 0 |
| Missing follower counts | 0 |
| Invalid or negative follower counts | 0 |
| Profiles with fewer than 1 million followers | 23,726 |
| Missing categories | 0 |
| Missing verification values | 12 |
| Profiles with missing latest-post dates | 23,521 |
| Profiles with missing oldest-post dates | 23,521 |

All profile records have unique usernames, valid non-negative follower counts, and populated category fields. Twelve profiles have missing verification values, while latest-post and oldest-post dates are unavailable for most profiles.

The missing date values are documented rather than treated as evidence that the accounts have never published content.

### 7.2 Post Dataset Validation

The post dataset contains 2,802 records and 42 columns.

| Validation check | Result |
|---|---:|
| Total post rows | 2,802 |
| Unique post accounts | 325 |
| Duplicate post IDs | 0 |
| Missing account usernames | 0 |
| Missing timestamps | 872 |
| Missing likes counts | 0 |
| Missing comments counts | 0 |
| Missing captions | 34 |

The post dataset has no duplicate post IDs according to the validation check. However, 872 records have missing timestamps, and 34 records have missing captions. These fields should be considered when performing time-based or caption-based analysis.

### 7.3 Profile-to-Post Matching

All 325 unique accounts in the post dataset matched usernames in the normalized profile dataset.

| Matching check | Result |
|---|---:|
| Post accounts matching profiles | 325 |
| Post accounts not matching profiles | 0 |

This indicates that every account represented in the post dataset has a corresponding profile record after normalizing usernames for comparison.

### 7.4 Overall Assessment

The profile dataset passed the basic checks for username uniqueness, follower-count completeness, follower eligibility, and category completeness.

The post dataset passed the basic username and post-ID checks, but some timestamps and captions are missing. These limitations are recorded so that missing information is not mistaken for zero activity or used as unsupported evidence.

The validation confirms basic structural consistency. It does not independently establish that every source value is accurate or current.
## 8. Output Files

The main preprocessed datasets are:

- `final_influencer_dataset_normalized.csv`
- `final_influencer_posts.csv`

Additional processed files may include:

- `influencers_phase1_filtered.csv`
- `influencers_phase1_filtered.xlsx`

The additional Phase 1 outputs should be included if they are generated by the final processing script and are part of the submitted workflow.

## 9. Limitations

- Post-level observations are available for fewer accounts than the total profile pool.
- Some profile and post attributes may be missing.
- Post engagement may vary over time and may not represent complete account performance.
- Differences in data sources can affect completeness and consistency.
- Results should be interpreted in light of data coverage and collection limitations.

## 10. Conclusion

Week 2 produced normalized profile and post datasets for the next stage of the project. These datasets support influencer ranking, engagement analysis, category-wise comparisons, and exploratory machine learning.

The data preparation workflow also preserves the distinction between eligible influencer profiles and accounts for which post-level evidence is available.

**Repository:** https://github.com/bultimistry/instagram_influencer_analytics
