import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="SR NEXT Influencer Analytics", layout="wide")

st.title("📊 AI-Powered Instagram Influencer Dashboard")
st.markdown("### SR NEXT Phase 2 Deliverable — Micro/Macro Influencer Ranking (<1M Followers)")

# Load Data
@st.cache_data
def load_data():
    if os.path.exists("ranked_influencers.csv"):
        return pd.read_csv("ranked_influencers.csv")
    elif os.path.exists("influencers_phase1_filtered.csv"):
        df = pd.read_csv("influencers_phase1_filtered.csv")
        df['Rank'] = df.index + 1
        df['AI_Predicted_Engagement'] = df['Engagement Rate (%)']
        df['Composite_Score'] = df['Engagement Rate (%)']
        return df
    else:
        st.error("No dataset found! Please run 'phase2_ml_ranking.py' first.")
        st.stop()

df = load_data()

# Ensure required fallback columns exist
if 'Rank' not in df.columns:
    df['Rank'] = df.index + 1
if 'AI_Predicted_Engagement' not in df.columns:
    df['AI_Predicted_Engagement'] = df['Engagement Rate (%)']
if 'Composite_Score' not in df.columns:
    df['Composite_Score'] = df['Engagement Rate (%)']

#  Sidebar Filters
st.sidebar.header("Filter Options")

categories = ["All"] + list(df['Category'].unique())
selected_category = st.sidebar.selectbox("Select Niche / Category", categories)

min_followers, max_followers = int(df['Followers'].min()), int(df['Followers'].max())
selected_followers = st.sidebar.slider("Follower Range", min_followers, max_followers, (min_followers, max_followers))

# Filter DataFrame
filtered_df = df.copy()
if selected_category != "All":
    filtered_df = filtered_df[filtered_df['Category'] == selected_category]

filtered_df = filtered_df[
    (filtered_df['Followers'] >= selected_followers[0]) & 
    (filtered_df['Followers'] <= selected_followers[1])
]

#  High-Level Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Influencers Analyzed", f"{len(filtered_df):,}")
col2.metric("Avg Engagement Rate", f"{filtered_df['Engagement Rate (%)'].mean():.2f}%")
col3.metric("Avg Followers", f"{int(filtered_df['Followers'].mean()):,}")
col4.metric("Top Ranked Profile", filtered_df.iloc[0]['Name / Username'] if len(filtered_df) > 0 else "N/A")

st.markdown("---")

#  Ranked Influencers Table
st.subheader("🏆 Ranked Influencer Directory")

display_cols = [col for col in [
    'Rank', 'Name / Username', 'Instagram handle', 'Category', 
    'Followers', 'Engagement Rate (%)', 'AI_Predicted_Engagement', 
    'Composite_Score', 'Automation Usage', 'Contact Details'
] if col in filtered_df.columns]

st.dataframe(filtered_df[display_cols], width="stretch")

#  Interactive Visualizations
st.markdown("---")
st.subheader("📈 Category & Performance Insights")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    fig_cat = px.histogram(
        filtered_df, x="Category", color="Category", 
        title="Distribution of Influencers by Category"
    )
    st.plotly_chart(fig_cat, width="stretch")

with chart_col2:
    fig_scatter = px.scatter(
        filtered_df, x="Followers", y="Engagement Rate (%)", 
        color="Category", hover_name="Name / Username",
        title="Followers vs. Engagement Rate (%)"
    )
    st.plotly_chart(fig_scatter, width="stretch")