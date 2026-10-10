# 📊 AI-Powered Instagram Influencer Analytics & Automation Insights

**Program:** SR NEXT Self-Guided Internship Program[cite: 1, 2]  
**Role:** Independent Intern / Project Contributor  
**Intern Name:** Bulti Mistry  
**Duration:** 4 Weeks Total (Phase 1 & Phase 2 Complete)[cite: 2]  
**Tech Stack:** Python, Pandas, NumPy, Scikit-Learn, Streamlit, Plotly, OpenPyXL  

---

## 📌 Executive Summary

This repository contains the complete end-to-end deliverables for the **SR NEXT Self-Guided Internship Program**[cite: 1, 2]. The project is divided into two major phases focusing on data collection, automated engagement calculation, predictive machine learning ranking, and interactive web dashboarding for Instagram creators and brand pages under 1 million followers[cite: 2, 3].

---

## 📁 Repository Structure

```text
instagram-influencer-analytics/
├── process_profile_data.py       # Phase 1: Data extraction, cleaning, and ER calculation script
├── phase2_ml_ranking.py          # Phase 2: Random Forest ML modeling and composite scoring script
├── app.py                        # Interactive Streamlit & Plotly web dashboard UI
├── influencers_phase1_filtered.csv  # Phase 1 Final Cleaned Dataset (CSV Format, 2,050+ records)
├── influencers_phase1_filtered.xlsx # Phase 1 Final Cleaned Dataset (Excel Format)
├── ranked_influencers.csv        # Phase 2 ML-Ranked Influencer Output
├── requirements.txt              # Python library dependencies
├── WEEK_1_REPORT.md              # Official Phase 1 Week-1 Submission Report
├── WEEK_2_REPORT.md              # Official Phase 2 Week-2 Submission Report
└── README.md                     # Comprehensive project documentation   

🔍 Phase 1 (Week 1): Data Collection & PreparationObjective: Collect public Instagram data and build a structured influencer dataset.
 Key Scope & Specifications:Dataset Size: Contains 2,050+ unique influencer profiles and pages.
 Follower Limit: Strictly filtered to accounts with fewer than 1M followers[cite: 3].Niche Categories:
 Balanced across Tech, Fashion, Fitness, Lifestyle, and Travel[cite: 3].Engagement Rate Formula: Programmatically calculated across the last 10 published posts using the required metric[cite: 3]:
 $$\text{Engagement Rate (\%)} = \left( \frac{\text{Last 10 Posts Likes} + \text{Last 10 Posts Comments}}{\text{Followers} \times 10} \right) \times 100$$Captured Data Points: Username, Handle, Followers, Category, Engagement Rate, Bio Contact Details, Posting Frequency (posts/month), Content Themes/Hashtags, and Automation Usage[cite: 3].

🤖 Phase 2 (Week 2): AI-Powered Analysis & RankingObjective: Analyze collected data, apply AI/ML techniques, and rank influencers.
 Key Execution Details:Feature Engineering: Processed engagement rates, monthly posting frequencies, hashtag diversity, and encoded categorical attributes (Category, Automation Usage).
 Predictive Modeling: Trained a RandomForestRegressor model in Scikit-Learn to model engagement trends based on followers, post counts, and categories.   Composite Scoring: Combined actual engagement metrics and AI predictions into a weighted influence ranking metric (ranked_influencers.csv)[cite: 4].Interactive Dashboard: Deployed a local web app using Streamlit and Plotly to visualize category breakdowns, top influencers, and follower-to-engagement correlations[cite: 4].

⚙️ Quick Start & Local Setup1. Install DependenciesPowerShellpip install -r requirements.txt

 Run Data Processing & ML PipelinesPowerShell# Step 1: Generate Phase 1 filtered dataset
 python process_profile_data.py

 Step 2: Run Phase 2 Machine Learning ranking
 python phase2_ml_ranking.py

 Launch Interactive Streamlit DashboardPowerShellpython -m streamlit run app.py
 Access the local web dashboard at: http://localhost:8501
