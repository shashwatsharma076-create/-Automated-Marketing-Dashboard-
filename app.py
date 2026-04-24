import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import base64

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="📊 Marketing Dashboard Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/shashwatsharma076-create',
        'Report a bug': 'https://github.com/shashwatsharma076-create',
        'About': '# Marketing Dashboard Pro\nBuilt with Streamlit + Plotly'
    }
)

# Custom CSS for enhanced UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main styling */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Dark metrics */
    .metric-dark {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Green success */
    .metric-success {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    
    /* Red warning */
    .metric-warning {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
    }
    
    /* Hide default header */
    header {visibility: hidden;}
    
    /* Custom title */
    .main-title {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Card hover effect */
    .css-1r6slb0 {
        transition: transform 0.3s ease;
    }
    .css-1r6slb0:hover {
        transform: translateY(-5px);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA GENERATOR - Simulates API Data
# ============================================================================

@st.cache_data
def generate_marketing_data():
    """Generate realistic marketing data (simulates API response)"""
    np.random.seed(42)
    n_records = 500
    
    # Date range
    dates = pd.date_range(end=datetime.now(), periods=90, freq='D')
    
    # Campaign types
    campaign_types = ['Social Media', 'Email', 'PPC', 'Content Marketing', 'Influencer', 'Retargeting']
    platforms = ['Facebook', 'Instagram', 'LinkedIn', 'Twitter', 'Google Ads', 'TikTok']
    content_types = ['Video', 'Image', 'Carousel', 'Story', 'Reels', 'Blog Post', 'Ad']
    
    data = {
        'date': np.random.choice(dates, n_records),
        'campaign_name': [f"CMP-{np.random.randint(1000,9999)}" for _ in range(n_records)],
        'campaign_type': np.random.choice(campaign_types, n_records),
        'platform': np.random.choice(platforms, n_records, p=[0.25, 0.25, 0.15, 0.15, 0.1, 0.1]),
        'content_type': np.random.choice(content_types, n_records),
        'impressions': np.random.lognormal(10, 1, n_records).astype(int),
        'clicks': np.random.lognormal(5, 1.5, n_records).astype(int),
        'conversions': np.random.lognormal(2, 1.5, n_records).astype(int),
        'spend': np.random.lognormal(4, 1.5, n_records).round(2),
        'revenue': np.random.lognormal(5, 2, n_records).round(2),
        'engagement_rate': np.random.beta(2, 5, n_records).round(4) * 100,
        'ctr': np.random.beta(1, 10, n_records).round(4) * 100,
        'conversion_rate': np.random.beta(1, 20, n_records).round(4) * 100,
    }
    
    df = pd.DataFrame(data)
    
    # Ensure logical relationships
    df['clicks'] = df['clicks'].apply(lambda x: max(1, min(x, df.loc[df.index[df['clicks']==x][0] if len(df.loc[df['clicks']==x])>0 else 0, 'impressions'] if 'impressions' in df.columns else x)))
    df['ctr'] = (df['clicks'] / df['impressions'] * 100).round(2)
    df['conversion_rate'] = (df['conversions'] / df['clicks'] * 100).round(2)
    df['cpc'] = (df['spend'] / df['clicks']).round(2)
    df['cpa'] = (df['spend'] / df['conversions']).round(2)
    df['roas'] = (df['revenue'] / df['spend']).round(2)
    
    return df.sort_values('date').reset_index(drop=True)

@st.cache_data
def generate_social_media_data():
    """Generate social media metrics"""
    np.random.seed(123)
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    
    data = {
        'date': dates,
        'followers': np.cumsum(np.random.randint(50, 200, 30)),
        'likes': np.random.randint(1000, 5000, 30),
        'comments': np.random.randint(50, 500, 30),
        'shares': np.random.randint(20, 200, 30),
        'posts': np.random.randint(1, 10, 30),
        'reach': np.random.randint(5000, 50000, 30),
        'engagement': np.random.uniform(2, 8, 30).round(2),
    }
    
    df = pd.DataFrame(data)
    df['followers'] = df['followers'].apply(lambda x: max(1000, x))
    return df

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

def render_sidebar():
    """Render sidebar navigation"""
    with st.sidebar:
        st.markdown("## 📊 Navigation")
        
        pages = {
            "🏠 Overview": "overview",
            "📈 Campaigns": "campaigns", 
            "📱 Social Media": "social",
            "💰 Spend Analysis": "spend",
            "🎯 Conversions": "conversions",
            "📋 Reports": "reports",
        }
        
        selected = st.radio("Go to", list(pages.keys()))
        
        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        
        date_range = st.date_input(
            "Select Date Range",
            value=(datetime.now() - timedelta(days=30), datetime.now())
        )
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.info("""
        **Marketing Dashboard Pro**
        
        Built with Streamlit + Plotly
        Real-time data visualization
        """)
        
        return pages[selected], date_range

# ============================================================================
# METRIC CARDS
# ============================================================================

def render_metric_card(title, value, change, prefix="", suffix="", color="blue"):
    """Render a metric card with trend"""
    colors = {
        "blue": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "green": "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)",
        "red": "linear-gradient(135deg, #eb3349 0%, #f45c43 100%)",
        "orange": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
    }
    
    change_emoji = "📈" if change > 0 else "📉"
    change_color = "#22c55e" if change > 0 else "#ef4444"
    
    st.markdown(f"""
    <div class="metric-card" style="background: {colors.get(color, colors['blue'])}">
        <p style="margin: 0; font-size: 0.9rem; opacity: 0.9;">{title}</p>
        <h2 style="margin: 5px 0; font-size: 2rem; font-weight: 700;">{prefix}{value:,.0f}{suffix}</h2>
        <p style="margin: 0; font-size: 0.85rem;">
            {change_emoji} <span style="color: {change_color};">{change:+.1f}%</span> vs last period
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_kpi_row(df, col1, col2):
    """Render KPI metrics row"""
    # Calculate metrics
    total_impressions = df['impressions'].sum()
    total_clicks = df['clicks'].sum()
    total_conversions = df['conversions'].sum()
    total_spend = df['spend'].sum()
    total_revenue = df['revenue'].sum()
    avg_ctr = (total_clicks / total_impressions * 100)
    avg_roas = total_revenue / total_spend
    
    # Display in columns
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        render_metric_card("Total Impressions", total_impressions, np.random.uniform(-5, 15), color="blue")
    with c2:
        render_metric_card("Total Clicks", total_clicks, np.random.uniform(-3, 10), color="green")
    with c3:
        render_metric_card("Conversions", total_conversions, np.random.uniform(0, 20), color="orange")
    with c4:
        render_metric_card("Revenue", total_revenue, "$", "", color="green")
    
    st.markdown("---")
    
    c5, c6, c7, c8 = st.columns(4)
    
    with c5:
        render_metric_card("CTR", avg_ctr, np.random.uniform(-2, 5), suffix="%", color="blue")
    with c6:
        render_metric_card("Spend", total_spend, "$", "", color="red")
    with c7:
        render_metric_card("ROAS", avg_roas, "x", "", color="green")
    with c8:
        render_metric_card("Cost/Conversion", total_spend/total_conversions, "$", "", color="orange")

# ============================================================================
# CHARTS
# ============================================================================

def render_line_chart(df, x_col, y_col, title, color=None):
    """Render line chart"""
    fig = px.line(
        df, x=x_col, y=y_col,
        title=title,
        template="plotly_dark",
        color=color,
        markers=True
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter"),
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

def render_bar_chart(df, x_col, y_col, title, color=None):
    """Render bar chart"""
    fig = px.bar(
        df, x=x_col, y=y_col,
        title=title,
        template="plotly_dark",
        color=color,
        text_auto=True
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter")
    )
    st.plotly_chart(fig, use_container_width=True)

def render_pie_chart(df, names, values, title):
    """Render pie chart"""
    fig = px.pie(
        df, values=values, names=names,
        title=title,
        template="plotly_dark",
        hole=0.4
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter")
    )
    st.plotly_chart(fig, use_container_width=True)

def render_scatter_chart(df, x_col, y_col, size_col, title, color_col=None):
    """Render scatter chart"""
    fig = px.scatter(
        df, x=x_col, y=y_col,
        size=size_col,
        title=title,
        template="plotly_dark",
        color=color_col,
        hover_data=df.columns,
        size_max=50
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter")
    )
    st.plotly_chart(fig, use_container_width=True)

def render_heatmap(df, title):
    """Render correlation heatmap"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    corr = df[numeric_cols].corr()
    
    fig = px.imshow(
        corr,
        title=title,
        template="plotly_dark",
        color_continuous_scale="RdBu_r",
        text_auto=True
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter")
    )
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE: OVERVIEW
# ============================================================================

def page_overview(df, social_df):
    """Overview page"""
    st.markdown("## 📊 Overview Dashboard")
    
    # KPI Row
    render_kpi_row(df, st, 1, 1)
    
    st.markdown("---")
    
    # Charts row 1
    c1, c2 = st.columns(2)
    
    with c1:
        # Daily impressions
        daily_df = df.groupby('date').agg({
            'impressions': 'sum',
            'clicks': 'sum',
            'conversions': 'sum'
        }).reset_index()
        render_line_chart(daily_df, 'date', 'impressions', 'Daily Impressions Trend', '#667eea')
    
    with c2:
        # Revenue over time
        revenue_df = df.groupby('date')['revenue'].sum().reset_index()
        render_line_chart(revenue_df, 'date', 'revenue', 'Revenue Over Time', '#11998e')
    
    st.markdown("---")
    
    # Charts row 2
    c3, c4 = st.columns(2)
    
    with c3:
        # Platform distribution
        platform_df = df.groupby('platform').agg({
            'impressions': 'sum',
            'clicks': 'sum',
            'spend': 'sum'
        }).reset_index()
        render_pie_chart(platform_df, 'platform', 'impressions', 'Impressions by Platform')
    
    with c4:
        # Campaign type distribution
        type_df = df.groupby('campaign_type')['revenue'].sum().reset_index()
        render_pie_chart(type_df, 'campaign_type', 'revenue', 'Revenue by Campaign Type')

# ============================================================================
# PAGE: CAMPAIGNS
# ============================================================================

def page_campaigns(df):
    """Campaigns page"""
    st.markdown("## 📈 Campaign Performance")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        campaign_type_filter = st.multiselect(
            "Campaign Type",
            options=df['campaign_type'].unique(),
            default=df['campaign_type'].unique()
        )
    
    with col2:
        platform_filter = st.multiselect(
            "Platform",
            options=df['platform'].unique(),
            default=df['platform'].unique()
        )
    
    with col3:
        sort_by = st.selectbox("Sort By", ['impressions', 'clicks', 'conversions', 'spend', 'revenue'])
    
    # Filter data
    filtered_df = df[
        (df['campaign_type'].isin(campaign_type_filter)) &
        (df['platform'].isin(platform_filter))
    ]
    
    # Aggregate by campaign
    campaign_df = filtered_df.groupby('campaign_name').agg({
        'impressions': 'sum',
        'clicks': 'sum',
        'conversions': 'sum',
        'spend': 'sum',
        'revenue': 'sum',
    }).reset_index()
    
    campaign_df['ctr'] = (campaign_df['clicks'] / campaign_df['impressions'] * 100).round(2)
    campaign_df['roas'] = (campaign_df['revenue'] / campaign_df['spend']).round(2)
    campaign_df = campaign_df.sort_values(sort_by, ascending=False)
    
    # Top campaigns table
    st.markdown("### Top Performing Campaigns")
    st.dataframe(
        campaign_df.head(20).style.background_gradient(subset=['impressions', 'clicks', 'revenue'], cmap='Greens'),
        use_container_width=True
    )
    
    st.markdown("---")
    
    # Visualizations
    c1, c2 = st.columns(2)
    
    with c1:
        render_bar_chart(campaign_df.head(10), 'campaign_name', 'impressions', 'Top 10 Campaigns by Impressions')
    
    with c2:
        render_bar_chart(campaign_df.head(10), 'campaign_name', 'revenue', 'Top 10 Campaigns by Revenue')

# ============================================================================
# PAGE: SOCIAL MEDIA
# ============================================================================

def page_social(social_df):
    """Social media page"""
    st.markdown("## 📱 Social Media Analytics")
    
    # Metrics
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        total_followers = social_df['followers'].iloc[-1]
        st.metric("Total Followers", f"{total_followers:,}", f"+{social_df['followers'].diff().sum():,}")
    
    with c2:
        total_likes = social_df['likes'].sum()
        st.metric("Total Likes", f"{total_likes:,}", f"+{social_df['likes'].diff().sum():,}")
    
    with c3:
        total_comments = social_df['comments'].sum()
        st.metric("Comments", f"{total_comments:,}", f"+{social_df['comments'].diff().sum():,}")
    
    with c4:
        avg_engagement = social_df['engagement'].mean()
        st.metric("Avg Engagement", f"{avg_engagement:.1f}%", f"{social_df['engagement'].diff().mean():.1f}%")
    
    st.markdown("---")
    
    # Charts
    c1, c2 = st.columns(2)
    
    with c1:
        # Follower growth
        fig = px.area(
            social_df, x='date', y='followers',
            title='Follower Growth',
            template='plotly_dark',
            fill='tozeroy'
        )
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        # Engagement metrics
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=social_df['date'], y=social_df['likes'], name='Likes', fill='tozeroy'))
        fig.add_trace(go.Scatter(x=social_df['date'], y=social_df['comments'], name='Comments', fill='tozeroy'))
        fig.add_trace(go.Scatter(x=social_df['date'], y=social_df['shares'], name='Shares', fill='tozeroy'))
        fig.update_layout(title='Engagement Over Time', template='plotly_dark', paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Social metrics heatmap
    social_corr = social_df[['likes', 'comments', 'shares', 'reach', 'engagement']].corr()
    fig = px.imshow(social_corr, text_auto=True, color_continuous_scale='RdBu_r', title='Metrics Correlation')
    fig.update_layout(template='plotly_dark', paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE: SPEND ANALYSIS
# ============================================================================

def page_spend(df):
    """Spend analysis page"""
    st.markdown("## 💰 Spend & Budget Analysis")
    
    # Metrics
    total_spend = df['spend'].sum()
    total_revenue = df['revenue'].sum()
    total_roi = ((total_revenue - total_spend) / total_spend * 100)
    
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.metric("Total Spend", f"${total_spend:,.2f}")
    
    with c2:
        st.metric("Total Revenue", f"${total_revenue:,.2f}")
    
    with c3:
        st.metric("ROI", f"{total_roi:.1f}%")
    
    with c4:
        avg_cpc = df['cpc'].mean()
        st.metric("Avg CPC", f"${avg_cpc:.2f}")
    
    st.markdown("---")
    
    # Spend by platform
    platform_spend = df.groupby('platform').agg({
        'spend': 'sum',
        'revenue': 'sum',
        'clicks': 'sum'
    }).reset_index()
    platform_spend['cpc'] = (platform_spend['spend'] / platform_spend['clicks']).round(2)
    
    c1, c2 = st.columns(2)
    
    with c1:
        render_bar_chart(platform_spend, 'platform', 'spend', 'Spend by Platform')
    
    with c2:
        render_bar_chart(platform_spend, 'platform', 'revenue', 'Revenue by Platform')
    
    st.markdown("---")
    
    # ROAS by platform
    platform_spend['roas'] = (platform_spend['revenue'] / platform_spend['spend']).round(2)
    fig = px.scatter(
        platform_spend, x='spend', y='revenue',
        size='clicks', color='roas',
        hover_data=['platform'],
        title='Spend vs Revenue by Platform',
        template='plotly_dark'
    )
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE: CONVERSIONS
# ============================================================================

def page_conversions(df):
    """Conversions page"""
    st.markdown("## 🎯 Conversion Analysis")
    
    # Metrics
    total_conversions = df['conversions'].sum()
    total_clicks = df['clicks'].sum()
    conversion_rate = total_conversions / total_clicks * 100
    total_spend = df['spend'].sum()
    cpa = total_spend / total_conversions
    
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.metric("Total Conversions", f"{total_conversions:,}")
    
    with c2:
        st.metric("Conversion Rate", f"{conversion_rate:.2f}%")
    
    with c3:
        st.metric("Cost per Acquisition", f"${cpa:.2f}")
    
    with c4:
        conversions_per_day = total_conversions / 90
        st.metric("Daily Conversions", f"{conversions_per_day:.1f}")
    
    st.markdown("---")
    
    # Conversion funnel
    funnel_df = pd.DataFrame({
        'Stage': ['Impressions', 'Clicks', 'Conversions'],
        'Count': [df['impressions'].sum(), df['clicks'].sum(), df['conversions'].sum()]
    })
    
    fig = px.funnel(
        funnel_df, x='Count', y='Stage',
        title='Conversion Funnel',
        template='plotly_dark'
    )
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Conversion by campaign type
    conv_type = df.groupby('campaign_type').agg({
        'conversions': 'sum',
        'spend': 'sum',
        'clicks': 'sum'
    }).reset_index()
    conv_type['conversion_rate'] = (conv_type['conversions'] / conv_type['clicks'] * 100).round(2)
    
    c1, c2 = st.columns(2)
    
    with c1:
        render_bar_chart(conv_type, 'campaign_type', 'conversions', 'Conversions by Campaign Type')
    
    with c2:
        render_bar_chart(conv_type, 'campaign_type', 'conversion_rate', 'Conversion Rate by Campaign Type')

# ============================================================================
# PAGE: REPORTS
# ============================================================================

def page_reports(df):
    """Reports page"""
    st.markdown("## 📋 Reports & Export")
    
    st.markdown("### 📥 Download Reports")
    
    # CSV Export
    csv = df.to_csv(index=False)
    st.download_button(
        label="📊 Download Full Data (CSV)",
        data=csv,
        file_name="marketing_data_export.csv",
        mime="text/csv"
    )
    
    st.markdown("---")
    
    st.markdown("### 📈 Summary Reports")
    
    # Summary statistics
    st.markdown("#### Performance Summary")
    summary_stats = df.describe()
    st.dataframe(summary_stats)
    
    st.markdown("---")
    
    st.markdown("#### Platform Comparison")
    platform_summary = df.groupby('platform').agg({
        'impressions': 'sum',
        'clicks': 'sum',
        'conversions': 'sum',
        'spend': 'sum',
        'revenue': 'sum'
    })
    st.dataframe(platform_summary)
    
    st.markdown("---")
    
    st.markdown("#### Campaign Type Comparison")
    type_summary = df.groupby('campaign_type').agg({
        'impressions': 'sum',
        'clicks': 'sum',
        'conversions': 'sum',
        'spend': 'sum',
        'revenue': 'sum'
    })
    st.dataframe(type_summary)

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    """Main application"""
    
    # Load data
    with st.spinner("Loading data..."):
        df = generate_marketing_data()
        social_df = generate_social_media_data()
    
    # Get page selection
    page, date_range = render_sidebar()
    
    # Render selected page
    if page == "overview":
        page_overview(df, social_df)
    elif page == "campaigns":
        page_campaigns(df)
    elif page == "social":
        page_social(social_df)
    elif page == "spend":
        page_spend(df)
    elif page == "conversions":
        page_conversions(df)
    elif page == "reports":
        page_reports(df)

if __name__ == "__main__":
    main()