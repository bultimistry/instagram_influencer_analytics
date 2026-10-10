# Week 1 Report: Data Collection Process, Tools, and Sources

**Project:** AI-Powered Instagram Influencer Analytics & Automation Insights  
**Organization:** SR Next  
**Project Type:** Data Scraping and Python Data Analysis

## 1. Objective

The objective of Week 1 was to identify eligible Instagram influencer profiles, assemble profile and post data, and prepare the data for cleaning, validation, and further analysis.

The project focuses on influencers with fewer than 1,000,000 followers.

## 2. Data Collection Process

The project used a combination of available influencer profile data and collected Instagram post records.

The main steps were:

1. Prepared a pool of eligible influencer profiles.
2. Identified profile records with fewer than 1,000,000 followers.
3. Organized profile information, including usernames, followers, categories, verification status, and post availability.
4. Prepared post-level records containing information such as usernames, timestamps, likes, comments, captions, and hashtags.
5. Matched post records to account usernames where possible.
6. Investigated accounts with missing post coverage and prepared additional candidate accounts for collection.
7. Stored the profile and post datasets separately for easier validation and analysis.

Instagram access restrictions affected the collection process, so the available post records do not cover every eligible profile.

## 3. Tools and Technologies

- **Python:** Main programming language.
- **Pandas:** Reading, cleaning, transforming, and validating CSV data.
- **CSV and Excel:** Storing and reviewing datasets.
- **VS Code:** Development environment.
- **PowerShell:** Running Python scripts and inspecting output.
- **Apify:** Used in the post-data collection workflow.
- **Git and GitHub:** Version control and project submission.

## 4. Data Sources

The project uses available influencer profile dataset records and Instagram post records collected through the project's data collection workflow.

Profile data includes usernames, follower counts, categories, verification status, and post-related metrics where available.

Post data includes account usernames, timestamps, likes, comments, captions, hashtags, and other post metadata.

The profile dataset and post dataset have different coverage. The project does not claim that all profiles were freshly scraped from Instagram. The final submission should identify any original source datasets used in the workflow and include their links where available.

## 5. Initial Dataset Summary

The latest recorded datasets contain:

| Dataset | Records | Columns |
|---|---:|---:|
| Normalized influencer profiles | 23,726 | 15 |
| Instagram post records | 2,802 | 42 |

The profile dataset is stored in `final_influencer_dataset_normalized.csv`.

The post dataset is stored in `final_influencer_posts.csv`.

The post dataset contains records from multiple posts per account, so the number of post records is not the number of unique influencers.

## 6. Challenges Encountered

- Automated access to Instagram was restricted during early collection attempts.
- Not every eligible influencer had available post records.
- Different data sources and exports used different column names and structures.
- Additional work was needed to match profile usernames with post usernames.
- Missing post data made it important to distinguish profile eligibility from engagement-data availability.

## 7. Week 1 Outcome

Week 1 established the data foundation for the project. The profile dataset and post dataset were organized and prepared for validation, cleaning, and preprocessing in the next stage.

## 8. Conclusion

The data collection and preparation work provided a structured starting point for the influencer analytics project. The resulting datasets support further data quality checks, engagement analysis, influencer ranking, and dashboard development.

**Repository:** https://github.com/bultimistry/instagram_influencer_analytics
